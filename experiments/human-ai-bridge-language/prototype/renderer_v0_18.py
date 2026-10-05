#!/usr/bin/env python3
"""Bridge-0 canonical renderer prototype v0.18."""

from __future__ import annotations

import json
import sys
from typing import Any

from renderer_v0_2 import BridgeRenderError
from renderer_v0_3 import render_kv


def render_statement(s: dict[str, Any]) -> str:
    sid = s.get("id")
    if not isinstance(sid, str) or not sid:
        raise BridgeRenderError("v0.18 statement missing id")
    qid = f"[{sid}]"

    if s.get("kind") == "program":
        return (
            f"⊙ {qid} program "
            + render_kv([
                ("name", s.get("name")),
                ("targets", s.get("targets")),
            ])
        )

    if s.get("kind") == "loss_authorization":
        return (
            f"→ {qid} authorize_loss "
            + render_kv([
                ("domain", s.get("domain")),
                ("artifact", s.get("artifact")),
                ("route", s.get("route")),
                ("loss_ack", s.get("loss_ack")),
                ("authority", s.get("authority")),
                ("scope", s.get("scope")),
                ("artifact_digest", s.get("artifact_digest")),
                ("provenance", s.get("provenance")),
                ("issued_at", s.get("issued_at")),
                ("expires_at", s.get("expires_at")),
                ("evaluate_at", s.get("evaluate_at")),
                ("observe", s.get("observe")),
            ])
        )

    raise BridgeRenderError(f"Unsupported v0.18 statement kind: {s.get('kind')!r}")


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
