#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.11.

v0.11 introduces one language-neutral semantic compute task that can be
compiled into more than one implementation language.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from parser_v0_2 import BridgeParseError
from parser_v0_3 import parse_kv_tokens
from parser_v0_7 import ParserV07


class ParserV011(ParserV07):
    def parse_goal(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "program":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"name", "targets"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Program missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "program", **fields}
        return super().parse_goal(rest)

    def parse_action(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "compute":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"op", "values", "observe"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Compute missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "semantic_compute", **fields}
        return super().parse_action(rest)


def parse_document(text: str) -> dict[str, Any]:
    parser = ParserV011()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.11",
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
