#!/usr/bin/env python3
"""Bridge-0 canonical renderer prototype v0.2.

Renders canonical IR back into the restricted Bridge-0 surface syntax.
The goal is semantic round-trip stability, not stylistic preservation.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
PATH = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)*$")


class BridgeRenderError(ValueError):
    pass


def qid(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", value or ""):
        raise BridgeRenderError(f"Invalid semantic id: {value!r}")
    return f"[{value}]"


def render_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        # Avoid gratuitous trailing zeros while remaining deterministic.
        return format(value, ".15g")
    if isinstance(value, dict) and set(value.keys()) == {"ref"}:
        return qid(str(value["ref"]))
    if isinstance(value, str):
        if IDENT.fullmatch(value):
            return value
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    raise BridgeRenderError(f"Unsupported value type: {type(value).__name__}")


def render_term(value: Any) -> str:
    if isinstance(value, dict) and set(value.keys()) == {"ref"}:
        return qid(str(value["ref"]))
    if isinstance(value, str):
        if PATH.fullmatch(value):
            return value
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return render_value(value)
    raise BridgeRenderError(f"Unsupported term: {value!r}")


def render_statement(s: dict[str, Any]) -> str:
    sid = qid(str(s.get("id", "")))
    kind = s.get("kind")

    if kind == "entity":
        name = s.get("name")
        if not isinstance(name, str) or not IDENT.fullmatch(name):
            raise BridgeRenderError(f"Invalid entity name for {sid}")
        return f"○ {sid} {name}"

    if kind == "claim":
        state = s.get("epistemic_state")
        marker = {"fact": "■", "hypothesis": "△"}.get(state)
        if marker is None:
            raise BridgeRenderError(f"Invalid epistemic state for {sid}: {state}")

        if "path" in s and s.get("operator") == "=":
            path = s["path"]
            if not isinstance(path, str) or not PATH.fullmatch(path):
                raise BridgeRenderError(f"Invalid claim path for {sid}")
            value = render_value(s.get("value"))
            unit = s.get("unit")
            suffix = f" {unit}" if unit else ""
            return f"{marker} {sid} {path} = {value}{suffix}"

        if "predicate" in s:
            return (
                f"{marker} {sid} "
                f"{render_term(s.get('subject'))} "
                f"{s.get('predicate')} "
                f"{render_term(s.get('object'))}"
            )

        raise BridgeRenderError(f"Claim {sid} has no renderable form")

    if kind == "unknown":
        path = s.get("path")
        if not isinstance(path, str) or not PATH.fullmatch(path):
            raise BridgeRenderError(f"Invalid unknown path for {sid}")
        return f"? {sid} {path}"

    if kind == "evidence":
        source = s.get("source")
        relation = s.get("relation")
        target = s.get("target")
        if not isinstance(source, str):
            raise BridgeRenderError(f"Invalid evidence source for {sid}")
        return f"◆ {sid} {source} {relation} {qid(str(target))}"

    if kind == "guard":
        return (
            f"! {sid} {s.get('action')} "
            f"{s.get('relation')} {s.get('condition')}"
        )

    if kind == "goal":
        return f"⊙ {sid} {s.get('expression')}"

    if kind == "action":
        out = f"→ {sid} {s.get('actor')} {s.get('action')}"
        if s.get("object") is not None:
            out += f" {s.get('object')}"
        return out

    if kind == "verification":
        return f"✓ {sid} {qid(str(s.get('target')))} verified_by {s.get('method')}"

    if kind == "prohibition":
        return f"× {sid} {s.get('expression')}"

    if kind == "time_binding":
        return f"⏱ {sid} {s.get('path')} = {s.get('timestamp')}"

    raise BridgeRenderError(f"Unsupported statement kind: {kind!r}")


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
