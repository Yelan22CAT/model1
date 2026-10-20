#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.9.

v0.9 keeps the v0.8 workflow grammar and adds compiler-facing
observable fields used for multi-backend equivalence tests.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from parser_v0_2 import BridgeParseError
from parser_v0_8 import ParserV08


def parse_document(text: str) -> dict[str, Any]:
    parser = ParserV08()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.9",
        "source_language": None,
        "labels": {},
        "statements": statements,
    }


def main() -> int:
    source = sys.stdin.read()
    try:
        doc = parse_document(source)
    except BridgeParseError as exc:
        print(f"BridgeParseError: {exc}", file=sys.stderr)
        return 2
    json.dump(doc, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
