#!/usr/bin/env python3
"""Bridge-0 canonical renderer prototype v0.5."""

from __future__ import annotations

import json
import sys
from typing import Any

from renderer_v0_2 import BridgeRenderError
from renderer_v0_3 import render_kv
from renderer_v0_4 import render_statement as render_v04


def render_statement(s: dict[str, Any]) -> str:
    sid = s.get("id")
    if not isinstance(sid, str) or not sid:
        raise BridgeRenderError("Concurrency statement missing id")
    qid = f"[{sid}]"
    kind = s.get("kind")

    if kind == "snapshot":
        ordered = [
            ("branch", s.get("branch")),
            ("parent", s.get("parent")),
            ("seq", s.get("seq")),
            ("domain", s.get("domain")),
            ("state_hash", s.get("state_hash")),
            ("at", s.get("at")),
        ]
        return f"○ {qid} snapshot {render_kv(ordered)}"

    if kind == "split_brain_conflict":
        ordered = [
            ("left", s.get("left")),
            ("right", s.get("right")),
            ("domain", s.get("domain")),
            ("status", s.get("status")),
        ]
        return f"◆ {qid} conflict {render_kv(ordered)}"

    if kind == "merge":
        ordered = [
            ("left", s.get("left")),
            ("right", s.get("right")),
            ("conflict", s.get("conflict")),
            ("strategy", s.get("strategy")),
            ("result_hash", s.get("result_hash")),
            ("at", s.get("at")),
        ]
        return f"→ {qid} merge {render_kv(ordered)}"

    if kind == "finality":
        ordered = [
            ("target", s.get("target")),
            ("by", s.get("by")),
            ("term", s.get("term")),
            ("at", s.get("at")),
        ]
        return f"✓ {qid} final {render_kv(ordered)}"

    if kind == "execution":
        ordered = [
            ("actor", s.get("actor")),
            ("action", s.get("action")),
            ("state", s.get("state")),
            ("finality", s.get("finality")),
            ("at", s.get("at")),
        ]
        return f"→ {qid} execute {render_kv(ordered)}"

    return render_v04(s)


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
