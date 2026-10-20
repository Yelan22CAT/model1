#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.5.

v0.5 adds split-brain / concurrency records without adding new glyphs:
snapshot, conflict, merge, finality, execution.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from parser_v0_2 import BridgeParseError
from parser_v0_3 import parse_kv_tokens
from parser_v0_4 import ParserV04


class ParserV05(ParserV04):
    def parse_entity(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "snapshot":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"branch", "parent", "seq", "domain", "state_hash", "at"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Snapshot missing required field(s): " + ", ".join(missing)
                )
            if not isinstance(fields["seq"], int) or isinstance(fields["seq"], bool):
                raise BridgeParseError("Snapshot seq must be an integer")
            return {"id": sid, "kind": "snapshot", **fields}
        return super().parse_entity(rest)

    def parse_evidence(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "conflict":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"left", "right", "domain", "status"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Conflict missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "split_brain_conflict", **fields}
        return super().parse_evidence(rest)

    def parse_action(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "merge":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "left",
                "right",
                "conflict",
                "strategy",
                "result_hash",
                "at",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Merge missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "merge", **fields}

        if len(tokens) >= 3 and tokens[1] == "execute":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"actor", "action", "state", "finality", "at"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Execution missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "execution", **fields}

        return super().parse_action(rest)

    def parse_verification(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "final":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"target", "by", "term", "at"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Finality missing required field(s): " + ", ".join(missing)
                )
            if not isinstance(fields["term"], int) or isinstance(fields["term"], bool):
                raise BridgeParseError("Finality term must be an integer")
            return {"id": sid, "kind": "finality", **fields}
        return super().parse_verification(rest)


def parse_document(text: str) -> dict[str, Any]:
    parser = ParserV05()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.5",
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
