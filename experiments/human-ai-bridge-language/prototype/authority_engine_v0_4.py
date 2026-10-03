#!/usr/bin/env python3
"""Bridge-0 authority lifecycle engine v0.4.

This module evaluates grant/delegation/revocation/expiry/replay state.
It is deliberately deterministic and restricted.

Important: a stale document cannot know about a revocation that is absent from
that document. The caller may therefore supply an external expected_epoch.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from validator_v0_3 import parse_time, ref_id


AUTHORITY_KINDS = {"grant", "delegation"}
MUTATION_KINDS = {"grant", "delegation", "revocation"}


def event_time(statement: dict[str, Any]) -> datetime | None:
    raw = statement.get("at")
    if not isinstance(raw, str):
        return None
    try:
        return parse_time(raw)
    except ValueError:
        return None


def scope_subset(child: str, parent: str) -> bool:
    """Restricted absolute-path scope containment for v0.4."""
    if not isinstance(child, str) or not isinstance(parent, str):
        return False
    if not child.startswith("/") or not parent.startswith("/"):
        return False
    if ".." in child or ".." in parent:
        return False

    if parent == "/**":
        return True

    if parent.endswith("/**"):
        base = parent[:-3]
        if child == parent or child == base:
            return True
        return child.startswith(base.rstrip("/") + "/")

    return child == parent


def authority_actor(statement: dict[str, Any]) -> str | None:
    if statement.get("kind") == "grant":
        value = statement.get("actor")
        return value if isinstance(value, str) else None
    if statement.get("kind") == "delegation":
        value = statement.get("to")
        return value if isinstance(value, str) else None
    return None


def authority_start(statement: dict[str, Any]) -> datetime | None:
    raw = statement.get("valid_from")
    if not isinstance(raw, str):
        raw = statement.get("at")
    if not isinstance(raw, str):
        return None
    try:
        return parse_time(raw)
    except ValueError:
        return None


def authority_end(statement: dict[str, Any]) -> datetime | None:
    raw = statement.get("valid_until")
    if not isinstance(raw, str):
        return None
    try:
        return parse_time(raw)
    except ValueError:
        return None


def build_index(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    statements = doc.get("statements", [])
    return {
        s["id"]: s
        for s in statements
        if isinstance(s, dict) and isinstance(s.get("id"), str)
    }


def revocation_times(doc: dict[str, Any]) -> dict[str, list[datetime]]:
    out: dict[str, list[datetime]] = {}
    for s in doc.get("statements", []):
        if not isinstance(s, dict) or s.get("kind") != "revocation":
            continue
        target = ref_id(s.get("target"))
        when = event_time(s)
        if target is not None and when is not None:
            out.setdefault(target, []).append(when)
    return out


def authority_active(
    doc: dict[str, Any],
    authority_id: str,
    at: datetime,
    _stack: tuple[str, ...] = (),
) -> bool:
    by_id = build_index(doc)
    statement = by_id.get(authority_id)
    if statement is None or statement.get("kind") not in AUTHORITY_KINDS:
        return False

    if authority_id in _stack:
        return False

    start = authority_start(statement)
    if start is None or at < start:
        return False

    end = authority_end(statement)
    if end is not None and at > end:
        return False

    for revoked_at in revocation_times(doc).get(authority_id, []):
        if revoked_at <= at:
            return False

    if statement.get("kind") == "delegation":
        parent = ref_id(statement.get("parent"))
        if parent is None:
            return False
        if not authority_active(doc, parent, at, _stack + (authority_id,)):
            return False

    return True


def authority_root_grant(
    doc: dict[str, Any],
    authority_id: str,
) -> dict[str, Any] | None:
    by_id = build_index(doc)
    seen: set[str] = set()
    current = authority_id
    while current not in seen:
        seen.add(current)
        s = by_id.get(current)
        if s is None:
            return None
        if s.get("kind") == "grant":
            return s
        if s.get("kind") != "delegation":
            return None
        parent = ref_id(s.get("parent"))
        if parent is None:
            return None
        current = parent
    return None


def current_epoch_at(doc: dict[str, Any], at: datetime) -> int:
    epochs: list[int] = []
    for s in doc.get("statements", []):
        if not isinstance(s, dict) or s.get("kind") not in MUTATION_KINDS:
            continue
        when = event_time(s)
        epoch = s.get("epoch")
        if when is not None and when <= at and isinstance(epoch, int) and not isinstance(epoch, bool):
            epochs.append(epoch)
    return max(epochs, default=0)


def document_epoch(doc: dict[str, Any]) -> int:
    epochs = [
        s.get("epoch")
        for s in doc.get("statements", [])
        if isinstance(s, dict)
        and s.get("kind") in MUTATION_KINDS
        and isinstance(s.get("epoch"), int)
        and not isinstance(s.get("epoch"), bool)
    ]
    return max(epochs, default=0)
