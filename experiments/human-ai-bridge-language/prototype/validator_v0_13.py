#!/usr/bin/env python3
"""Bridge-0 binary64 floating semantic validator v0.13."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from validator_v0_3 import issue


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
FINITE_HALF = re.compile(r"^-?(?:[0-9]+)\.5$")
ALLOWED_TARGETS = {"python312", "node20"}
SPECIAL_TOKENS = {"nan", "+inf", "-inf", "-0", "+0"}


def csv_values(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [v.strip() for v in raw.split(",") if v.strip()]


def valid_float_token(token: str) -> bool:
    return token in SPECIAL_TOKENS or bool(FINITE_HALF.fullmatch(token))


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    errors = []
    warnings = []
    conflicts = []

    statements = doc.get("statements")
    if not isinstance(statements, list):
        errors.append(issue("V084", "statements must be a list"))
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
        errors.append(issue("V084", "v0.13 executable subset contains unsupported statement kinds"))

    if len(programs) != 1:
        errors.append(issue("V084", "v0.13 requires exactly one program"))
    else:
        program = programs[0]
        sid = str(program.get("id"))
        name = program.get("name")
        targets = csv_values(program.get("targets"))
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            errors.append(issue("V084", "program name is invalid", sid))
        if len(targets) != len(set(targets)):
            errors.append(issue("V085", "program targets must be unique", sid))
        if set(targets) != ALLOWED_TARGETS:
            errors.append(
                issue(
                    "V085",
                    "v0.13 float test requires exactly python312,node20",
                    sid,
                )
            )

    if len(computes) != 1:
        errors.append(issue("V086", "v0.13 requires exactly one semantic compute task"))
    else:
        task = computes[0]
        sid = str(task.get("id"))
        if task.get("op") != "float_profile":
            errors.append(issue("V086", "v0.13 supports only op=float_profile", sid))
        if task.get("numeric") != "binary64":
            errors.append(issue("V087", "v0.13 requires numeric=binary64", sid))
        if task.get("rounding") != "ties_to_even":
            errors.append(issue("V087", "v0.13 requires rounding=ties_to_even", sid))
        if task.get("observe") != "json_value":
            errors.append(issue("V087", "v0.13 requires observe=json_value", sid))

        values = csv_values(task.get("values"))
        if not values:
            errors.append(issue("V088", "float values must be non-empty", sid))
        else:
            bad = [value for value in values if not valid_float_token(value)]
            if bad:
                errors.append(
                    issue(
                        "V088",
                        "unsupported or non-canonical float token(s): " + ", ".join(bad),
                        sid,
                    )
                )
            if len(values) != len(set(values)):
                errors.append(issue("V088", "float tokens must be unique", sid))
            required = {"nan", "+inf", "-inf", "-0", "+0", "2.5", "3.5", "-2.5", "-3.5"}
            if not required.issubset(set(values)):
                errors.append(
                    issue(
                        "V088",
                        "v0.13 conformance vector must include all required edge tokens",
                        sid,
                    )
                )

        allowed = {"id", "kind", "op", "numeric", "rounding", "values", "observe"}
        extras = set(task) - allowed
        if extras:
            errors.append(issue("V088", "semantic compute contains unsupported fields", sid))

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
