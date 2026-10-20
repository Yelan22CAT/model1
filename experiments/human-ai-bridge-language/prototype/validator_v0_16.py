#!/usr/bin/env python3
"""Bridge-0 semantic-profile compatibility validator v0.16."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from validator_v0_3 import issue


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
ALLOWED_TARGETS = {"python312", "node20"}
ALLOWED_PROFILES = {
    "grapheme_v1",
    "grapheme_v2",
    "grapheme_v3_breaking",
}


def csv_values(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [v.strip() for v in raw.split(",") if v.strip()]


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    errors = []
    warnings = []
    conflicts = []

    statements = doc.get("statements")
    if not isinstance(statements, list):
        errors.append(issue("V100", "statements must be a list"))
        return {"valid": False, "errors": errors, "warnings": warnings, "conflicts": conflicts}

    programs = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "program"
    ]
    checks = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "semantic_compatibility"
    ]
    others = [
        s for s in statements
        if isinstance(s, dict)
        and s.get("kind") not in {"program", "semantic_compatibility"}
    ]

    if others:
        errors.append(issue("V100", "v0.16 executable subset contains unsupported statement kinds"))

    if len(programs) != 1:
        errors.append(issue("V100", "v0.16 requires exactly one program"))
    else:
        program = programs[0]
        sid = str(program.get("id"))
        name = program.get("name")
        targets = csv_values(program.get("targets"))
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            errors.append(issue("V100", "program name is invalid", sid))
        if len(targets) != len(set(targets)):
            errors.append(issue("V101", "program targets must be unique", sid))
        if set(targets) != ALLOWED_TARGETS:
            errors.append(
                issue(
                    "V101",
                    "v0.16 compatibility test requires exactly python312,node20",
                    sid,
                )
            )

    if len(checks) != 1:
        errors.append(issue("V102", "v0.16 requires exactly one compatibility task"))
    else:
        task = checks[0]
        sid = str(task.get("id"))

        if task.get("domain") != "grapheme":
            errors.append(issue("V102", "v0.16 supports only domain=grapheme", sid))

        profiles = csv_values(task.get("profiles"))
        if len(profiles) != len(set(profiles)):
            errors.append(issue("V103", "profiles must be unique", sid))
        if set(profiles) != ALLOWED_PROFILES:
            errors.append(
                issue(
                    "V103",
                    "v0.16 requires grapheme_v1,grapheme_v2,grapheme_v3_breaking",
                    sid,
                )
            )

        if task.get("policy") != "behavioral_manifest":
            errors.append(issue("V104", "v0.16 requires policy=behavioral_manifest", sid))
        if task.get("migration") != "explicit":
            errors.append(issue("V104", "v0.16 requires migration=explicit", sid))
        if task.get("observe") != "json_value":
            errors.append(issue("V104", "v0.16 requires observe=json_value", sid))

        allowed = {
            "id",
            "kind",
            "domain",
            "profiles",
            "policy",
            "migration",
            "observe",
        }
        extras = set(task) - allowed
        if extras:
            errors.append(issue("V105", "compatibility task contains unsupported fields", sid))

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
