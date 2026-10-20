#!/usr/bin/env python3
"""Bridge-0 canonical renderer prototype v0.6."""

from __future__ import annotations

import json
import sys
from typing import Any

from renderer_v0_2 import BridgeRenderError
from renderer_v0_3 import render_kv
from renderer_v0_5 import render_statement as render_v05


def render_statement(s: dict[str, Any]) -> str:
    sid = s.get("id")
    if not isinstance(sid, str) or not sid:
        raise BridgeRenderError("v0.6 statement missing id")
    qid = f"[{sid}]"
    kind = s.get("kind")

    if kind == "conflict_set":
        ordered = [
            ("members", s.get("members")),
            ("domain", s.get("domain")),
            ("status", s.get("status")),
        ]
        return f"◆ {qid} conflict_set {render_kv(ordered)}"

    if kind == "quorum_policy":
        ordered = [
            ("voters", s.get("voters")),
            ("threshold", s.get("threshold")),
            ("independence_min", s.get("independence_min")),
        ]
        return f"! {qid} quorum {render_kv(ordered)}"

    if kind == "reconciliation_proposal":
        ordered = [
            ("conflict_set", s.get("conflict_set")),
            ("strategy", s.get("strategy")),
            ("result_hash", s.get("result_hash")),
            ("at", s.get("at")),
        ]
        return f"→ {qid} propose {render_kv(ordered)}"

    if kind == "vote":
        ordered = [
            ("voter", s.get("voter")),
            ("proposal", s.get("proposal")),
            ("decision", s.get("decision")),
            ("independence", s.get("independence")),
            ("evidence_hash", s.get("evidence_hash")),
            ("at", s.get("at")),
        ]
        return f"◆ {qid} vote {render_kv(ordered)}"

    if kind == "finality_certificate":
        ordered = [
            ("proposal", s.get("proposal")),
            ("quorum", s.get("quorum")),
            ("votes", s.get("votes")),
            ("issued_by", s.get("issued_by")),
            ("term", s.get("term")),
            ("at", s.get("at")),
        ]
        return f"✓ {qid} certificate {render_kv(ordered)}"

    return render_v05(s)


def render_document(doc: dict[str, Any]) -> str:
    if doc.get("language") != "Bridge-0":
        raise BridgeRenderError("Document language must be Bridge-0")
    statements = doc.get("statements")
    if not isinstance(statements, list):
        raise BridgeRenderError("Document statements must be a list")
    lines = [render_statement(s) for s in statements]
    return "\n".join(lines) + ("\n" if lines else "")


def main() -> int:
    try:
        doc = json.load(sys.stdin)
        out = render_document(doc)
    except (json.JSONDecodeError, BridgeRenderError) as exc:
        print(f"BridgeRenderError: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
