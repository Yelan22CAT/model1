#!/usr/bin/env python3
"""Bridge-0 v0.8 compiler: canonical IR -> GitHub Actions YAML.

The compiler is intentionally narrow:
- one workflow;
- ubuntu-latest;
- push or workflow_dispatch;
- allowlisted tasks only;
- no raw shell task;
- no arbitrary GitHub Action references.

This is a source-language experiment, not a production compiler.
"""

from __future__ import annotations

import sys
from typing import Any

from validator_v0_8 import validate_document


class BridgeCompileError(ValueError):
    pass


def yaml_quote(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def compile_github_actions(doc: dict[str, Any]) -> str:
    validation = validate_document(doc)
    if not validation["valid"]:
        messages = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in validation["errors"]
        )
        raise BridgeCompileError(messages)

    workflow = next(
        s for s in doc["statements"]
        if s.get("kind") == "workflow"
    )
    tasks = [
        s for s in doc["statements"]
        if s.get("kind") == "workflow_task"
    ]

    lines: list[str] = []
    lines.append(f"name: {yaml_quote(str(workflow['name']))}")
    lines.append("")
    lines.append("on:")

    trigger = workflow["trigger"]
    if trigger == "workflow_dispatch":
        lines.append("  workflow_dispatch:")
    elif trigger == "push":
        lines.append("  push:")
        lines.append("    branches:")
        lines.append(f"      - {yaml_quote(str(workflow['branch']))}")
    else:
        raise BridgeCompileError(f"Unsupported trigger after validation: {trigger}")

    lines.append("")
    lines.append("permissions:")
    lines.append("  contents: read")
    lines.append("")
    lines.append("jobs:")
    lines.append("  bridge_job:")
    lines.append(f"    runs-on: {workflow['runner']}")
    lines.append("    steps:")

    for task in tasks:
        tid = str(task["id"])
        opcode = task["task_kind"]

        if opcode == "checkout":
            lines.append(f"      - name: Bridge task {tid} checkout")
            lines.append("        uses: actions/checkout@v4")

        elif opcode == "setup_python":
            lines.append(f"      - name: Bridge task {tid} setup Python")
            lines.append("        uses: actions/setup-python@v5")
            lines.append("        with:")
            lines.append(f"          python-version: {yaml_quote(str(task['version']))}")

        elif opcode == "python_module":
            lines.append(f"      - name: Bridge task {tid} python module")
            cwd = task.get("cwd")
            if cwd is not None:
                lines.append(f"        working-directory: {yaml_quote(str(cwd))}")

            command = ["python", "-m", str(task["module"])]
            raw_args = task.get("args", "")
            if raw_args:
                command.extend(str(raw_args).split(","))
            lines.append("        run: " + " ".join(command))

        else:
            raise BridgeCompileError(f"Unsupported task after validation: {opcode}")

    lines.append("")
    lines.append("# Generated from Bridge-0 v0.8. Do not hand-edit this artifact.")
    return "\n".join(lines) + "\n"


def main() -> int:
    import json

    try:
        doc = json.load(sys.stdin)
        output = compile_github_actions(doc)
    except (json.JSONDecodeError, BridgeCompileError) as exc:
        print(f"BridgeCompileError: {exc}", file=sys.stderr)
        return 2

    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
