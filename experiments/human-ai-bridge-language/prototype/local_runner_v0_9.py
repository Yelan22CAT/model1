#!/usr/bin/env python3
"""Bridge-0 v0.9 local deterministic backend runner."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
from typing import Any

from parser_v0_9 import parse_document
from validator_v0_9 import validate_document


class LocalBackendError(RuntimeError):
    pass


def task_args(task: dict[str, Any]) -> list[str]:
    raw_args = task.get("args", "")
    return [] if not raw_args else str(raw_args).split(",")


def run_local(source_path: pathlib.Path) -> list[pathlib.Path]:
    doc = parse_document(source_path.read_text(encoding="utf-8"))
    result = validate_document(doc)
    if not result["valid"]:
        raise LocalBackendError(str(result["errors"]))

    repo_root = source_path.resolve().parents[2]
    outputs: list[pathlib.Path] = []

    for task in doc["statements"]:
        if task.get("kind") != "workflow_task":
            continue

        opcode = task["task_kind"]
        tid = str(task["id"])

        if opcode == "checkout":
            if not (repo_root / ".git").exists():
                raise LocalBackendError("local backend requires checked-out repository")

        elif opcode == "setup_python":
            required = str(task["version"])
            actual = f"{sys.version_info.major}.{sys.version_info.minor}"
            if actual != required:
                raise LocalBackendError(
                    f"Python version mismatch: required {required}, actual {actual}"
                )

        elif opcode == "python_module":
            cwd = repo_root
            if task.get("cwd"):
                cwd = repo_root / str(task["cwd"])

            command = [sys.executable, "-m", str(task["module"]), *task_args(task)]
            completed = subprocess.run(
                command,
                cwd=cwd,
                text=True,
                capture_output=True,
                check=False,
            )
            if completed.returncode != 0:
                raise LocalBackendError(
                    f"task {tid} failed rc={completed.returncode}: {completed.stderr}"
                )

            if task.get("observe") == "stdout":
                path = cwd / f".bridge-local-{tid}.stdout"
                path.write_text(completed.stdout, encoding="utf-8")
                outputs.append(path)

        else:
            raise LocalBackendError(f"unsupported local task: {opcode}")

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    args = parser.parse_args()

    try:
        outputs = run_local(pathlib.Path(args.source))
    except LocalBackendError as exc:
        print(f"LocalBackendError: {exc}", file=sys.stderr)
        return 2

    for path in outputs:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
