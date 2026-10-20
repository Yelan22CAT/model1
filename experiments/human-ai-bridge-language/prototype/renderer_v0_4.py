#!/usr/bin/env python3
"""Bridge-0 canonical renderer prototype v0.4."""

from __future__ import annotations

import json
import sys
from typing import Any

from renderer_v0_2 import BridgeRenderError
from renderer_v0_3 import render_atom, render_kv, render_statement as render_v03


def render_statement(s: dict[str, Any]) -> str:
    sid = s.get("id")
    if not isinstance(sid, str) or not sid:
        raise BridgeRenderError("Authority lifecycle statement missing id")
    qid = f"[{sid}]"
    kind = s.get("kind")

    if kind == "grant":
        ordered = [
            ("grantor", s.get("grantor")),
            ("actor", s.get("actor")),
            ("action", s.get("action")),
            ("resource", s.get("resource")),
            ("scope", s.get("scope")),
            ("at", s.get("at")),
            ("epoch", s.get("epoch")),
        ]
        for key in ("valid_from", "valid_until", "condition"):
            if key in s:
                ordered.append((key, s[key]))
        return f"! {qid} grant {render_kv(ordered)}"

    if kind == "delegation":
        ordered = [
            ("parent", s.get("parent")),
            ("from", s.get("from")),
            ("to", s.get("to")),
            ("action", s.get("action")),
            ("resource", s.get("resource")),
            ("scope", s.get("scope")),
            ("at", s.get("at")),
            ("epoch", s.get("epoch")),
        ]
        for key in ("valid_until", "condition"):
            if key in s:
                ordered.append((key, s[key]))
        return f"→ {qid} delegate {render_kv(ordered)}"

    if kind == "revocation":
        ordered = [
            ("target", s.get("target")),
            ("by", s.get("by")),
            ("at", s.get("at")),
            ("epoch", s.get("epoch")),
        ]
        if "reason" in s:
            ordered.append(("reason", s["reason"]))
        return f"× {qid} revoke {render_kv(ordered)}"

    if kind == "replay":
        ordered = [
            ("target", s.get("target")),
            ("authority", s.get("authority")),
            ("at", s.get("at")),
            ("epoch", s.get("epoch")),
        ]
        return f"→ {qid} replay {render_kv(ordered)}"

    return render_v03(s)


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
