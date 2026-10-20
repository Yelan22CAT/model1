#!/usr/bin/env python3
"""Bridge-0 multi-backend equivalence validator v0.9."""

from __future__ import annotations

import json
import sys
from typing import Any

from validator_v0_3 import issue
from validator_v0_8 import validate_document as validate_v08


ALLOWED_OBSERVABLES = {"stdout"}


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    base = validate_v08(doc)
    errors = list(base["errors"])
    warnings = list(base["warnings"])
    conflicts = list(base["conflicts"])

    statements = doc.get("statements")
    if not isinstance(statements, list):
        return base

    observable_count = 0

    for task in statements:
        if not isinstance(task, dict) or task.get("kind") != "workflow_task":
            continue
        sid = str(task.get("id"))
        opcode = task.get("task_kind")
        observe = task.get("observe")

        if observe is not None:
            if opcode != "python_module":
                errors.append(
                    issue(
                        "V068",
                        "v0.9 observables are supported only for python_module",
                        sid,
                    )
                )
            elif observe not in ALLOWED_OBSERVABLES:
                errors.append(
                    issue(
                        "V068",
                        f"unsupported observable: {observe!r}",
                        sid,
                    )
                )
            else:
                observable_count += 1

        if opcode == "python_module":
            allowed = {
                "id",
                "kind",
                "task_kind",
                "module",
                "cwd",
                "args",
                "observe",
            }
            extras = set(task) - allowed
            if extras:
                errors.append(
                    issue(
                        "V069",
                        "python_module contains unsupported compiler fields",
                        sid,
                    )
                )

    if observable_count == 0:
        warnings.append(
            issue(
                "V070",
                "program contains no observable task; backend equivalence cannot be measured",
            )
        )

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
        "authority_epoch": base.get("authority_epoch", 0),
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
