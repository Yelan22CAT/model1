#!/usr/bin/env python3
"""Bridge-0 v0.3 parse + validate CLI."""

from __future__ import annotations

import json
import sys

from parser_v0_3 import BridgeParseError, parse_document
from validator_v0_3 import validate_document


def main() -> int:
    source = sys.stdin.read()
    try:
        doc = parse_document(source)
    except BridgeParseError as exc:
        print(json.dumps({"stage": "parse", "valid": False, "error": str(exc)}, indent=2))
        return 2

    result = validate_document(doc)
    print(
        json.dumps(
            {"stage": "validate", "ir": doc, "validation": result},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
