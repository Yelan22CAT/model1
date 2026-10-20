#!/usr/bin/env python3
"""Bridge-0 typed-observable / heterogeneous-runtime validator v0.10."""

from __future__ import annotations

import json
import sys
from typing import Any

from validator_v0_3 import issue
from validator_v0_8 import validate_document as validate_v08


ALLOWED_TYPED_OBSERVABLES = {"json_value"}
ALLOWED_TARGETS = {"ubuntu-latest", "windows-latest", "macos-latest"}


def csv_values(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [v.strip() for v in raw.split(",") if v.strip()]


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    base = validate_v08(doc)
    errors = list(base["errors"])
    warnings = list(base["warnings"])
    conflicts = list(base["conflicts"])

    statements = doc.get("statements")
    if not isinstance(statements, list):
        return base

    workflows = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "workflow"
    ]
    tasks = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "workflow_task"
    ]

    if len(workflows) == 1:
        workflow = workflows[0]
        targets = csv_values(workflow.get("targets"))
        if not targets:
            errors.append(issue("V071", "v0.10 workflow requires targets=", workflow.get("id")))
        else:
            if len(targets) != len(set(targets)):
                errors.append(issue("V071", "workflow targets must be unique", workflow.get("id")))
            unknown = [t for t in targets if t not in ALLOWED_TARGETS]
            if unknown:
                errors.append(
                    issue(
                        "V071",
                        "unsupported heterogeneous target(s): " + ", ".join(unknown),
                        workflow.get("id"),
                    )
                )
            if len(set(targets)) < 2:
                errors.append(issue("V071", "heterogeneous test requires at least two targets", workflow.get("id")))

    typed_count = 0
    for task in tasks:
        sid = str(task.get("id"))
        opcode = task.get("task_kind")
        observe = task.get("observe")

        if observe is not None:
            if opcode != "python_module":
                errors.append(issue("V072", "typed observable supported only for python_module", sid))
            elif observe not in ALLOWED_TYPED_OBSERVABLES:
                errors.append(issue("V072", f"unsupported typed observable: {observe!r}", sid))
            else:
                typed_count += 1

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
                errors.append(issue("V073", "python_module contains unsupported v0.10 fields", sid))

    if typed_count == 0:
        errors.append(issue("V074", "v0.10 requires at least one typed observable"))

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
