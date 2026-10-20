#!/usr/bin/env python3
"""Compile Bridge-0 v0.12 exact-integer source to Python or Node.js."""

from __future__ import annotations

import argparse
import sys

from compiler_exact_integer_v0_12 import (
    BridgeExactIntegerCompileError,
    compile_target,
)
from parser_v0_2 import BridgeParseError
from parser_v0_12 import parse_document


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, choices=["python312", "node20"])
    args = parser.parse_args()

    try:
        doc = parse_document(sys.stdin.read())
        sys.stdout.write(compile_target(doc, args.target))
    except (BridgeParseError, BridgeExactIntegerCompileError) as exc:
        print(f"BridgeCompileError: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
