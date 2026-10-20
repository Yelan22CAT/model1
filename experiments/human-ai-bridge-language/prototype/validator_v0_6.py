#!/usr/bin/env python3
"""Bridge-0 conflict-set / quorum validator v0.6.

v0.6 replaces pairwise conflict declarations for many-way divergence with
compact conflict sets and validates reconciliation proposals, independent
votes, finality certificates, and certificate-bound execution.

A quorum certificate is governance finality, not proof that a proposition is
true about the external world.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from typing import Any

from authority_engine_v0_4 import build_index
from validator_v0_3 import issue, parse_time, ref_id
from validator_v0_4 import validate_document as validate_v04


def statement_time(statement: dict[str, Any]):
    raw = statement.get("at")
    if not isinstance(raw, str):
        return None
    try:
        return parse_time(raw)
    except ValueError:
        return None


def csv_values(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    values = [item.strip() for item in raw.split(",")]
    return [item for item in values if item]


def snapshot_parent(snapshot: dict[str, Any]) -> str | None:
    parent = snapshot.get("parent")
    if parent == "none":
        return None
    return ref_id(parent)


def validate_document(
    doc: dict[str, Any],
    expected_epoch: int | None = None,
    trusted_finalizer: str = "control_plane",
) -> dict[str, Any]:
    base = validate_v04(doc, expected_epoch=expected_epoch)
    errors = list(base["errors"])
    warnings = list(base["warnings"])
    conflicts = list(base["conflicts"])

    statements = doc.get("statements")
    if not isinstance(statements, list):
        return base

    by_id = build_index(doc)

    snapshots: list[dict[str, Any]] = []
    conflict_sets: list[dict[str, Any]] = []
    proposals: list[dict[str, Any]] = []
    votes: list[dict[str, Any]] = []
    quorums: list[dict[str, Any]] = []
    certificates: list[dict[str, Any]] = []
    executions: list[dict[str, Any]] = []

    # Local validation and categorization.
    for s in statements:
        if not isinstance(s, dict):
            continue
        sid = str(s.get("id"))
        kind = s.get("kind")

        if kind == "snapshot":
            snapshots.append(s)
            seq = s.get("seq")
            if not isinstance(seq, int) or isinstance(seq, bool) or seq < 0:
                errors.append(issue("V044", "snapshot seq must be a non-negative integer", sid))
            if not s.get("branch") or not s.get("domain") or not s.get("state_hash"):
                errors.append(issue("V044", "snapshot requires branch, domain, and state_hash", sid))
            when = statement_time(s)
            if when is None:
                errors.append(issue("V044", "snapshot requires valid at timestamp", sid))

            parent = s.get("parent")
            if parent != "none":
                parent_id = ref_id(parent)
                parent_obj = by_id.get(parent_id) if parent_id else None
                if parent_obj is None or parent_obj.get("kind") != "snapshot":
                    errors.append(issue("V044", "snapshot parent must reference an existing snapshot", sid))
                else:
                    if s.get("domain") != parent_obj.get("domain"):
                        errors.append(issue("V044", "snapshot domain must match parent domain", sid))
                    pseq = parent_obj.get("seq")
                    if (
                        isinstance(seq, int)
                        and not isinstance(seq, bool)
                        and isinstance(pseq, int)
                        and not isinstance(pseq, bool)
                        and seq != pseq + 1
                    ):
                        errors.append(issue("V044", "snapshot seq must equal parent seq + 1", sid))
                    pt = statement_time(parent_obj)
                    if when is not None and pt is not None and when < pt:
                        errors.append(issue("V044", "snapshot cannot precede parent in time", sid))

        elif kind == "conflict_set":
            conflict_sets.append(s)
            members = csv_values(s.get("members"))
            if len(members) < 2:
                errors.append(issue("V045", "conflict_set needs at least two members", sid))
            if len(members) != len(set(members)):
                errors.append(issue("V045", "conflict_set members must be unique", sid))
            if s.get("status") != "open":
                errors.append(issue("V045", "v0.6 conflict_set status must be open", sid))

            member_objs = [by_id.get(mid) for mid in members]
            if any(obj is None or obj.get("kind") != "snapshot" for obj in member_objs):
                errors.append(issue("V045", "all conflict_set members must be existing snapshots", sid))
            elif member_objs:
                domains = {obj.get("domain") for obj in member_objs}
                parents = {snapshot_parent(obj) for obj in member_objs}
                seqs = {obj.get("seq") for obj in member_objs}
                hashes = {obj.get("state_hash") for obj in member_objs}
                if len(domains) != 1 or s.get("domain") not in domains:
                    errors.append(issue("V045", "conflict_set domain mismatch", sid))
                if len(parents) != 1 or len(seqs) != 1:
                    errors.append(issue("V045", "conflict_set members must be sibling snapshots", sid))
                if len(hashes) < 2:
                    errors.append(issue("V045", "conflict_set must contain real divergence", sid))

        elif kind == "reconciliation_proposal":
            proposals.append(s)
            conflict_id = ref_id(s.get("conflict_set"))
            conflict_obj = by_id.get(conflict_id) if conflict_id else None
            if conflict_obj is None or conflict_obj.get("kind") != "conflict_set":
                errors.append(issue("V047", "proposal must reference an existing conflict_set", sid))
            if s.get("strategy") != "explicit":
                errors.append(issue("V047", "automatic reconciliation is forbidden in v0.6", sid))
            if not s.get("result_hash"):
                errors.append(issue("V047", "proposal requires result_hash", sid))
            ptime = statement_time(s)
            if ptime is None:
                errors.append(issue("V047", "proposal requires valid at timestamp", sid))
            elif conflict_obj is not None:
                for member_id in csv_values(conflict_obj.get("members")):
                    member = by_id.get(member_id)
                    mt = statement_time(member) if isinstance(member, dict) else None
                    if mt is not None and ptime < mt:
                        errors.append(issue("V047", "proposal cannot precede conflict member", sid))

        elif kind == "quorum_policy":
            quorums.append(s)
            voters_list = csv_values(s.get("voters"))
            threshold = s.get("threshold")
            independence_min = s.get("independence_min")

            if len(voters_list) != len(set(voters_list)) or not voters_list:
                errors.append(issue("V048", "quorum voters must be unique and non-empty", sid))
            if (
                not isinstance(threshold, int)
                or isinstance(threshold, bool)
                or threshold <= 0
                or threshold > len(set(voters_list))
            ):
                errors.append(issue("V048", "quorum threshold is invalid", sid))
            if (
                not isinstance(independence_min, int)
                or isinstance(independence_min, bool)
                or independence_min <= 0
                or (
                    isinstance(threshold, int)
                    and not isinstance(threshold, bool)
                    and independence_min > threshold
                )
            ):
                errors.append(issue("V048", "quorum independence_min is invalid", sid))

        elif kind == "vote":
            votes.append(s)
            proposal_id = ref_id(s.get("proposal"))
            proposal_obj = by_id.get(proposal_id) if proposal_id else None
            if proposal_obj is None or proposal_obj.get("kind") != "reconciliation_proposal":
                errors.append(issue("V049", "vote must reference an existing proposal", sid))
            if s.get("decision") not in {"approve", "reject", "abstain"}:
                errors.append(issue("V049", "vote decision must be approve/reject/abstain", sid))
            if not s.get("voter") or not s.get("independence") or not s.get("evidence_hash"):
                errors.append(issue("V049", "vote requires voter, independence, and evidence_hash", sid))
            vtime = statement_time(s)
            if vtime is None:
                errors.append(issue("V049", "vote requires valid at timestamp", sid))
            elif proposal_obj is not None:
                ptime = statement_time(proposal_obj)
                if ptime is not None and vtime < ptime:
                    errors.append(issue("V049", "vote cannot precede proposal", sid))

        elif kind == "finality_certificate":
            certificates.append(s)
            proposal_id = ref_id(s.get("proposal"))
            quorum_id = ref_id(s.get("quorum"))
            proposal_obj = by_id.get(proposal_id) if proposal_id else None
            quorum_obj = by_id.get(quorum_id) if quorum_id else None

            if proposal_obj is None or proposal_obj.get("kind") != "reconciliation_proposal":
                errors.append(issue("V050", "certificate proposal reference is invalid", sid))
            if quorum_obj is None or quorum_obj.get("kind") != "quorum_policy":
                errors.append(issue("V050", "certificate quorum reference is invalid", sid))
            if s.get("issued_by") != trusted_finalizer:
                errors.append(issue("V050", "certificate issuer is not trusted finalizer", sid))

            term = s.get("term")
            if not isinstance(term, int) or isinstance(term, bool) or term <= 0:
                errors.append(issue("V050", "certificate term must be a positive integer", sid))

            ctime = statement_time(s)
            if ctime is None:
                errors.append(issue("V050", "certificate requires valid at timestamp", sid))

            vote_ids = csv_values(s.get("votes"))
            if len(vote_ids) != len(set(vote_ids)) or not vote_ids:
                errors.append(issue("V051", "certificate vote IDs must be unique and non-empty", sid))

            if quorum_obj is not None and proposal_obj is not None:
                allowed_voters = set(csv_values(quorum_obj.get("voters")))
                threshold = quorum_obj.get("threshold")
                independence_min = quorum_obj.get("independence_min")

                selected_votes: list[dict[str, Any]] = []
                for vote_id in vote_ids:
                    vote_obj = by_id.get(vote_id)
                    if vote_obj is None or vote_obj.get("kind") != "vote":
                        errors.append(issue("V051", f"certificate vote [{vote_id}] does not exist", sid))
                        continue
                    selected_votes.append(vote_obj)

                    if ref_id(vote_obj.get("proposal")) != proposal_id:
                        errors.append(issue("V051", "certificate contains vote for another proposal", sid))
                    if vote_obj.get("decision") != "approve":
                        errors.append(issue("V051", "certificate may count only approve votes", sid))
                    if vote_obj.get("voter") not in allowed_voters:
                        errors.append(issue("V051", "certificate contains unauthorized voter", sid))
                    vt = statement_time(vote_obj)
                    if ctime is not None and vt is not None and ctime < vt:
                        errors.append(issue("V051", "certificate cannot precede included vote", sid))

                unique_voters = {v.get("voter") for v in selected_votes if v.get("decision") == "approve"}
                unique_independence = {
                    v.get("independence")
                    for v in selected_votes
                    if v.get("decision") == "approve"
                }

                if (
                    isinstance(threshold, int)
                    and not isinstance(threshold, bool)
                    and len(unique_voters) < threshold
                ):
                    errors.append(issue("V052", "certificate does not meet voter threshold", sid))
                if (
                    isinstance(independence_min, int)
                    and not isinstance(independence_min, bool)
                    and len(unique_independence) < independence_min
                ):
                    errors.append(issue("V052", "certificate does not meet independence threshold", sid))

        elif kind == "execution":
            executions.append(s)

    # Detect divergent sibling groups in O(n)-style grouping rather than pairwise records.
    groups: dict[tuple[Any, Any, Any], list[dict[str, Any]]] = defaultdict(list)
    for s in snapshots:
        groups[(snapshot_parent(s), s.get("seq"), s.get("domain"))].append(s)

    divergent_groups: list[set[str]] = []
    for group in groups.values():
        if len(group) < 2:
            continue
        hashes = {s.get("state_hash") for s in group}
        if len(hashes) < 2:
            continue
        members = {str(s.get("id")) for s in group}
        divergent_groups.append(members)
        conflicts.append(
            {
                "rule": "V046",
                "members": sorted(members),
                "message": "many-way divergent sibling snapshots detected",
            }
        )

    declared_sets: dict[frozenset[str], str] = {}
    for s in conflict_sets:
        members = frozenset(csv_values(s.get("members")))
        declared_sets[members] = str(s.get("id"))

    for members in divergent_groups:
        key = frozenset(members)
        if key not in declared_sets:
            errors.append(
                issue(
                    "V046",
                    "divergent sibling group must be represented by one exact conflict_set",
                )
            )

    for members, sid in declared_sets.items():
        if set(members) not in divergent_groups:
            errors.append(issue("V045", "declared conflict_set does not match a divergent sibling group", sid))

    # Finality certificate terms must be unique and monotonic with time.
    ordered_certificates: list[tuple[Any, int, str]] = []
    seen_terms: dict[int, str] = {}
    for cert in certificates:
        term = cert.get("term")
        when = statement_time(cert)
        sid = str(cert.get("id"))
        if isinstance(term, int) and not isinstance(term, bool):
            if term in seen_terms:
                errors.append(issue("V053", f"duplicate certificate term {term}", sid))
            else:
                seen_terms[term] = sid
            if when is not None:
                ordered_certificates.append((when, term, sid))

    ordered_certificates.sort(key=lambda x: (x[0], x[1]))
    for (_, previous_term, _), (_, next_term, next_id) in zip(
        ordered_certificates,
        ordered_certificates[1:],
    ):
        if next_term <= previous_term:
            errors.append(issue("V053", "certificate term must increase with certificate time", next_id))

    # Certificate-bound execution.
    for execution in executions:
        sid = str(execution.get("id"))
        state_id = ref_id(execution.get("state"))
        cert_id = ref_id(execution.get("finality"))
        state_obj = by_id.get(state_id) if state_id else None
        cert_obj = by_id.get(cert_id) if cert_id else None

        if state_obj is None or state_obj.get("kind") != "reconciliation_proposal":
            errors.append(issue("V054", "v0.6 execution state must reference a reconciliation proposal", sid))
        if cert_obj is None or cert_obj.get("kind") != "finality_certificate":
            errors.append(issue("V054", "v0.6 execution requires a finality certificate", sid))
            continue
        if ref_id(cert_obj.get("proposal")) != state_id:
            errors.append(issue("V054", "execution certificate does not finalize execution state", sid))
        et = statement_time(execution)
        ct = statement_time(cert_obj)
        if et is None:
            errors.append(issue("V054", "execution requires valid at timestamp", sid))
        elif ct is not None and et < ct:
            errors.append(issue("V054", "execution cannot precede certificate", sid))

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
