#!/usr/bin/env python3
"""Bridge-0 identity / provenance / anti-Sybil validator v0.7.

This layer verifies semantic consistency of declared identity attestations and
evidence provenance. It does not perform cryptographic identity proof.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from typing import Any

from authority_engine_v0_4 import build_index
from validator_v0_3 import issue, parse_time, ref_id
from validator_v0_6 import csv_values, statement_time, validate_document as validate_v06


TRUSTED_IDENTITY_ISSUERS = {"identity_ca", "backup_ca"}


def attestation_active(
    doc: dict[str, Any],
    attestation_id: str,
    at,
) -> bool:
    by_id = build_index(doc)
    attestation = by_id.get(attestation_id)
    if attestation is None or attestation.get("kind") != "identity_attestation":
        return False
    if attestation.get("status") != "valid":
        return False
    try:
        start = parse_time(str(attestation.get("valid_from")))
        end = parse_time(str(attestation.get("valid_until")))
    except ValueError:
        return False
    if at < start or at > end:
        return False

    for s in doc.get("statements", []):
        if not isinstance(s, dict) or s.get("kind") != "attestation_revocation":
            continue
        if ref_id(s.get("target")) != attestation_id:
            continue
        rt = statement_time(s)
        if rt is not None and rt <= at:
            return False
    return True


def identity_key(identity: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(identity.get("control_domain", "")),
        str(identity.get("model_lineage", "")),
        str(identity.get("runtime_origin", "")),
    )


def evidence_root_fingerprint(
    doc: dict[str, Any],
    provenance_id: str,
) -> tuple[str, str] | None:
    by_id = build_index(doc)
    seen: set[str] = set()
    current = provenance_id

    while current not in seen:
        seen.add(current)
        record = by_id.get(current)
        if record is None or record.get("kind") != "evidence_provenance":
            return None

        parent = record.get("parent")
        if parent == "none":
            return (
                str(record.get("origin", "")),
                str(record.get("evidence_hash", "")),
            )

        parent_id = ref_id(parent)
        if parent_id is None:
            return None
        current = parent_id

    return None


def validate_document(
    doc: dict[str, Any],
    expected_epoch: int | None = None,
    trusted_finalizer: str = "control_plane",
) -> dict[str, Any]:
    base = validate_v06(
        doc,
        expected_epoch=expected_epoch,
        trusted_finalizer=trusted_finalizer,
    )
    errors = list(base["errors"])
    warnings = list(base["warnings"])
    conflicts = list(base["conflicts"])

    statements = doc.get("statements")
    if not isinstance(statements, list):
        return base

    by_id = build_index(doc)
    identities: list[dict[str, Any]] = []
    attestations: list[dict[str, Any]] = []
    provenance_records: list[dict[str, Any]] = []
    votes: list[dict[str, Any]] = []
    certificates: list[dict[str, Any]] = []

    for s in statements:
        if not isinstance(s, dict):
            continue
        sid = str(s.get("id"))
        kind = s.get("kind")

        if kind == "identity":
            identities.append(s)
            for field in ("subject", "control_domain", "model_lineage", "runtime_origin"):
                if not s.get(field):
                    errors.append(issue("V055", f"identity missing {field}", sid))

        elif kind == "identity_attestation":
            attestations.append(s)
            identity_id = ref_id(s.get("identity"))
            identity = by_id.get(identity_id) if identity_id else None

            if identity is None or identity.get("kind") != "identity":
                errors.append(issue("V056", "attestation must reference an identity", sid))
            if s.get("issuer") not in TRUSTED_IDENTITY_ISSUERS:
                errors.append(issue("V056", "attestation issuer is not trusted", sid))
            if s.get("status") != "valid":
                errors.append(issue("V056", "attestation status must be valid", sid))
            try:
                start = parse_time(str(s.get("valid_from")))
                end = parse_time(str(s.get("valid_until")))
                if end < start:
                    errors.append(issue("V056", "attestation validity window is inverted", sid))
            except ValueError:
                errors.append(issue("V056", "attestation has invalid validity timestamp", sid))

        elif kind == "attestation_revocation":
            target_id = ref_id(s.get("target"))
            target = by_id.get(target_id) if target_id else None
            if target is None or target.get("kind") != "identity_attestation":
                errors.append(issue("V057", "revocation target must be an attestation", sid))
            else:
                if s.get("by") != target.get("issuer"):
                    errors.append(issue("V057", "attestation revoker must match issuer", sid))
                rt = statement_time(s)
                if rt is None:
                    errors.append(issue("V057", "attestation revocation needs valid time", sid))
                else:
                    try:
                        start = parse_time(str(target.get("valid_from")))
                        if rt < start:
                            errors.append(issue("V057", "attestation cannot be revoked before validity starts", sid))
                    except ValueError:
                        pass

        elif kind == "evidence_provenance":
            provenance_records.append(s)
            identity_id = ref_id(s.get("source_identity"))
            attestation_id = ref_id(s.get("attestation"))
            identity = by_id.get(identity_id) if identity_id else None
            attestation = by_id.get(attestation_id) if attestation_id else None

            if identity is None or identity.get("kind") != "identity":
                errors.append(issue("V058", "evidence provenance source_identity is invalid", sid))
            if attestation is None or attestation.get("kind") != "identity_attestation":
                errors.append(issue("V058", "evidence provenance attestation is invalid", sid))
            elif ref_id(attestation.get("identity")) != identity_id:
                errors.append(issue("V058", "evidence provenance attestation does not bind source identity", sid))

            pt = statement_time(s)
            if pt is None:
                errors.append(issue("V058", "evidence provenance requires valid at timestamp", sid))
            elif attestation_id is not None and not attestation_active(doc, attestation_id, pt):
                errors.append(issue("V058", "evidence provenance uses inactive attestation", sid))

            parent = s.get("parent")
            if parent != "none":
                parent_id = ref_id(parent)
                parent_obj = by_id.get(parent_id) if parent_id else None
                if parent_obj is None or parent_obj.get("kind") != "evidence_provenance":
                    errors.append(issue("V058", "evidence provenance parent is invalid", sid))

        elif kind == "vote":
            votes.append(s)
            identity_id = ref_id(s.get("identity"))
            attestation_id = ref_id(s.get("attestation"))
            provenance_id = ref_id(s.get("provenance"))
            identity = by_id.get(identity_id) if identity_id else None
            attestation = by_id.get(attestation_id) if attestation_id else None
            provenance = by_id.get(provenance_id) if provenance_id else None
            vt = statement_time(s)

            if identity is None or identity.get("kind") != "identity":
                errors.append(issue("V059", "vote identity is invalid", sid))
            else:
                if s.get("voter") != identity.get("subject"):
                    errors.append(issue("V059", "vote voter does not match identity subject", sid))
                if s.get("independence") != identity.get("control_domain"):
                    errors.append(issue("V059", "declared independence must match attested control_domain", sid))

            if attestation is None or attestation.get("kind") != "identity_attestation":
                errors.append(issue("V059", "vote attestation is invalid", sid))
            elif ref_id(attestation.get("identity")) != identity_id:
                errors.append(issue("V059", "vote attestation does not bind vote identity", sid))
            elif vt is not None and attestation_id is not None and not attestation_active(doc, attestation_id, vt):
                errors.append(issue("V059", "vote uses inactive attestation", sid))

            if provenance is None or provenance.get("kind") != "evidence_provenance":
                errors.append(issue("V060", "vote provenance is invalid", sid))
            else:
                if provenance.get("evidence_hash") != s.get("evidence_hash"):
                    errors.append(issue("V060", "vote evidence_hash does not match provenance", sid))
                if ref_id(provenance.get("source_identity")) != identity_id:
                    errors.append(issue("V060", "vote provenance source identity does not match voter identity", sid))

        elif kind == "quorum_policy":
            evidence_min = s.get("evidence_min")
            threshold = s.get("threshold")
            if (
                not isinstance(evidence_min, int)
                or isinstance(evidence_min, bool)
                or evidence_min <= 0
                or (
                    isinstance(threshold, int)
                    and not isinstance(threshold, bool)
                    and evidence_min > threshold
                )
            ):
                errors.append(issue("V061", "quorum evidence_min is invalid", sid))

        elif kind == "finality_certificate":
            certificates.append(s)

    # Provenance cycle detection.
    parent_map: dict[str, str] = {}
    for record in provenance_records:
        rid = str(record.get("id"))
        parent_id = ref_id(record.get("parent"))
        if parent_id:
            parent_map[rid] = parent_id

    for start in list(parent_map):
        seen: set[str] = set()
        node = start
        while node in parent_map:
            if node in seen:
                errors.append(issue("V062", f"evidence provenance cycle at [{node}]"))
                break
            seen.add(node)
            node = parent_map[node]

    # Certificate-level attested independence and evidence-root checks.
    for cert in certificates:
        sid = str(cert.get("id"))
        quorum_id = ref_id(cert.get("quorum"))
        quorum = by_id.get(quorum_id) if quorum_id else None
        if quorum is None or quorum.get("kind") != "quorum_policy":
            continue

        vote_ids = csv_values(cert.get("votes"))
        selected_votes = [
            by_id[vote_id]
            for vote_id in vote_ids
            if vote_id in by_id and by_id[vote_id].get("kind") == "vote"
        ]

        control_domains: set[str] = set()
        model_lineages: set[str] = set()
        runtime_origins: set[str] = set()
        evidence_roots: set[tuple[str, str]] = set()

        for vote in selected_votes:
            if vote.get("decision") != "approve":
                continue

            identity_id = ref_id(vote.get("identity"))
            identity = by_id.get(identity_id) if identity_id else None
            if isinstance(identity, dict) and identity.get("kind") == "identity":
                control_domains.add(str(identity.get("control_domain", "")))
                model_lineages.add(str(identity.get("model_lineage", "")))
                runtime_origins.add(str(identity.get("runtime_origin", "")))

            provenance_id = ref_id(vote.get("provenance"))
            if provenance_id:
                root = evidence_root_fingerprint(doc, provenance_id)
                if root is not None:
                    evidence_roots.add(root)

        independence_min = quorum.get("independence_min")
        evidence_min = quorum.get("evidence_min")

        if (
            isinstance(independence_min, int)
            and not isinstance(independence_min, bool)
            and (
                len(control_domains) < independence_min
                or len(model_lineages) < independence_min
                or len(runtime_origins) < independence_min
            )
        ):
            errors.append(
                issue(
                    "V063",
                    "certificate does not meet attested control/model/runtime independence threshold",
                    sid,
                )
            )

        if (
            isinstance(evidence_min, int)
            and not isinstance(evidence_min, bool)
            and len(evidence_roots) < evidence_min
        ):
            errors.append(
                issue(
                    "V064",
                    "certificate does not meet independent evidence-root threshold",
                    sid,
                )
            )

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "conflicts": conflicts,
        "authority_epoch": base.get("authority_epoch", 0),
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
