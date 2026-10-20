#!/usr/bin/env python3
"""Bridge-0 v0.4 delegation/revocation/expiry/replay tests."""

import unittest
from datetime import datetime, timezone

from authority_engine_v0_4 import authority_active
from parser_v0_4 import parse_document
from renderer_v0_4 import render_document
from validator_v0_4 import validate_document


class AuthorityLifecycleTests(unittest.TestCase):
    def assert_round_trip_valid(self, source):
        first = parse_document(source)
        r1 = validate_document(first)
        self.assertTrue(r1["valid"], r1["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        r2 = validate_document(second)
        self.assertTrue(r2["valid"], r2["errors"])
        self.assertEqual(first, second)
        return second

    def test_grant_round_trip(self):
        self.assert_round_trip_valid(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1 "
            "valid_until=2026-10-31T23:59:59Z"
        )

    def test_narrow_delegation_round_trip(self):
        self.assert_round_trip_valid(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "→ [D1] delegate parent=[P1] from=agent_a to=agent_b action=read "
            "resource=repo scope=/docs/team/** at=2026-10-02T00:10:00Z epoch=2\n"
        )

    def test_broader_scope_delegation_rejected(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/team/** at=2026-10-02T00:00:00Z epoch=1\n"
            "→ [D1] delegate parent=[P1] from=agent_a to=agent_b action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:10:00Z epoch=2\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V030" for e in result["errors"]))

    def test_action_change_delegation_rejected(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "→ [D1] delegate parent=[P1] from=agent_a to=agent_b action=write "
            "resource=repo scope=/docs/team/** at=2026-10-02T00:10:00Z epoch=2\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V030" for e in result["errors"]))

    def test_delegation_cannot_outlive_parent(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1 "
            "valid_until=2026-10-10T00:00:00Z\n"
            "→ [D1] delegate parent=[P1] from=agent_a to=agent_b action=read "
            "resource=repo scope=/docs/team/** at=2026-10-02T00:10:00Z epoch=2 "
            "valid_until=2026-10-11T00:00:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V030" for e in result["errors"]))

    def test_root_revocation_cascades_to_delegate(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "→ [D1] delegate parent=[P1] from=agent_a to=agent_b action=read "
            "resource=repo scope=/docs/team/** at=2026-10-02T00:10:00Z epoch=2\n"
            "× [R1] revoke target=[P1] by=human_owner at=2026-10-02T01:00:00Z epoch=3\n"
        )
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        after = datetime(2026, 10, 2, 1, 1, tzinfo=timezone.utc)
        self.assertFalse(authority_active(doc, "D1", after))

    def test_historical_replay_before_revocation_is_valid(self):
        self.assert_round_trip_valid(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "△ [C1] finding = true\n"
            "→ [H1] handoff from=agent_a to=agent_b artifact=[C1] "
            "scope=review state=preserve provenance=preserve\n"
            "→ [Y1] replay target=[H1] authority=[P1] "
            "at=2026-10-02T00:30:00Z epoch=1\n"
            "× [R1] revoke target=[P1] by=human_owner "
            "at=2026-10-02T01:00:00Z epoch=2\n"
        )

    def test_replay_after_revocation_rejected(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "△ [C1] finding = true\n"
            "→ [H1] handoff from=agent_a to=agent_b artifact=[C1] "
            "scope=review state=preserve provenance=preserve\n"
            "× [R1] revoke target=[P1] by=human_owner "
            "at=2026-10-02T01:00:00Z epoch=2\n"
            "→ [Y1] replay target=[H1] authority=[P1] "
            "at=2026-10-02T01:10:00Z epoch=2\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V032" for e in result["errors"]))

    def test_stale_replay_epoch_rejected(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "△ [C1] finding = true\n"
            "× [R1] revoke target=[P1] by=human_owner "
            "at=2026-10-02T01:00:00Z epoch=2\n"
            "→ [Y1] replay target=[C1] authority=[P1] "
            "at=2026-10-02T01:10:00Z epoch=1\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        rules = {e["rule"] for e in result["errors"]}
        self.assertIn("V034", rules)

    def test_expired_grant_replay_rejected(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1 "
            "valid_until=2026-10-02T00:30:00Z\n"
            "△ [C1] finding = true\n"
            "→ [Y1] replay target=[C1] authority=[P1] "
            "at=2026-10-02T00:31:00Z epoch=1\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V032" for e in result["errors"]))

    def test_child_revocation_does_not_revoke_parent(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "→ [D1] delegate parent=[P1] from=agent_a to=agent_b action=read "
            "resource=repo scope=/docs/team/** at=2026-10-02T00:10:00Z epoch=2\n"
            "× [R1] revoke target=[D1] by=human_owner "
            "at=2026-10-02T01:00:00Z epoch=3\n"
        )
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        after = datetime(2026, 10, 2, 1, 1, tzinfo=timezone.utc)
        self.assertTrue(authority_active(doc, "P1", after))
        self.assertFalse(authority_active(doc, "D1", after))

    def test_wrong_revoker_rejected(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "× [R1] revoke target=[P1] by=agent_a "
            "at=2026-10-02T01:00:00Z epoch=2\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V031" for e in result["errors"]))

    def test_stale_snapshot_requires_external_epoch(self):
        stale = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
        )
        local_only = validate_document(stale)
        self.assertTrue(local_only["valid"])

        checked_against_runtime = validate_document(stale, expected_epoch=2)
        self.assertFalse(checked_against_runtime["valid"])
        self.assertTrue(
            any(e["rule"] == "V033" for e in checked_against_runtime["errors"])
        )

    def test_new_grant_after_revocation_does_not_reactivate_old_id(self):
        doc = parse_document(
            "! [P1] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T00:00:00Z epoch=1\n"
            "× [R1] revoke target=[P1] by=human_owner "
            "at=2026-10-02T01:00:00Z epoch=2\n"
            "! [P2] grant grantor=human_owner actor=agent_a action=read "
            "resource=repo scope=/docs/** at=2026-10-02T02:00:00Z epoch=3\n"
        )
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        after = datetime(2026, 10, 2, 2, 1, tzinfo=timezone.utc)
        self.assertFalse(authority_active(doc, "P1", after))
        self.assertTrue(authority_active(doc, "P2", after))

    def test_twenty_level_delegation_chain_then_root_revoke(self):
        lines = [
            "! [P1] grant grantor=human_owner actor=agent_0 action=read "
            "resource=repo scope=/** at=2026-10-02T00:00:00Z epoch=1"
        ]
        parent = "P1"
        for i in range(1, 21):
            minute = i
            child = f"D{i}"
            lines.append(
                f"→ [{child}] delegate parent=[{parent}] from=agent_{i-1} "
                f"to=agent_{i} action=read resource=repo "
                f"scope=/level_{i}/** at=2026-10-02T00:{minute:02d}:00Z epoch={i+1}"
            )
            # After first narrowing, keep exact child scope to avoid broadening.
            if i == 1:
                lines[-1] = (
                    f"→ [{child}] delegate parent=[{parent}] from=agent_{i-1} "
                    f"to=agent_{i} action=read resource=repo "
                    f"scope=/level_1/** at=2026-10-02T00:{minute:02d}:00Z epoch={i+1}"
                )
            elif i > 1:
                lines[-1] = (
                    f"→ [{child}] delegate parent=[{parent}] from=agent_{i-1} "
                    f"to=agent_{i} action=read resource=repo "
                    f"scope=/level_1/** at=2026-10-02T00:{minute:02d}:00Z epoch={i+1}"
                )
            parent = child
        lines.append(
            "× [R1] revoke target=[P1] by=human_owner "
            "at=2026-10-02T01:00:00Z epoch=22"
        )
        doc = parse_document("\n".join(lines))
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        after = datetime(2026, 10, 2, 1, 1, tzinfo=timezone.utc)
        self.assertFalse(authority_active(doc, "D20", after))


if __name__ == "__main__":
    unittest.main()
