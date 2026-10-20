#!/usr/bin/env python3
"""Bridge-0 v0.9 compiler to GitHub Actions with backend-equivalence harness."""

from __future__ import annotations

import sys
from typing import Any

from compiler_github_v0_8 import BridgeCompileError, yaml_quote
from validator_v0_9 import validate_document


def compile_github_actions(doc: dict[str, Any]) -> str:
    validation = validate_document(doc)
    if not validation["valid"]:
        messages = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in validation["errors"]
        )
        raise BridgeCompileError(messages)

    workflow = next(
        s for s in doc["statements"] if s.get("kind") == "workflow"
    )
    tasks = [
        s for s in doc["statements"] if s.get("kind") == "workflow_task"
    ]

    lines: list[str] = [
        f"name: {yaml_quote(str(workflow['name']))}",
        "",
        "on:",
    ]

    if workflow["trigger"] == "push":
        lines += [
            "  push:",
            "    branches:",
            f"      - {yaml_quote(str(workflow['branch']))}",
        ]
    else:
        lines.append("  workflow_dispatch:")

    lines += [
        "",
        "permissions:",
        "  contents: read",
        "",
        "jobs:",
        "  bridge_job:",
        f"    runs-on: {workflow['runner']}",
        "    steps:",
    ]

    observable_tasks: list[dict[str, Any]] = []

    for task in tasks:
        tid = str(task["id"])
        opcode = task["task_kind"]

        if opcode == "checkout":
            lines += [
                f"      - name: Bridge task {tid} checkout",
                "        uses: actions/checkout@v4",
            ]

        elif opcode == "setup_python":
            lines += [
                f"      - name: Bridge task {tid} setup Python",
                "        uses: actions/setup-python@v5",
                "        with:",
                f"          python-version: {yaml_quote(str(task['version']))}",
            ]

        elif opcode == "python_module":
            lines.append(f"      - name: Bridge task {tid} python module")
            cwd = task.get("cwd")
            if cwd:
                lines.append(f"        working-directory: {yaml_quote(str(cwd))}")

            command = ["python", "-m", str(task["module"])]
            raw_args = task.get("args", "")
            if raw_args:
                command.extend(str(raw_args).split(","))

            if task.get("observe") == "stdout":
                command.extend([">", f".bridge-github-{tid}.stdout"])
                observable_tasks.append(task)

            lines.append("        run: " + " ".join(command))

        else:
            raise BridgeCompileError(f"unsupported task: {opcode}")

    if observable_tasks:
        lines += [
            "      - name: Bridge local backend",
            "        working-directory: experiments/human-ai-bridge-language/prototype",
            "        run: python local_runner_v0_9.py ../executable_v0.9.bridge",
        ]

        for task in observable_tasks:
            tid = str(task["id"])
            cwd = str(task.get("cwd") or ".")
            lines += [
                f"      - name: Compare backend observable {tid}",
                f"        working-directory: {yaml_quote(cwd)}",
                "        run: "
                f"python compare_observables_v0_9.py "
                f".bridge-github-{tid}.stdout .bridge-local-{tid}.stdout",
            ]

    lines += [
        "",
        "# Generated from Bridge-0 v0.9. Do not hand-edit this artifact.",
    ]
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
