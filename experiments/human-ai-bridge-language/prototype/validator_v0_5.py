#!/usr/bin/env python3
"""Bridge-0 split-brain / concurrency validator v0.5."""

from __future__ import annotations

import json
import sys
from itertools import combinations
from typing import Any

from authority_engine_v0_4 import build_index
from validator_v0_3 import issue, parse_time, ref_id
from validator_v0_4 import validate_document as validate_v04


def statement_time(statement: dict[str, Any]):
    raw = statement.get("at")
    if not isinstance(raw, str):
        return None
    try:
        return parse_time(raw)
    except ValueError:
        return None


def snapshot_parent_id(snapshot: dict[str, Any]) -> str | None:
    parent = snapshot.get("parent")
    if parent == "none":
        return None
    return ref_id(parent)


def pair_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def validate_document(
    doc: dict[str, Any],
    expected_epoch: int | None = None,
    trusted_finalizer: str = "control_plane",
) -> dict[str, Any]:
    base = validate_v04(doc, expected_epoch=expected_epoch)
    errors = list(base["errors"])
    warnings = list(base["warnings"])
    conflicts = list(base["conflicts"])

    statements = doc.get("statements")
    if not isinstance(statements, list):
        return base

    by_id = build_index(doc)
    snapshots: list[dict[str, Any]] = []

    # Local shape and reference checks.
    for s in statements:
        if not isinstance(s, dict):
            continue
        sid = s.get("id")
        kind = s.get("kind")

        if kind == "snapshot":
            snapshots.append(s)
            if not isinstance(s.get("seq"), int) or isinstance(s.get("seq"), bool) or s["seq"] < 0:
                errors.append(issue("V035", "snapshot seq must be a non-negative integer", sid))
            if not s.get("branch") or not s.get("domain") or not s.get("state_hash"):
                errors.append(issue("V035", "snapshot requires branch, domain, and state_hash", sid))
            when = statement_time(s)
            if when is None:
                errors.append(issue("V035", "snapshot requires a valid at timestamp", sid))

            parent = s.get("parent")
            if parent != "none":
                parent_id = ref_id(parent)
                parent_obj = by_id.get(parent_id) if parent_id else None
                if parent_obj is None or parent_obj.get("kind") != "snapshot":
                    errors.append(issue("V035", "snapshot parent must reference an existing snapshot", sid))
                else:
                    if s.get("domain") != parent_obj.get("domain"):
                        errors.append(issue("V035", "snapshot domain must match parent domain", sid))
                    if isinstance(s.get("seq"), int) and isinstance(parent_obj.get("seq"), int):
                        if s["seq"] != parent_obj["seq"] + 1:
                            errors.append(issue("V035", "snapshot seq must equal parent seq + 1", sid))
                    child_time = statement_time(s)
                    parent_time = statement_time(parent_obj)
                    if child_time is not None and parent_time is not None and child_time < parent_time:
                        errors.append(issue("V035", "snapshot time cannot precede parent snapshot", sid))

        elif kind == "split_brain_conflict":
            left = ref_id(s.get("left"))
            right = ref_id(s.get("right"))
            left_obj = by_id.get(left) if left else None
            right_obj = by_id.get(right) if right else None
            if left_obj is None or right_obj is None:
                errors.append(issue("V037", "conflict references must exist", sid))
                continue
            if left_obj.get("kind") != "snapshot" or right_obj.get("kind") != "snapshot":
                errors.append(issue("V037", "conflict must reference snapshots", sid))
                continue
            if left == right:
                errors.append(issue("V037", "conflict requires two distinct snapshots", sid))
            if s.get("status") != "open":
                errors.append(issue("V037", "v0.5 conflict status must be open", sid))
            if s.get("domain") != left_obj.get("domain") or s.get("domain") != right_obj.get("domain"):
                errors.append(issue("V037", "conflict domain must match both snapshots", sid))

        elif kind == "merge":
            left = ref_id(s.get("left"))
            right = ref_id(s.get("right"))
            conflict_id = ref_id(s.get("conflict"))
            left_obj = by_id.get(left) if left else None
            right_obj = by_id.get(right) if right else None
            conflict_obj = by_id.get(conflict_id) if conflict_id else None

            if left_obj is None or right_obj is None:
                errors.append(issue("V038", "merge parents must exist", sid))
                continue
            if left_obj.get("kind") != "snapshot" or right_obj.get("kind") != "snapshot":
                errors.append(issue("V038", "merge parents must be snapshots", sid))
            if conflict_obj is None or conflict_obj.get("kind") != "split_brain_conflict":
                errors.append(issue("V038", "merge requires a declared conflict", sid))
            else:
                conflict_pair = pair_key(
                    ref_id(conflict_obj.get("left")) or "",
                    ref_id(conflict_obj.get("right")) or "",
                )
                if conflict_pair != pair_key(left or "", right or ""):
                    errors.append(issue("V038", "merge conflict does not match merge parents", sid))

            if s.get("strategy") != "explicit":
                errors.append(issue("V039", "automatic/last-writer merge is forbidden in v0.5", sid))
            if not s.get("result_hash"):
                errors.append(issue("V038", "merge requires result_hash", sid))

            merge_time = statement_time(s)
            if merge_time is None:
                errors.append(issue("V038", "merge requires a valid at timestamp", sid))
            else:
                for parent_obj in (left_obj, right_obj):
                    parent_time = statement_time(parent_obj)
                    if parent_time is not None and merge_time < parent_time:
                        errors.append(issue("V038", "merge cannot precede parent snapshot", sid))

        elif kind == "finality":
            target = ref_id(s.get("target"))
            target_obj = by_id.get(target) if target else None
            if target_obj is None or target_obj.get("kind") not in {"snapshot", "merge"}:
                errors.append(issue("V040", "finality target must be a snapshot or merge", sid))
            if s.get("by") != trusted_finalizer:
                errors.append(issue("V040", "finality issuer is not the trusted finalizer", sid))
            term = s.get("term")
            if not isinstance(term, int) or isinstance(term, bool) or term <= 0:
                errors.append(issue("V043", "finality term must be a positive integer", sid))
            if statement_time(s) is None:
                errors.append(issue("V043", "finality requires a valid at timestamp", sid))

        elif kind == "execution":
            state = ref_id(s.get("state"))
            finality = ref_id(s.get("finality"))
            state_obj = by_id.get(state) if state else None
            finality_obj = by_id.get(finality) if finality else None

            if state_obj is None or state_obj.get("kind") not in {"snapshot", "merge"}:
                errors.append(issue("V042", "execution state must reference snapshot or merge", sid))
            if finality_obj is None or finality_obj.get("kind") != "finality":
                errors.append(issue("V042", "execution requires an existing finality record", sid))
            else:
                if ref_id(finality_obj.get("target")) != state:
                    errors.append(issue("V042", "execution finality does not target execution state", sid))
                execution_time = statement_time(s)
                final_time = statement_time(finality_obj)
                if execution_time is None:
                    errors.append(issue("V042", "execution requires a valid at timestamp", sid))
                elif final_time is not None and execution_time < final_time:
                    errors.append(issue("V042", "execution cannot precede finality", sid))

    # Detect sibling divergence.
    divergent_pairs: dict[tuple[str, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    for left, right in combinations(snapshots, 2):
        if left.get("domain") != right.get("domain"):
            continue
        if snapshot_parent_id(left) != snapshot_parent_id(right):
            continue
        if left.get("seq") != right.get("seq"):
            continue
        if left.get("state_hash") == right.get("state_hash"):
            continue
        key = pair_key(str(left.get("id")), str(right.get("id")))
        divergent_pairs[key] = (left, right)

    declared_pairs: dict[tuple[str, str], str] = {}
    for s in statements:
        if not isinstance(s, dict) or s.get("kind") != "split_brain_conflict":
            continue
        left = ref_id(s.get("left"))
        right = ref_id(s.get("right"))
        if left and right:
            declared_pairs[pair_key(left, right)] = str(s.get("id"))

    for key, (left, right) in divergent_pairs.items():
        conflicts.append(
            {
                "rule": "V036",
                "left": left.get("id"),
                "right": right.get("id"),
                "message": "divergent sibling snapshots detected",
            }
        )
        if key not in declared_pairs:
            errors.append(
                issue(
                    "V036",
                    f"split-brain divergence between [{key[0]}] and [{key[1]}] must be declared",
                )
            )

    # Conflict objects must describe a real divergence.
    for key, conflict_id in declared_pairs.items():
        if key not in divergent_pairs:
            errors.append(issue("V037", "declared conflict does not correspond to divergent siblings", conflict_id))

    # A divergent branch snapshot cannot be finalized directly.
    divergent_snapshot_ids = {sid for pair in divergent_pairs for sid in pair}
    finalities = [s for s in statements if isinstance(s, dict) and s.get("kind") == "finality"]
    seen_terms: dict[int, str] = {}
    ordered_finalities = []

    for s in finalities:
        sid = str(s.get("id"))
        target = ref_id(s.get("target"))
        if target in divergent_snapshot_ids:
            errors.append(issue("V041", "divergent branch snapshot cannot receive finality before merge", sid))
        term = s.get("term")
        when = statement_time(s)
        if isinstance(term, int) and not isinstance(term, bool):
            if term in seen_terms:
                errors.append(issue("V043", f"duplicate finality term {term}", sid))
            else:
                seen_terms[term] = sid
            if when is not None:
                ordered_finalities.append((when, term, sid))

    ordered_finalities.sort(key=lambda x: (x[0], x[1]))
    for (_, prior_term, _), (_, next_term, next_id) in zip(ordered_finalities, ordered_finalities[1:]):
        if next_term <= prior_term:
            errors.append(issue("V043", "finality term must increase with finality time", next_id))

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
        "authority_epoch": base.get("authority_epoch", 0),
    }


def main() -> int:
    try:
        doc = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"valid": False, "errors": [{"rule": "V000", "message": str(exc)}]}))
        return 2
    result = validate_document(doc)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
