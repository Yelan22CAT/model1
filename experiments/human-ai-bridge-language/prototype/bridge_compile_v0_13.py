#!/usr/bin/env python3
"""Compile Bridge-0 v0.13 floating semantics to Python or Node.js."""

from __future__ import annotations

import argparse
import sys

from compiler_float_v0_13 import BridgeFloatCompileError, compile_target
from parser_v0_2 import BridgeParseError
from parser_v0_13 import parse_document


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, choices=["python312", "node20"])
    args = parser.parse_args()

    try:
        doc = parse_document(sys.stdin.read())
        sys.stdout.write(compile_target(doc, args.target))
    except (BridgeParseError, BridgeFloatCompileError) as exc:
        print(f"BridgeCompileError: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
