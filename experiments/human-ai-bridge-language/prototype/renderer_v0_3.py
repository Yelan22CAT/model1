#!/usr/bin/env python3
"""Bridge-0 canonical renderer prototype v0.3."""

from __future__ import annotations

import json
import sys
from typing import Any

from renderer_v0_2 import BridgeRenderError, render_statement as render_v02_statement


def render_atom(value: Any) -> str:
    if isinstance(value, dict) and set(value) == {"ref"}:
        ref = value["ref"]
        return f"[{ref}]"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        if any(ch.isspace() for ch in value):
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        return value
    raise BridgeRenderError(f"Unsupported structured value: {value!r}")


def render_kv(fields: list[tuple[str, Any]]) -> str:
    return " ".join(f"{key}={render_atom(value)}" for key, value in fields)


def render_statement(s: dict[str, Any]) -> str:
    sid = s.get("id")
    if not isinstance(sid, str) or not sid:
        raise BridgeRenderError("Structured statement missing id")
    qid = f"[{sid}]"
    kind = s.get("kind")

    if kind == "permission":
        ordered = [
            ("actor", s.get("actor")),
            ("action", s.get("action")),
            ("resource", s.get("resource")),
            ("scope", s.get("scope")),
        ]
        for key in ("condition", "valid_from", "valid_until"):
            if key in s:
                ordered.append((key, s[key]))
        return f"! {qid} permission {render_kv(ordered)}"

    if kind == "handoff":
        ordered = [
            ("from", s.get("from")),
            ("to", s.get("to")),
            ("artifact", s.get("artifact")),
            ("scope", s.get("scope")),
            ("state", s.get("state")),
            ("provenance", s.get("provenance")),
        ]
        if "transform" in s:
            ordered.append(("transform", s["transform"]))
        if "time" in s:
            ordered.append(("time", s["time"]))
        return f"→ {qid} handoff {render_kv(ordered)}"

    if kind == "state_transition":
        ordered = [
            ("subject", s.get("subject")),
            ("from", s.get("from")),
            ("to", s.get("to")),
            ("irreversible", s.get("irreversible")),
        ]
        if "when" in s:
            ordered.append(("when", s["when"]))
        if "authority" in s:
            ordered.append(("authority", s["authority"]))
        return f"→ {qid} transition {render_kv(ordered)}"

    if kind == "provenance":
        ordered = [
            ("artifact", s.get("artifact")),
            ("parent", s.get("parent")),
            ("actor", s.get("actor")),
            ("transform", s.get("transform")),
        ]
        if "time" in s:
            ordered.append(("time", s["time"]))
        return f"◆ {qid} provenance {render_kv(ordered)}"

    return render_v02_statement(s)


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
        text = render_document(doc)
    except (json.JSONDecodeError, BridgeRenderError) as exc:
        print(f"BridgeRenderError: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
