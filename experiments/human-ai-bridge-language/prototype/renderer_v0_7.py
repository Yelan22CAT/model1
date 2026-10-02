#!/usr/bin/env python3
"""Bridge-0 canonical renderer prototype v0.7."""

from __future__ import annotations

import json
import sys
from typing import Any

from renderer_v0_2 import BridgeRenderError
from renderer_v0_3 import render_kv
from renderer_v0_6 import render_statement as render_v06


def render_statement(s: dict[str, Any]) -> str:
    sid = s.get("id")
    if not isinstance(sid, str) or not sid:
        raise BridgeRenderError("v0.7 statement missing id")
    qid = f"[{sid}]"
    kind = s.get("kind")

    if kind == "identity":
        ordered = [
            ("subject", s.get("subject")),
            ("control_domain", s.get("control_domain")),
            ("model_lineage", s.get("model_lineage")),
            ("runtime_origin", s.get("runtime_origin")),
        ]
        return f"○ {qid} identity {render_kv(ordered)}"

    if kind == "identity_attestation":
        ordered = [
            ("identity", s.get("identity")),
            ("issuer", s.get("issuer")),
            ("status", s.get("status")),
            ("valid_from", s.get("valid_from")),
            ("valid_until", s.get("valid_until")),
        ]
        return f"◆ {qid} attest {render_kv(ordered)}"

    if kind == "evidence_provenance":
        ordered = [
            ("evidence_hash", s.get("evidence_hash")),
            ("source_identity", s.get("source_identity")),
            ("attestation", s.get("attestation")),
            ("origin", s.get("origin")),
            ("parent", s.get("parent")),
        ]
        return f"◆ {qid} evidence_provenance {render_kv(ordered)}"

    if kind == "vote":
        ordered = [
            ("voter", s.get("voter")),
            ("proposal", s.get("proposal")),
            ("decision", s.get("decision")),
            ("independence", s.get("independence")),
            ("evidence_hash", s.get("evidence_hash")),
            ("identity", s.get("identity")),
            ("attestation", s.get("attestation")),
            ("provenance", s.get("provenance")),
            ("at", s.get("at")),
        ]
        return f"◆ {qid} vote {render_kv(ordered)}"

    if kind == "quorum_policy":
        ordered = [
            ("voters", s.get("voters")),
            ("threshold", s.get("threshold")),
            ("independence_min", s.get("independence_min")),
            ("evidence_min", s.get("evidence_min")),
        ]
        return f"! {qid} quorum {render_kv(ordered)}"

    if kind == "attestation_revocation":
        ordered = [
            ("target", s.get("target")),
            ("by", s.get("by")),
            ("at", s.get("at")),
        ]
        return f"× {qid} revoke_attestation {render_kv(ordered)}"

    return render_v06(s)


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
