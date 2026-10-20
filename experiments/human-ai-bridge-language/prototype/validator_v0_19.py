#!/usr/bin/env python3
"""Bridge-0 revocation / replay-resistance validator v0.19."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from validator_v0_3 import issue


SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
AUTH_ID = re.compile(r"^[A-Za-z0-9_.:-]{8,64}$")
NONCE = re.compile(r"^[A-Za-z0-9_-]{8,64}$")
UTC_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")

ALLOWED_TARGETS = {"python312", "node20"}
EXPECTED_DIGEST = "07b88b41d6be837f8b370c27523053bf84b214eef0bc1d074633e1250db2db92"
EXPECTED_LOSS = {
    "$.units[*].id",
    "$.units[*].label",
    "$.units[*].confidence",
    "$.provenance",
    "$.notes",
}
EXPECTED_REVOCATION_EPOCH = 7


def csv_values(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [v.strip() for v in raw.split(",") if v.strip()]


def pipe_values(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [v.strip() for v in raw.split("|") if v.strip()]


def validate_document(doc: dict[str, Any]) -> dict[str, Any]:
    errors = []
    warnings = []
    conflicts = []

    statements = doc.get("statements")
    if not isinstance(statements, list):
        errors.append(issue("V121", "statements must be a list"))
        return {"valid": False, "errors": errors, "warnings": warnings, "conflicts": conflicts}

    programs = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "program"
    ]
    auths = [
        s for s in statements
        if isinstance(s, dict) and s.get("kind") == "single_use_authorization"
    ]
    others = [
        s for s in statements
        if isinstance(s, dict)
        and s.get("kind") not in {"program", "single_use_authorization"}
    ]

    if others:
        errors.append(issue("V121", "v0.19 executable subset contains unsupported statement kinds"))

    if len(programs) != 1:
        errors.append(issue("V121", "v0.19 requires exactly one program"))
    else:
        program = programs[0]
        sid = str(program.get("id"))
        name = program.get("name")
        targets = csv_values(program.get("targets"))
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name):
            errors.append(issue("V121", "program name is invalid", sid))
        if len(targets) != len(set(targets)):
            errors.append(issue("V122", "program targets must be unique", sid))
        if set(targets) != ALLOWED_TARGETS:
            errors.append(
                issue(
                    "V122",
                    "v0.19 replay test requires exactly python312,node20",
                    sid,
                )
            )

    if len(auths) != 1:
        errors.append(issue("V123", "v0.19 requires exactly one single-use authorization"))
    else:
        task = auths[0]
        sid = str(task.get("id"))

        if task.get("domain") != "grapheme":
            errors.append(issue("V123", "v0.19 supports only domain=grapheme", sid))
        if task.get("artifact") != "fixture_v1":
            errors.append(issue("V124", "v0.19 requires artifact=fixture_v1", sid))
        if task.get("route") != "v1_to_v3_compact":
            errors.append(issue("V124", "v0.19 authorizes only route=v1_to_v3_compact", sid))

        auth_id = task.get("authorization_id")
        nonce = task.get("nonce")
        if not isinstance(auth_id, str) or not AUTH_ID.fullmatch(auth_id):
            errors.append(issue("V125", "authorization_id format is invalid", sid))
        if not isinstance(nonce, str) or not NONCE.fullmatch(nonce):
            errors.append(issue("V125", "nonce format is invalid", sid))

        ack = pipe_values(task.get("loss_ack"))
        if len(ack) != len(set(ack)) or set(ack) != EXPECTED_LOSS:
            errors.append(issue("V126", "loss_ack must exactly match the known loss manifest", sid))

        if task.get("authority") != "fixture_owner":
            errors.append(issue("V127", "v0.19 requires authority=fixture_owner", sid))
        if task.get("scope") != "exact_loss_manifest":
            errors.append(issue("V127", "v0.19 requires scope=exact_loss_manifest", sid))
        if task.get("provenance") != "fixture_authority_record":
            errors.append(issue("V127", "v0.19 requires bound authority provenance", sid))

        digest = task.get("artifact_digest")
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            errors.append(issue("V128", "artifact_digest must be lowercase sha256", sid))
        elif digest != EXPECTED_DIGEST:
            errors.append(issue("V128", "artifact_digest does not bind the authorized artifact", sid))

        try:
            epoch = int(str(task.get("revocation_epoch")))
        except ValueError:
            epoch = -1
        if epoch != EXPECTED_REVOCATION_EPOCH:
            errors.append(
                issue(
                    "V129",
                    f"v0.19 requires revocation_epoch={EXPECTED_REVOCATION_EPOCH}",
                    sid,
                )
            )
        if task.get("usage") != "single_use":
            errors.append(issue("V129", "v0.19 requires usage=single_use", sid))

        for field in ("issued_at", "expires_at", "evaluate_at"):
            value = task.get(field)
            if not isinstance(value, str) or not UTC_TIME.fullmatch(value):
                errors.append(issue("V130", f"{field} must be canonical UTC time", sid))

        if task.get("observe") != "json_value":
            errors.append(issue("V130", "v0.19 requires observe=json_value", sid))

        allowed = {
            "id",
            "kind",
            "domain",
            "artifact",
            "route",
            "authorization_id",
            "nonce",
            "loss_ack",
            "authority",
            "scope",
            "artifact_digest",
            "provenance",
            "revocation_epoch",
            "usage",
            "issued_at",
            "expires_at",
            "evaluate_at",
            "observe",
        }
        extras = set(task) - allowed
        if extras:
            errors.append(issue("V131", "single-use authorization contains unsupported fields", sid))

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
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
