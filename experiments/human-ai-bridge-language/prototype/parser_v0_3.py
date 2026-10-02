#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.3.

v0.3 extends v0.2 with structured permission, handoff, state-transition,
and provenance records while preserving the same fail-closed parsing rule.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from parser_v0_2 import (
    BridgeParseError,
    Parser,
    parse_scalar,
    strip_id,
)


def parse_kv_atom(raw: str) -> Any:
    if raw.startswith("[") and raw.endswith("]"):
        return {"ref": strip_id(raw)}
    if raw in {"true", "false"}:
        return raw == "true"
    if re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
        return float(raw) if "." in raw else int(raw)
    if raw.startswith('"') and raw.endswith('"'):
        return parse_scalar(raw)
    return raw


def parse_kv_tokens(tokens: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for token in tokens:
        if "=" not in token:
            raise BridgeParseError(f"Expected key=value token: {token}")
        key, raw = token.split("=", 1)
        if not key or not raw:
            raise BridgeParseError(f"Malformed key=value token: {token}")
        if key in out:
            raise BridgeParseError(f"Duplicate key: {key}")
        out[key] = parse_kv_atom(raw)
    return out


class ParserV03(Parser):
    def parse_evidence(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "provenance":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"artifact", "parent", "actor", "transform"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Provenance missing required field(s): " + ", ".join(missing)
                )
            return {
                "id": sid,
                "kind": "provenance",
                **fields,
            }
        return super().parse_evidence(rest)

    def parse_guard(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) >= 3 and tokens[1] == "permission":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"actor", "action", "resource", "scope"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Permission missing required field(s): " + ", ".join(missing)
                )
            return {
                "id": sid,
                "kind": "permission",
                **fields,
            }
        return super().parse_guard(rest)

    def parse_action(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()

        if len(tokens) >= 3 and tokens[1] == "handoff":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {
                "from",
                "to",
                "artifact",
                "scope",
                "state",
                "provenance",
            }
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Handoff missing required field(s): " + ", ".join(missing)
                )
            return {
                "id": sid,
                "kind": "handoff",
                **fields,
            }

        if len(tokens) >= 3 and tokens[1] == "transition":
            sid = self.claim_id(tokens[0])
            fields = parse_kv_tokens(tokens[2:])
            required = {"subject", "from", "to", "irreversible"}
            missing = sorted(required - set(fields))
            if missing:
                raise BridgeParseError(
                    "Transition missing required field(s): " + ", ".join(missing)
                )
            if not isinstance(fields["irreversible"], bool):
                raise BridgeParseError("Transition irreversible must be true or false")
            return {
                "id": sid,
                "kind": "state_transition",
                **fields,
            }

        return super().parse_action(rest)


def parse_document(text: str) -> dict[str, Any]:
    parser = ParserV03()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.3",
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
