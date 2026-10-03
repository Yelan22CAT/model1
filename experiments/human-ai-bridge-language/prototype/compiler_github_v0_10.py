#!/usr/bin/env python3
"""Bridge-0 v0.10 compiler to a heterogeneous GitHub Actions matrix.

The compiler emits one backend job per declared target and a separate
comparison job for typed JSON observables.
"""

from __future__ import annotations

import re
import sys
from typing import Any

from compiler_github_v0_8 import BridgeCompileError, yaml_quote
from validator_v0_10 import csv_values, validate_document


CAPTURE_HELPER = (
    "experiments/human-ai-bridge-language/prototype/"
    "backend_capture_v0_10.py"
)
COMPARATOR = (
    "experiments/human-ai-bridge-language/prototype/"
    "compare_typed_observables_v0_10.py"
)


def job_key(target: str) -> str:
    return "backend_" + re.sub(r"[^A-Za-z0-9_]", "_", target)


def observable_filename(task_id: str) -> str:
    return f"bridge-v010-{task_id}.json"


def python_command(task: dict[str, Any]) -> list[str]:
    command = ["python", "-m", str(task["module"])]
    raw_args = task.get("args", "")
    if raw_args:
        command.extend(str(raw_args).split(","))
    return command


def capture_command(task: dict[str, Any]) -> list[str]:
    tid = str(task["id"])
    command = [
        "python",
        CAPTURE_HELPER,
        "--module",
        str(task["module"]),
        "--output",
        observable_filename(tid),
    ]
    if task.get("cwd"):
        command.extend(["--cwd", str(task["cwd"])])
    raw_args = task.get("args", "")
    if raw_args:
        for arg in str(raw_args).split(","):
            command.append(f"--arg={arg}")
    return command


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
    targets = csv_values(workflow["targets"])
    observable_tasks = [
        t for t in tasks if t.get("observe") == "json_value"
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
    ]

    for target in targets:
        key = job_key(target)
        lines += [
            f"  {key}:",
            f"    runs-on: {target}",
            "    steps:",
        ]

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
                if task.get("observe") == "json_value":
                    lines.append("        run: " + " ".join(capture_command(task)))
                else:
                    if task.get("cwd"):
                        lines.append(
                            f"        working-directory: {yaml_quote(str(task['cwd']))}"
                        )
                    lines.append("        run: " + " ".join(python_command(task)))

            else:
                raise BridgeCompileError(f"unsupported task: {opcode}")

        if observable_tasks:
            artifact_name = f"bridge-v010-{target}"
            paths = "\n".join(
                f"            {observable_filename(str(task['id']))}"
                for task in observable_tasks
            )
            lines += [
                f"      - name: Upload Bridge observables for {target}",
                "        uses: actions/upload-artifact@v4",
                "        with:",
                f"          name: {yaml_quote(artifact_name)}",
                "          path: |",
                paths,
                "          if-no-files-found: error",
            ]

    compare_needs = ", ".join(job_key(target) for target in targets)
    lines += [
        "  compare_backends:",
        f"    needs: [{compare_needs}]",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - name: Checkout",
        "        uses: actions/checkout@v4",
        "      - name: Set up Python",
        "        uses: actions/setup-python@v5",
        "        with:",
        "          python-version: '3.12'",
    ]

    for target in targets:
        lines += [
            f"      - name: Download observables from {target}",
            "        uses: actions/download-artifact@v4",
            "        with:",
            f"          name: {yaml_quote(f'bridge-v010-{target}')}",
            f"          path: {yaml_quote(f'artifacts/{target}')}",
        ]

    for task in observable_tasks:
        tid = str(task["id"])
        paths = " ".join(
            f"artifacts/{target}/{observable_filename(tid)}"
            for target in targets
        )
        lines += [
            f"      - name: Compare typed observable {tid}",
            f"        run: python {COMPARATOR} {paths}",
        ]

    lines += [
        "",
        "# Generated from Bridge-0 v0.10. Do not hand-edit this artifact.",
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
