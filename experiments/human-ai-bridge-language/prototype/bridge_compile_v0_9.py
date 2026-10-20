#!/usr/bin/env python3
"""Compile Bridge-0 v0.9 source directly to GitHub Actions YAML."""

from __future__ import annotations

import sys

from compiler_github_v0_8 import BridgeCompileError
from compiler_github_v0_9 import compile_github_actions
from parser_v0_2 import BridgeParseError
from parser_v0_9 import parse_document


def main() -> int:
    source = sys.stdin.read()
    try:
        doc = parse_document(source)
        out = compile_github_actions(doc)
    except (BridgeParseError, BridgeCompileError) as exc:
        print(f"BridgeCompileError: {exc}", file=sys.stderr)
        return 2

    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
