#!/usr/bin/env python3
"""Bridge-0 deterministic IR validator prototype v0.2.

The validator checks structural/semantic invariants that can be decided
without consulting a language model or the external world.

It does NOT establish real-world truth.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from typing import Any

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


def issue(rule: str, message: str, statement_id: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"rule": rule, "message": message}
    if statement_id is not None:
        out["statement_id"] = statement_id
    return out


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []

    if doc.get("language") != "Bridge-0":
        errors.append(issue("V000", "language must be Bridge-0"))

    statements = doc.get("statements")
    if not isinstance(statements, list):
        errors.append(issue("V000", "statements must be an array"))
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "conflicts": conflicts,
        }

    by_id: dict[str, dict[str, Any]] = {}

    # Pass 1: identity and local shape.
    for s in statements:
        if not isinstance(s, dict):
            errors.append(issue("V000", "each statement must be an object"))
            continue

        sid = s.get("id")
        kind = s.get("kind")

        if not isinstance(sid, str) or not sid:
            errors.append(issue("V001", "statement id is required"))
            continue

        if sid in by_id:
            errors.append(issue("V001", f"duplicate statement id [{sid}]", sid))
            continue

        by_id[sid] = s

        if kind == "unknown":
            if "value" in s:
                errors.append(issue("V003", "unknown must not carry a value", sid))

        if kind == "claim":
            state = s.get("epistemic_state")
            if state not in {"fact", "hypothesis"}:
                errors.append(
                    issue(
                        "V002",
                        "claim epistemic_state must be fact or hypothesis",
                        sid,
                    )
                )

            predicate = s.get("predicate")
            if predicate is not None:
                expected = RELATION_CLASSES.get(predicate)
                if expected is None:
                    errors.append(issue("V018", f"unknown relation: {predicate}", sid))
                elif s.get("relation_class") != expected:
                    errors.append(
                        issue(
                            "V008",
                            f"relation {predicate} must have class {expected}",
                            sid,
                        )
                    )

        if kind == "evidence":
            relation = s.get("relation")
            if relation not in {"supports", "opposes", "derived_from"}:
                errors.append(
                    issue("V008", f"invalid evidential relation: {relation}", sid)
                )
            if s.get("relation_class") != "evidential":
                errors.append(
                    issue("V008", "evidence relation_class must be evidential", sid)
                )

        if kind == "guard" and s.get("relation_class") != "normative":
            errors.append(
                issue("V008", "guard relation_class must be normative", sid)
            )

    # Pass 2: references.
    for sid, s in by_id.items():
        kind = s.get("kind")

        if kind == "evidence":
            target = s.get("target")
            if target not in by_id:
                errors.append(
                    issue("V004", f"evidence target [{target}] does not exist", sid)
                )

        if kind == "verification":
            target = s.get("target")
            if target not in by_id:
                errors.append(
                    issue("V012", f"verification target [{target}] does not exist", sid)
                )

        if kind == "claim":
            for field in ("subject", "object", "value"):
                value = s.get(field)
                if isinstance(value, dict) and "ref" in value:
                    ref = value["ref"]
                    if ref not in by_id:
                        errors.append(
                            issue(
                                "V004",
                                f"claim reference [{ref}] does not exist",
                                sid,
                            )
                        )

    # Pass 3: evidence conflict. Conflict is preserved, not resolved.
    evidence_by_target: dict[str, set[str]] = defaultdict(set)
    evidence_ids_by_target: dict[str, list[str]] = defaultdict(list)

    for sid, s in by_id.items():
        if s.get("kind") != "evidence":
            continue
        target = s.get("target")
        relation = s.get("relation")
        if isinstance(target, str) and isinstance(relation, str):
            evidence_by_target[target].add(relation)
            evidence_ids_by_target[target].append(sid)

    for target, relations in evidence_by_target.items():
        if "supports" in relations and "opposes" in relations:
            conflicts.append(
                {
                    "rule": "V007",
                    "target": target,
                    "evidence_ids": evidence_ids_by_target[target],
                    "message": "conflicting evidence preserved; no automatic resolution",
                }
            )

    # Pass 4: semantic warnings that are decidable from explicit IR only.
    # Meta-claims remain separate automatically because referenced claims are never mutated.
    for sid, s in by_id.items():
        if s.get("kind") == "claim" and s.get("predicate") == "asserted":
            obj = s.get("object")
            if isinstance(obj, dict) and "ref" in obj:
                warnings.append(
                    issue(
                        "V006",
                        f"meta-claim references [{obj['ref']}]; embedded claim state unchanged",
                        sid,
                    )
                )

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
                    "errors": [
                        {
                            "rule": "V000",
                            "message": f"invalid JSON: {exc.msg}",
                        }
                    ],
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
