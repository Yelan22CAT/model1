#!/usr/bin/env python3
"""Bridge-0 compiler-facing workflow validator v0.8.

The v0.8 compiler subset is intentionally allowlisted.
There is no raw shell task.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from validator_v0_3 import issue
from validator_v0_7 import validate_document as validate_v07


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
SAFE_BRANCH = re.compile(r"^[A-Za-z0-9_./-]+$")
SAFE_MODULE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")
SAFE_REL_PATH = re.compile(r"^[A-Za-z0-9_./-]+$")
SAFE_ARG = re.compile(r"^[A-Za-z0-9_./:@=+-]+$")
ALLOWED_RUNNERS = {"ubuntu-latest"}
ALLOWED_TRIGGERS = {"push", "workflow_dispatch"}
ALLOWED_TASKS = {"checkout", "setup_python", "python_module"}


def safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if value.startswith("/") or value.startswith("~"):
        return False
    if ".." in value.split("/"):
        return False
    return bool(SAFE_REL_PATH.fullmatch(value))


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    base = validate_v07(doc)
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

    if len(workflows) != 1:
        errors.append(issue("V065", "v0.8 compiler subset requires exactly one workflow"))
    else:
        w = workflows[0]
        sid = str(w.get("id"))
        name = w.get("name")
        runner = w.get("runner")
        trigger = w.get("trigger")
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            errors.append(issue("V065", "workflow name is unsafe or invalid", sid))
        if runner not in ALLOWED_RUNNERS:
            errors.append(issue("V065", "workflow runner is not allowlisted", sid))
        if trigger not in ALLOWED_TRIGGERS:
            errors.append(issue("V065", "workflow trigger is not allowlisted", sid))
        if trigger == "push":
            branch_name = w.get("branch")
            if not isinstance(branch_name, str) or not SAFE_BRANCH.fullmatch(branch_name):
                errors.append(issue("V065", "push workflow requires safe branch", sid))

    if not tasks:
        errors.append(issue("V066", "workflow must contain at least one task"))

    for task in tasks:
        sid = str(task.get("id"))
        opcode = task.get("task_kind")

        if opcode not in ALLOWED_TASKS:
            errors.append(issue("V066", f"task kind {opcode!r} is not allowlisted", sid))
            continue

        if opcode == "checkout":
            allowed = {"id", "kind", "task_kind"}
            extras = set(task) - allowed
            if extras:
                errors.append(issue("V067", "checkout task has unsupported fields", sid))

        elif opcode == "setup_python":
            version = task.get("version")
            if str(version) != "3.12":
                errors.append(issue("V067", "setup_python version is not allowlisted", sid))

        elif opcode == "python_module":
            module = task.get("module")
            if not isinstance(module, str) or not SAFE_MODULE.fullmatch(module):
                errors.append(issue("V067", "python_module module is invalid", sid))

            cwd = task.get("cwd")
            if cwd is not None and not safe_relative_path(cwd):
                errors.append(issue("V067", "python_module cwd is unsafe", sid))

            raw_args = task.get("args", "")
            if raw_args:
                if not isinstance(raw_args, str):
                    errors.append(issue("V067", "python_module args must be comma-separated text", sid))
                else:
                    for arg in raw_args.split(","):
                        if not arg or not SAFE_ARG.fullmatch(arg):
                            errors.append(issue("V067", f"unsafe python argument: {arg!r}", sid))

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
