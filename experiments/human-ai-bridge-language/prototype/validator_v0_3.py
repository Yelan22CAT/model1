#!/usr/bin/env python3
"""Bridge-0 deterministic validator prototype v0.3.

Extends v0.2 checks with structured authority, handoff, transition,
provenance, and validity-window semantics.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from typing import Any

from validator_v0_2 import issue, validate_document as validate_v02


def parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def ref_id(value: Any) -> str | None:
    if isinstance(value, dict) and set(value) == {"ref"}:
        ref = value.get("ref")
        return ref if isinstance(ref, str) else None
    return None


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    base = validate_v02(doc)
    errors = list(base["errors"])
    warnings = list(base["warnings"])
    conflicts = list(base["conflicts"])

    statements = doc.get("statements")
    if not isinstance(statements, list):
        return base

    by_id = {
        s.get("id"): s
        for s in statements
        if isinstance(s, dict) and isinstance(s.get("id"), str)
    }

    provenance_edges: dict[str, str] = {}

    for s in statements:
        if not isinstance(s, dict):
            continue
        sid = s.get("id")
        kind = s.get("kind")

        if kind == "permission":
            required = ("actor", "action", "resource", "scope")
            missing = [k for k in required if not s.get(k)]
            if missing:
                errors.append(
                    issue(
                        "V019",
                        "permission tuple missing: " + ", ".join(missing),
                        sid,
                    )
                )

            if "valid_from" in s and "valid_until" in s:
                try:
                    start = parse_time(str(s["valid_from"]))
                    end = parse_time(str(s["valid_until"]))
                    if start > end:
                        errors.append(
                            issue(
                                "V020",
                                "permission valid_from is after valid_until",
                                sid,
                            )
                        )
                except ValueError:
                    errors.append(
                        issue("V020", "invalid permission validity timestamp", sid)
                    )

        elif kind == "handoff":
            artifact = ref_id(s.get("artifact"))
            if artifact is None or artifact not in by_id:
                errors.append(
                    issue("V021", "handoff artifact reference is missing or unknown", sid)
                )

            if s.get("state") != "preserve":
                errors.append(
                    issue(
                        "V022",
                        "handoff must preserve epistemic state in v0.3",
                        sid,
                    )
                )

            if s.get("provenance") != "preserve":
                errors.append(
                    issue(
                        "V022",
                        "handoff must preserve provenance in v0.3",
                        sid,
                    )
                )

            if not s.get("from") or not s.get("to") or not s.get("scope"):
                errors.append(
                    issue(
                        "V021",
                        "handoff requires from, to, and scope",
                        sid,
                    )
                )

        elif kind == "state_transition":
            irreversible = s.get("irreversible")
            if not isinstance(irreversible, bool):
                errors.append(
                    issue("V023", "transition irreversible must be boolean", sid)
                )
            if irreversible:
                guard = ref_id(s.get("when"))
                if guard is None or guard not in by_id:
                    errors.append(
                        issue(
                            "V023",
                            "irreversible transition requires an existing guard reference",
                            sid,
                        )
                    )
                elif by_id[guard].get("kind") != "guard":
                    errors.append(
                        issue(
                            "V023",
                            "transition 'when' reference must target a guard",
                            sid,
                        )
                    )

                if not s.get("authority"):
                    errors.append(
                        issue(
                            "V023",
                            "irreversible transition requires explicit authority",
                            sid,
                        )
                    )

        elif kind == "provenance":
            artifact = ref_id(s.get("artifact"))
            parent = ref_id(s.get("parent"))

            if artifact is None or artifact not in by_id:
                errors.append(
                    issue("V024", "provenance artifact reference is missing or unknown", sid)
                )
            if parent is None or parent not in by_id:
                errors.append(
                    issue("V024", "provenance parent reference is missing or unknown", sid)
                )
            if artifact is not None and parent is not None:
                provenance_edges[artifact] = parent

            if not s.get("actor") or not s.get("transform"):
                errors.append(
                    issue(
                        "V024",
                        "provenance requires actor and transform",
                        sid,
                    )
                )

    # Detect cycles in artifact → parent provenance edges.
    for start in list(provenance_edges):
        seen: set[str] = set()
        node = start
        while node in provenance_edges:
            if node in seen:
                errors.append(
                    issue(
                        "V025",
                        f"provenance cycle detected at [{node}]",
                    )
                )
                break
            seen.add(node)
            node = provenance_edges[node]

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
    }


def main() -> int:
    try:
        doc = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(
            json.dumps(
                {
                    "valid": False,
                    "errors": [{"rule": "V000", "message": f"invalid JSON: {exc.msg}"}],
                    "warnings": [],
                    "conflicts": [],
                },
                indent=2,
            )
        )
        return 2

    result = validate_document(doc)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
