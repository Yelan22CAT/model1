#!/usr/bin/env python3
"""Bridge-0 exact-integer semantic validator v0.12."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from validator_v0_3 import issue


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
CANONICAL_INT = re.compile(r"^(?:0|-?[1-9][0-9]*)$")
ALLOWED_TARGETS = {"python312", "node20"}


def csv_values(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [v.strip() for v in raw.split(",") if v.strip()]


def exact_int_values(raw: Any) -> list[int] | None:
    parts = csv_values(raw)
    if not parts:
        return None
    values: list[int] = []
    for part in parts:
        if not CANONICAL_INT.fullmatch(part):
            return None
        values.append(int(part))
    return values


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    errors = []
    warnings = []
    conflicts = []

    statements = doc.get("statements")
    if not isinstance(statements, list):
        errors.append(issue("V079", "statements must be a list"))
        return {"valid": False, "errors": errors, "warnings": warnings, "conflicts": conflicts}

    programs = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "program"
    ]
    computes = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "semantic_compute"
    ]
    others = [
        s for s in statements
        if isinstance(s, dict)
        and s.get("kind") not in {"program", "semantic_compute"}
    ]

    if others:
        errors.append(issue("V079", "v0.12 executable subset contains unsupported statement kinds"))

    if len(programs) != 1:
        errors.append(issue("V079", "v0.12 requires exactly one program"))
    else:
        program = programs[0]
        sid = str(program.get("id"))
        name = program.get("name")
        targets = csv_values(program.get("targets"))
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            errors.append(issue("V079", "program name is invalid", sid))
        if len(targets) != len(set(targets)):
            errors.append(issue("V080", "program targets must be unique", sid))
        if set(targets) != ALLOWED_TARGETS:
            errors.append(
                issue(
                    "V080",
                    "v0.12 exact-integer test requires exactly python312,node20",
                    sid,
                )
            )

    if len(computes) != 1:
        errors.append(issue("V081", "v0.12 requires exactly one semantic compute task"))
    else:
        task = computes[0]
        sid = str(task.get("id"))

        if task.get("op") != "stats":
            errors.append(issue("V081", "v0.12 supports only op=stats", sid))
        if task.get("numeric") != "exact_integer":
            errors.append(issue("V082", "v0.12 requires numeric=exact_integer", sid))
        if task.get("observe") != "json_value":
            errors.append(issue("V082", "v0.12 requires observe=json_value", sid))

        values = exact_int_values(task.get("values"))
        if values is None:
            errors.append(
                issue(
                    "V083",
                    "values must be canonical decimal exact integers",
                    sid,
                )
            )
        elif len(values) > 256:
            errors.append(issue("V083", "values list exceeds v0.12 limit", sid))

        allowed = {"id", "kind", "op", "numeric", "values", "observe"}
        extras = set(task) - allowed
        if extras:
            errors.append(issue("V083", "semantic compute contains unsupported fields", sid))

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
    }


def main() -> int:
    try:
        doc = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"valid": False, "errors": [{"rule": "V000", "message": str(exc)}]}))
        return 2
    result = validate_document(doc)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
