#!/usr/bin/env python3
"""Cross-platform observable capture helper for Bridge-0 v0.10."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True)
    parser.add_argument("--cwd", default=".")
    parser.add_argument("--output", required=True)
    parser.add_argument("--arg", action="append", default=[])
    args = parser.parse_args()

    cwd = pathlib.Path(args.cwd)
    output = pathlib.Path(args.output)

    completed = subprocess.run(
        [sys.executable, "-m", args.module, *args.arg],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if completed.returncode != 0:
        sys.stderr.write(completed.stderr)
        return completed.returncode

    output.write_text(completed.stdout, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
