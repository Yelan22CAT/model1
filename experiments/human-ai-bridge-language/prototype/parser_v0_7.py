#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.7.

v0.7 adds identity, attestation, attestation revocation, and evidence
provenance records. No new glyphs are introduced.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from parser_v0_2 import BridgeParseError
from parser_v0_3 import parse_kv_tokens
from parser_v0_6 import ParserV06


class ParserV07(ParserV06):
    def parse_entity(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "identity":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "subject",
                "control_domain",
                "model_lineage",
                "runtime_origin",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Identity missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "identity", **fields}
        return super().parse_entity(rest)

    def parse_evidence(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "attest":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "identity",
                "issuer",
                "status",
                "valid_from",
                "valid_until",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Attestation missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "identity_attestation", **fields}

        if len(tokens) >= 3 and tokens[1] == "evidence_provenance":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "evidence_hash",
                "source_identity",
                "attestation",
                "origin",
                "parent",
                "at",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Evidence provenance missing required field(s): "
                    + ", ".join(missing)
                )
            return {"id": sid, "kind": "evidence_provenance", **fields}

        if len(tokens) >= 3 and tokens[1] == "vote":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "voter",
                "proposal",
                "decision",
                "independence",
                "evidence_hash",
                "identity",
                "attestation",
                "provenance",
                "at",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Attested vote missing required field(s): " + ", ".join(missing)
                )
            return {"id": sid, "kind": "vote", **fields}

        return super().parse_evidence(rest)

    def parse_guard(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "quorum":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "voters",
                "threshold",
                "independence_min",
                "evidence_min",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Attested quorum missing required field(s): " + ", ".join(missing)
                )
            for field in ("threshold", "independence_min", "evidence_min"):
                if not isinstance(fields[field], int) or isinstance(fields[field], bool):
                    raise BridgeParseError(f"Quorum {field} must be an integer")
            return {"id": sid, "kind": "quorum_policy", **fields}
        return super().parse_guard(rest)

    def parse_prohibition(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "revoke_attestation":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"target", "by", "at"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Attestation revocation missing required field(s): "
                    + ", ".join(missing)
                )
            return {"id": sid, "kind": "attestation_revocation", **fields}
        return super().parse_prohibition(rest)


def parse_document(text: str) -> dict[str, Any]:
    parser = ParserV07()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.7",
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
