#!/usr/bin/env python3
"""Bridge-0 executable migration / loss-audit validator v0.17."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from validator_v0_3 import issue


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
ALLOWED_TARGETS = {"python312", "node20"}
ALLOWED_ROUTES = {"v1_to_v2", "v1_to_v3_compact"}


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
        errors.append(issue("V106", "statements must be a list"))
        return {"valid": False, "errors": errors, "warnings": warnings, "conflicts": conflicts}

    programs = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "program"
    ]
    migrations = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "semantic_migration"
    ]
    others = [
        s for s in statements
        if isinstance(s, dict)
        and s.get("kind") not in {"program", "semantic_migration"}
    ]

    if others:
        errors.append(issue("V106", "v0.17 executable subset contains unsupported statement kinds"))

    if len(programs) != 1:
        errors.append(issue("V106", "v0.17 requires exactly one program"))
    else:
        program = programs[0]
        sid = str(program.get("id"))
        name = program.get("name")
        targets = csv_values(program.get("targets"))
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            errors.append(issue("V106", "program name is invalid", sid))
        if len(targets) != len(set(targets)):
            errors.append(issue("V107", "program targets must be unique", sid))
        if set(targets) != ALLOWED_TARGETS:
            errors.append(
                issue(
                    "V107",
                    "v0.17 migration test requires exactly python312,node20",
                    sid,
                )
            )

    if len(migrations) != 1:
        errors.append(issue("V108", "v0.17 requires exactly one migration task"))
    else:
        task = migrations[0]
        sid = str(task.get("id"))

        if task.get("domain") != "grapheme":
            errors.append(issue("V108", "v0.17 supports only domain=grapheme", sid))
        if task.get("artifact") != "fixture_v1":
            errors.append(issue("V109", "v0.17 requires artifact=fixture_v1", sid))

        routes = csv_values(task.get("routes"))
        if len(routes) != len(set(routes)):
            errors.append(issue("V109", "migration routes must be unique", sid))
        if set(routes) != ALLOWED_ROUTES:
            errors.append(
                issue(
                    "V109",
                    "v0.17 requires routes=v1_to_v2,v1_to_v3_compact",
                    sid,
                )
            )

        if task.get("loss_policy") != "reject_unacknowledged":
            errors.append(
                issue(
                    "V110",
                    "v0.17 requires loss_policy=reject_unacknowledged",
                    sid,
                )
            )
        if task.get("roundtrip") != "audit":
            errors.append(issue("V110", "v0.17 requires roundtrip=audit", sid))
        if task.get("execution") != "gate_on_audit":
            errors.append(issue("V110", "v0.17 requires execution=gate_on_audit", sid))
        if task.get("observe") != "json_value":
            errors.append(issue("V110", "v0.17 requires observe=json_value", sid))

        allowed = {
            "id",
            "kind",
            "domain",
            "artifact",
            "routes",
            "loss_policy",
            "roundtrip",
            "execution",
            "observe",
        }
        extras = set(task) - allowed
        if extras:
            errors.append(issue("V111", "migration task contains unsupported fields", sid))

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
