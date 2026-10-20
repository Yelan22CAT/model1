#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.19.

v0.19 adds revocation and replay-resistance semantics for scoped authorization.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from parser_v0_2 import BridgeParseError
from parser_v0_3 import parse_kv_tokens
from parser_v0_7 import ParserV07


class ParserV019(ParserV07):
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
        if len(tokens) >= 3 and tokens[1] == "authorize_once":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "domain",
                "artifact",
                "route",
                "authorization_id",
                "nonce",
                "loss_ack",
                "authority",
                "scope",
                "artifact_digest",
                "provenance",
                "revocation_epoch",
                "usage",
                "issued_at",
                "expires_at",
                "evaluate_at",
                "observe",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Single-use authorization missing required field(s): "
                    + ", ".join(missing)
                )
            return {"id": sid, "kind": "single_use_authorization", **fields}
        return super().parse_action(rest)


def parse_document(text: str) -> dict[str, Any]:
    parser = ParserV019()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.19",
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
