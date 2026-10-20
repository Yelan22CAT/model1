#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.6.

v0.6 adds many-way conflict sets, reconciliation proposals,
quorum policies, independent votes, and finality certificates.
No new surface glyphs are introduced.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from parser_v0_2 import BridgeParseError
from parser_v0_3 import parse_kv_tokens
from parser_v0_5 import ParserV05


class ParserV06(ParserV05):
    def parse_evidence(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "conflict_set":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"members", "domain", "status"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Conflict set missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "conflict_set", **fields}

        if len(tokens) >= 3 and tokens[1] == "vote":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "voter",
                "proposal",
                "decision",
                "independence",
                "evidence_hash",
                "at",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Vote missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "vote", **fields}

        return super().parse_evidence(rest)

    def parse_guard(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "quorum":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"voters", "threshold", "independence_min"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Quorum missing required field(s): " + ", ".join(missing)
                )
            for field in ("threshold", "independence_min"):
                if not isinstance(fields[field], int) or isinstance(fields[field], bool):
                    raise BridgeParseError(f"Quorum {field} must be an integer")
            return {"id": sid, "kind": "quorum_policy", **fields}

        return super().parse_guard(rest)

    def parse_action(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "propose":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"conflict_set", "strategy", "result_hash", "at"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Proposal missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "reconciliation_proposal", **fields}

        return super().parse_action(rest)

    def parse_verification(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "certificate":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "proposal",
                "quorum",
                "votes",
                "issued_by",
                "term",
                "at",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Certificate missing required field(s): " + ", ".join(missing)
                )
            if not isinstance(fields["term"], int) or isinstance(fields["term"], bool):
                raise BridgeParseError("Certificate term must be an integer")
            return {"id": sid, "kind": "finality_certificate", **fields}

        return super().parse_verification(rest)


def parse_document(text: str) -> dict[str, Any]:
    parser = ParserV06()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.6",
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
