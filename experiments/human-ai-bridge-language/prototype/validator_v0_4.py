#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from typing import Any

from authority_engine_v0_4 import (
    AUTHORITY_KINDS,
    MUTATION_KINDS,
    authority_active,
    authority_actor,
    authority_end,
    authority_root_grant,
    authority_start,
    build_index,
    current_epoch_at,
    document_epoch,
    event_time,
    scope_subset,
)
from validator_v0_3 import issue, ref_id, validate_document as validate_v03


def validate_document(doc: dict[str, Any], expected_epoch: int | None = None) -> dict[str, Any]:
    base = validate_v03(doc)
    errors = list(base["errors"])
    warnings = list(base["warnings"])
    conflicts = list(base["conflicts"])

    statements = doc.get("statements")
    if not isinstance(statements, list):
        return base

    by_id = build_index(doc)
    seen_epochs: dict[int, str] = {}
    mutations: list[tuple[Any, int, str]] = []

    for s in statements:
        if not isinstance(s, dict):
            continue
        sid = s.get("id")
        kind = s.get("kind")

        if kind in MUTATION_KINDS:
            epoch = s.get("epoch")
            when = event_time(s)
            if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch <= 0:
                errors.append(issue("V026", "epoch must be a positive integer", sid))
            elif epoch in seen_epochs:
                errors.append(issue("V026", f"duplicate epoch {epoch}", sid))
            else:
                seen_epochs[epoch] = str(sid)
            if when is None:
                errors.append(issue("V027", "event requires valid at timestamp", sid))
            elif isinstance(epoch, int) and not isinstance(epoch, bool):
                mutations.append((when, epoch, str(sid)))

    ordered = sorted(mutations, key=lambda x: (x[0], x[1]))
    for (_, e1, _), (_, e2, sid2) in zip(ordered, ordered[1:]):
        if e2 <= e1:
            errors.append(issue("V026", "epoch order conflicts with event time", sid2))

    for s in statements:
        if not isinstance(s, dict):
            continue
        sid = s.get("id")
        kind = s.get("kind")

        if kind == "grant":
            required = ("grantor", "actor", "action", "resource", "scope", "at", "epoch")
            missing = [k for k in required if s.get(k) in (None, "")]
            if missing:
                errors.append(issue("V028", "grant missing: " + ", ".join(missing), sid))
            if not scope_subset(str(s.get("scope", "")), "/**"):
                errors.append(issue("V028", "grant scope must be an absolute restricted scope", sid))
            start = authority_start(s)
            end = authority_end(s)
            if start is None:
                errors.append(issue("V028", "grant has invalid start", sid))
            if end is not None and start is not None and end < start:
                errors.append(issue("V028", "grant end precedes start", sid))

        elif kind == "delegation":
            parent_id = ref_id(s.get("parent"))
            parent = by_id.get(parent_id) if parent_id else None
            when = event_time(s)
            if parent is None or parent.get("kind") not in AUTHORITY_KINDS:
                errors.append(issue("V029", "delegation parent must be an existing authority", sid))
                continue
            if when is None or not authority_active(doc, parent_id, when):
                errors.append(issue("V029", "parent authority is not active at delegation time", sid))
            if s.get("from") != authority_actor(parent):
                errors.append(issue("V029", "delegation from does not match parent holder", sid))
            if s.get("action") != parent.get("action"):
                errors.append(issue("V030", "delegation cannot change action", sid))
            if s.get("resource") != parent.get("resource"):
                errors.append(issue("V030", "delegation cannot change resource", sid))
            if not scope_subset(str(s.get("scope", "")), str(parent.get("scope", ""))):
                errors.append(issue("V030", "delegation scope must be narrower or equal", sid))
            child_end = authority_end(s)
            parent_end = authority_end(parent)
            if child_end is not None and parent_end is not None and child_end > parent_end:
                errors.append(issue("V030", "delegation cannot outlive parent", sid))

        elif kind == "revocation":
            target_id = ref_id(s.get("target"))
            target = by_id.get(target_id) if target_id else None
            when = event_time(s)
            if target is None or target.get("kind") not in AUTHORITY_KINDS:
                errors.append(issue("V031", "revocation target must be an existing authority", sid))
                continue
            root = authority_root_grant(doc, target_id)
            if root is None or s.get("by") != root.get("grantor"):
                errors.append(issue("V031", "revocation issuer must match root grantor", sid))
            start = authority_start(target)
            if when is None:
                errors.append(issue("V031", "revocation requires valid at timestamp", sid))
            elif start is not None and when < start:
                errors.append(issue("V031", "revocation cannot precede authority start", sid))

        elif kind == "replay":
            target_id = ref_id(s.get("target"))
            authority_id = ref_id(s.get("authority"))
            when = event_time(s)
            epoch = s.get("epoch")
            if target_id is None or target_id not in by_id:
                errors.append(issue("V032", "replay target does not exist", sid))
            if authority_id is None or authority_id not in by_id:
                errors.append(issue("V032", "replay authority does not exist", sid))
                continue
            if when is None:
                errors.append(issue("V032", "replay requires valid at timestamp", sid))
                continue
            if not authority_active(doc, authority_id, when):
                errors.append(issue("V032", "replay authority is inactive at replay time", sid))
            expected_at_time = current_epoch_at(doc, when)
            if epoch != expected_at_time:
                errors.append(issue("V034", f"replay epoch {epoch} != {expected_at_time}", sid))

    if expected_epoch is not None:
        local_epoch = document_epoch(doc)
        if local_epoch != expected_epoch:
            errors.append(issue("V033", f"local epoch {local_epoch} != runtime epoch {expected_epoch}"))

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
        "authority_epoch": document_epoch(doc),
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
