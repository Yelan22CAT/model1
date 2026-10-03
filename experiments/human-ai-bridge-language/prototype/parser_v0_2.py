#!/usr/bin/env python3
"""Bridge-0 restricted parser prototype v0.2.

This parser intentionally accepts only a small deterministic subset.
It MUST reject unsupported syntax rather than guessing intent.

No external dependencies.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from typing import Any

ID_RE = r"\[(?P<id>[A-Za-z0-9_-]+)\]"
IDENT = r"[A-Za-z_][A-Za-z0-9_-]*"
PATH = rf"{IDENT}(?:\.{IDENT})*"

RELATION_CLASSES = {
    "supports": "evidential",
    "opposes": "evidential",
    "derived_from": "evidential",
    "supersedes": "temporal",
    "precedes": "temporal",
    "follows": "temporal",
    "causes": "causal",
    "contributes_to": "causal",
    "prevents": "causal",
    "associated_with": "descriptive",
    "contains": "descriptive",
    "depends_on": "descriptive",
    "asserted": "descriptive",
    "requires": "normative",
    "allows": "normative",
    "forbids": "normative",
    "owned_by": "authority",
    "approval_by": "authority",
}

EVIDENTIAL = {"supports", "opposes", "derived_from"}
NORMATIVE = {"requires", "allows", "forbids"}

class BridgeParseError(ValueError):
    pass


def strip_id(token: str) -> str:
    if not (token.startswith("[") and token.endswith("]")):
        raise BridgeParseError(f"Invalid reference id: {token}")
    value = token[1:-1]
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise BridgeParseError(f"Invalid reference id: {token}")
    return value


def parse_scalar(raw: str) -> Any:
    raw = raw.strip()

    if raw == "?":
        raise BridgeParseError(
            "UNKNOWN cannot be used as a value. "
            "Use '? [ID] path' instead."
        )

    if raw == "true":
        return True
    if raw == "false":
        return False

    if re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
        return float(raw) if "." in raw else int(raw)

    if raw.startswith('"') and raw.endswith('"') and len(raw) >= 2:
        return raw[1:-1]

    if re.fullmatch(IDENT, raw):
        return raw

    if re.fullmatch(ID_RE, raw):
        return {"ref": strip_id(raw)}

    raise BridgeParseError(f"Unsupported value: {raw}")


def parse_value_and_unit(raw: str) -> tuple[Any, str | None]:
    raw = raw.strip()

    # Quoted strings are never split into value + unit.
    if raw.startswith('"'):
        return parse_scalar(raw), None

    parts = raw.split()
    if len(parts) == 1:
        return parse_scalar(parts[0]), None
    if len(parts) == 2:
        value = parse_scalar(parts[0])
        unit = parts[1]
        if not re.fullmatch(r"[A-Za-z%°/_-][A-Za-z0-9%°/_-]*", unit):
            raise BridgeParseError(f"Invalid unit: {unit}")
        return value, unit

    raise BridgeParseError(f"Ambiguous value/unit sequence: {raw}")


@dataclass
class Parser:
    seen_ids: set[str]

    def __init__(self) -> None:
        self.seen_ids = set()

    def claim_id(self, raw: str) -> str:
        value = strip_id(raw)
        if value in self.seen_ids:
            raise BridgeParseError(f"Duplicate statement id: [{value}]")
        self.seen_ids.add(value)
        return value

    def parse_line(self, line: str, line_number: int) -> dict[str, Any] | None:
        source = line.strip()
        if not source or source.startswith("#"):
            return None

        marker = source[0]
        rest = source[1:].strip()

        try:
            if marker == "○":
                return self.parse_entity(rest)
            if marker in {"■", "△"}:
                return self.parse_claim(rest, marker)
            if marker == "?":
                return self.parse_unknown(rest)
            if marker == "◆":
                return self.parse_evidence(rest)
            if marker == "!":
                return self.parse_guard(rest)
            if marker == "⊙":
                return self.parse_goal(rest)
            if marker == "→":
                return self.parse_action(rest)
            if marker == "✓":
                return self.parse_verification(rest)
            if marker == "×":
                return self.parse_prohibition(rest)
            if marker == "⏱":
                return self.parse_time(rest)
        except BridgeParseError as exc:
            raise BridgeParseError(f"line {line_number}: {exc}") from exc

        raise BridgeParseError(f"line {line_number}: unknown marker {marker!r}")

    def parse_entity(self, rest: str) -> dict[str, Any]:
        m = re.fullmatch(rf"({ID_RE})\s+({IDENT})", rest)
        if not m:
            raise BridgeParseError("Invalid entity declaration")
        sid = self.claim_id(m.group(1))
        name = m.group(m.lastindex)
        return {"id": sid, "kind": "entity", "name": name}

    def parse_claim(self, rest: str, marker: str) -> dict[str, Any]:
        epistemic = "fact" if marker == "■" else "hypothesis"

        m_assign = re.fullmatch(rf"({ID_RE})\s+({PATH})\s*=\s*(.+)", rest)
        if m_assign:
            sid = self.claim_id(m_assign.group(1))
            path = m_assign.group(m_assign.lastindex - 1)
            raw_value = m_assign.group(m_assign.lastindex)
            value, unit = parse_value_and_unit(raw_value)
            return {
                "id": sid,
                "kind": "claim",
                "epistemic_state": epistemic,
                "path": path,
                "operator": "=",
                "value": value,
                "unit": unit,
                "relation_class": None,
            }

        tokens = rest.split()
        if len(tokens) != 4:
            raise BridgeParseError(
                "Claim must be assignment or '<ID> TERM RELATION TERM'"
            )

        sid = self.claim_id(tokens[0])
        subject, relation, obj = tokens[1], tokens[2], tokens[3]
        if relation not in RELATION_CLASSES:
            raise BridgeParseError(f"Unknown relation: {relation}")

        return {
            "id": sid,
            "kind": "claim",
            "epistemic_state": epistemic,
            "subject": normalize_term(subject),
            "predicate": relation,
            "object": normalize_term(obj),
            "relation_class": RELATION_CLASSES[relation],
        }

    def parse_unknown(self, rest: str) -> dict[str, Any]:
        m = re.fullmatch(rf"({ID_RE})\s+({PATH})", rest)
        if not m:
            raise BridgeParseError("Unknown must be '? [ID] path' with no value")
        sid = self.claim_id(m.group(1))
        path = m.group(m.lastindex)
        return {"id": sid, "kind": "unknown", "path": path}

    def parse_evidence(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) != 4:
            raise BridgeParseError(
                "Evidence must be '◆ [ID] SOURCE supports|opposes|derived_from [TARGET]'"
            )
        sid = self.claim_id(tokens[0])
        source, relation, target_raw = tokens[1], tokens[2], tokens[3]
        if relation not in EVIDENTIAL:
            raise BridgeParseError(f"Invalid evidential relation: {relation}")
        target = strip_id(target_raw)
        return {
            "id": sid,
            "kind": "evidence",
            "source": source,
            "relation": relation,
            "relation_class": "evidential",
            "target": target,
        }

    def parse_guard(self, rest: str) -> dict[str, Any]:
        m = re.fullmatch(
            rf"({ID_RE})\s+(.+?)\s+(requires|allows|forbids)\s+(.+)",
            rest,
        )
        if not m:
            raise BridgeParseError(
                "Guard must be '! [ID] ACTION requires|allows|forbids CONDITION'"
            )
        sid = self.claim_id(m.group(1))
        action = m.group(m.lastindex - 2).strip()
        relation = m.group(m.lastindex - 1)
        condition = m.group(m.lastindex).strip()
        if not action or not condition:
            raise BridgeParseError("Guard action and condition cannot be empty")
        return {
            "id": sid,
            "kind": "guard",
            "action": action,
            "relation": relation,
            "relation_class": "normative",
            "condition": condition,
        }

    def parse_goal(self, rest: str) -> dict[str, Any]:
        m = re.fullmatch(rf"({ID_RE})\s+(.+)", rest)
        if not m:
            raise BridgeParseError("Goal must be '⊙ [ID] expression'")
        sid = self.claim_id(m.group(1))
        expr = m.group(m.lastindex).strip()
        return {"id": sid, "kind": "goal", "expression": expr}

    def parse_action(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) not in {3, 4}:
            raise BridgeParseError(
                "Action must be '→ [ID] ACTOR ACTION [OBJECT]'"
            )
        sid = self.claim_id(tokens[0])
        actor, action = tokens[1], tokens[2]
        obj = tokens[3] if len(tokens) == 4 else None
        return {
            "id": sid,
            "kind": "action",
            "actor": actor,
            "action": action,
            "object": obj,
        }

    def parse_verification(self, rest: str) -> dict[str, Any]:
        tokens = rest.split()
        if len(tokens) != 4 or tokens[2] != "verified_by":
            raise BridgeParseError(
                "Verification must be '✓ [ID] [TARGET] verified_by METHOD'"
            )
        sid = self.claim_id(tokens[0])
        target = strip_id(tokens[1])
        method = tokens[3]
        return {
            "id": sid,
            "kind": "verification",
            "target": target,
            "method": method,
        }

    def parse_prohibition(self, rest: str) -> dict[str, Any]:
        m = re.fullmatch(rf"({ID_RE})\s+(.+)", rest)
        if not m:
            raise BridgeParseError("Prohibition must be '× [ID] expression'")
        sid = self.claim_id(m.group(1))
        expr = m.group(m.lastindex).strip()
        return {"id": sid, "kind": "prohibition", "expression": expr}

    def parse_time(self, rest: str) -> dict[str, Any]:
        m = re.fullmatch(rf"({ID_RE})\s+({PATH})\s*=\s*(\S+)", rest)
        if not m:
            raise BridgeParseError(
                "Time must be '⏱ [ID] path = ISO-8601-timestamp'"
            )
        sid = self.claim_id(m.group(1))
        path = m.group(m.lastindex - 1)
        timestamp = m.group(m.lastindex)
        if not looks_like_iso8601(timestamp):
            raise BridgeParseError(f"Invalid timestamp: {timestamp}")
        return {
            "id": sid,
            "kind": "time_binding",
            "path": path,
            "timestamp": timestamp,
        }


def normalize_term(token: str) -> Any:
    if token.startswith("[") and token.endswith("]"):
        return {"ref": strip_id(token)}
    if re.fullmatch(PATH, token):
        return token
    if token.startswith('"') and token.endswith('"'):
        return token[1:-1]
    if re.fullmatch(r"-?\d+(?:\.\d+)?", token):
        return float(token) if "." in token else int(token)
    raise BridgeParseError(f"Unsupported term: {token}")


def looks_like_iso8601(value: str) -> bool:
    return bool(
        re.fullmatch(
            r"\d{4}-\d{2}-\d{2}"
            r"(?:T\d{2}:\d{2}:\d{2}"
            r"(?:Z|[+-]\d{2}:\d{2})?)?",
            value,
        )
    )


def parse_document(text: str) -> dict[str, Any]:
    parser = Parser()
    statements: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        item = parser.parse_line(line, line_number)
        if item is not None:
            statements.append(item)
    return {
        "language": "Bridge-0",
        "version": "0.2",
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
