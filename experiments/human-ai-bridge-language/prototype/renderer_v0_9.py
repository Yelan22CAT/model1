#!/usr/bin/env python3
"""Bridge-0 canonical renderer prototype v0.9."""

from __future__ import annotations

import json
import sys
from typing import Any

from renderer_v0_2 import BridgeRenderError
from renderer_v0_3 import render_kv
from renderer_v0_8 import render_statement as render_v08


def render_statement(s: dict[str, Any]) -> str:
    sid = s.get("id")
    if not isinstance(sid, str) or not sid:
        raise BridgeRenderError("v0.9 statement missing id")

    if s.get("kind") == "workflow_task":
        ordered = [("kind", s.get("task_kind"))]
        for key in ("version", "module", "cwd", "args", "observe"):
            if key in s:
                ordered.append((key, s.get(key)))
        return f"→ [{sid}] task {render_kv(ordered)}"

    return render_v08(s)


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
