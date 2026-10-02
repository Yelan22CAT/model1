#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.4.

v0.4 adds authority lifecycle events:
grant → delegate → revoke/expire → replay.
No new surface glyphs are introduced.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from parser_v0_2 import BridgeParseError
from parser_v0_3 import ParserV03, parse_kv_tokens


class ParserV04(ParserV03):
    def parse_guard(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "grant":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "grantor",
                "actor",
                "action",
                "resource",
                "scope",
                "at",
                "epoch",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Grant missing required field(s): " + ", ".join(missing)
                )
            if not isinstance(fields["epoch"], int) or isinstance(fields["epoch"], bool):
                raise BridgeParseError("Grant epoch must be an integer")
            return {"id": sid, "kind": "grant", **fields}

        return super().parse_guard(rest)

    def parse_action(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "delegate":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "parent",
                "from",
                "to",
                "action",
                "resource",
                "scope",
                "at",
                "epoch",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Delegation missing required field(s): " + ", ".join(missing)
                )
            if not isinstance(fields["epoch"], int) or isinstance(fields["epoch"], bool):
                raise BridgeParseError("Delegation epoch must be an integer")
            return {"id": sid, "kind": "delegation", **fields}

        if len(tokens) >= 3 and tokens[1] == "replay":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"target", "authority", "at", "epoch"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Replay missing required field(s): " + ", ".join(missing)
                )
            if not isinstance(fields["epoch"], int) or isinstance(fields["epoch"], bool):
                raise BridgeParseError("Replay epoch must be an integer")
            return {"id": sid, "kind": "replay", **fields}

        return super().parse_action(rest)

    def parse_prohibition(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "revoke":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"target", "by", "at", "epoch"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Revocation missing required field(s): " + ", ".join(missing)
                )
            if not isinstance(fields["epoch"], int) or isinstance(fields["epoch"], bool):
                raise BridgeParseError("Revocation epoch must be an integer")
            return {"id": sid, "kind": "revocation", **fields}

        return super().parse_prohibition(rest)


def parse_document(text: str) -> dict[str, Any]:
    parser = ParserV04()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.4",
        "source_language": None,
        "labels": {},
        "statements": statements,
    }


def main() -> int:
    text = sys.stdin.read()
    try:
        doc = parse_document(text)
    except BridgeParseError as exc:
        print(f"BridgeParseError: {exc}", file=sys.stderr)
        return 2

    json.dump(doc, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
