#!/usr/bin/env python3
"""Bridge-0 v0.5 parse + split-brain validate CLI."""

import json
import sys

from parser_v0_2 import BridgeParseError
from parser_v0_5 import parse_document
from validator_v0_5 import validate_document


def main() -> int:
    source = sys.stdin.read()
    try:
        doc = parse_document(source)
    except BridgeParseError as exc:
        print(json.dumps({"stage": "parse", "valid": False, "error": str(exc)}, indent=2))
        return 2

    result = validate_document(doc)
    print(json.dumps({"stage": "validate", "ir": doc, "validation": result}, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
