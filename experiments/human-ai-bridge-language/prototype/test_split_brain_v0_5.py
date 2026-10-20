#!/usr/bin/env python3
"""Bridge-0 v0.5 split-brain / reconciliation tests."""

import itertools
import unittest

from parser_v0_5 import parse_document
from renderer_v0_5 import render_document
from validator_v0_5 import validate_document


class SplitBrainTests(unittest.TestCase):
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

    def test_equivalent_siblings_need_no_conflict(self):
        self.assert_round_trip_valid(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority "
            "state_hash=h1 at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=B parent=[S0] seq=1 domain=authority "
            "state_hash=h1 at=2026-10-02T00:01:00Z\n"
        )

    def test_divergence_without_conflict_is_rejected(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority "
            "state_hash=ha at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=B parent=[S0] seq=1 domain=authority "
            "state_hash=hb at=2026-10-02T00:01:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V036" for e in result["errors"]))

    def test_declared_conflict_round_trip(self):
        doc = self.assert_round_trip_valid(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority "
            "state_hash=ha at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=B parent=[S0] seq=1 domain=authority "
            "state_hash=hb at=2026-10-02T00:01:00Z\n"
            "◆ [CF1] conflict left=[SA] right=[SB] domain=authority status=open\n"
        )
        result = validate_document(doc)
        self.assertEqual(
            len([c for c in result["conflicts"] if c["rule"] == "V036"]),
            1,
        )

    def test_false_conflict_rejected(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority "
            "state_hash=h1 at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=B parent=[S0] seq=1 domain=authority "
            "state_hash=h1 at=2026-10-02T00:01:00Z\n"
            "◆ [CF1] conflict left=[SA] right=[SB] domain=authority status=open\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V037" for e in result["errors"]))

    def test_last_writer_merge_is_rejected(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority "
            "state_hash=ha at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=B parent=[S0] seq=1 domain=authority "
            "state_hash=hb at=2026-10-02T00:01:00Z\n"
            "◆ [CF1] conflict left=[SA] right=[SB] domain=authority status=open\n"
            "→ [M1] merge left=[SA] right=[SB] conflict=[CF1] "
            "strategy=last_writer result_hash=hm at=2026-10-02T00:02:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V039" for e in result["errors"]))

    def test_explicit_merge_round_trip(self):
        self.assert_round_trip_valid(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority "
            "state_hash=ha at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=B parent=[S0] seq=1 domain=authority "
            "state_hash=hb at=2026-10-02T00:01:00Z\n"
            "◆ [CF1] conflict left=[SA] right=[SB] domain=authority status=open\n"
            "→ [M1] merge left=[SA] right=[SB] conflict=[CF1] "
            "strategy=explicit result_hash=hm at=2026-10-02T00:02:00Z\n"
        )

    def test_divergent_branch_cannot_be_finalized_directly(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority "
            "state_hash=ha at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=B parent=[S0] seq=1 domain=authority "
            "state_hash=hb at=2026-10-02T00:01:00Z\n"
            "◆ [CF1] conflict left=[SA] right=[SB] domain=authority status=open\n"
            "✓ [F1] final target=[SA] by=control_plane term=1 "
            "at=2026-10-02T00:02:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V041" for e in result["errors"]))

    def test_merge_can_receive_finality(self):
        self.assert_round_trip_valid(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=A parent=[S0] seq=1 domain=authority "
            "state_hash=ha at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=B parent=[S0] seq=1 domain=authority "
            "state_hash=hb at=2026-10-02T00:01:00Z\n"
            "◆ [CF1] conflict left=[SA] right=[SB] domain=authority status=open\n"
            "→ [M1] merge left=[SA] right=[SB] conflict=[CF1] "
            "strategy=explicit result_hash=hm at=2026-10-02T00:02:00Z\n"
            "✓ [F1] final target=[M1] by=control_plane term=1 "
            "at=2026-10-02T00:03:00Z\n"
        )

    def test_agent_cannot_self_finalize(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "✓ [F1] final target=[S0] by=agent_a term=1 "
            "at=2026-10-02T00:01:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V040" for e in result["errors"]))

    def test_execution_requires_matching_finality(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "→ [X1] execute actor=agent_a action=deploy state=[S0] "
            "finality=[F404] at=2026-10-02T00:02:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V042" for e in result["errors"]))

    def test_execution_after_finality_round_trip(self):
        self.assert_round_trip_valid(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "✓ [F1] final target=[S0] by=control_plane term=1 "
            "at=2026-10-02T00:01:00Z\n"
            "→ [X1] execute actor=agent_a action=deploy state=[S0] "
            "finality=[F1] at=2026-10-02T00:02:00Z\n"
        )

    def test_execution_cannot_precede_finality(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "✓ [F1] final target=[S0] by=control_plane term=1 "
            "at=2026-10-02T00:02:00Z\n"
            "→ [X1] execute actor=agent_a action=deploy state=[S0] "
            "finality=[F1] at=2026-10-02T00:01:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V042" for e in result["errors"]))

    def test_duplicate_finality_term_rejected(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z\n"
            "✓ [F1] final target=[S0] by=control_plane term=1 "
            "at=2026-10-02T00:01:00Z\n"
            "✓ [F2] final target=[S0] by=control_plane term=1 "
            "at=2026-10-02T00:02:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V043" for e in result["errors"]))

    def test_twelve_way_fork_requires_all_pair_conflicts(self):
        lines = [
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=h0 at=2026-10-02T00:00:00Z"
        ]
        ids = []
        for i in range(12):
            sid = f"S{i+1}"
            ids.append(sid)
            lines.append(
                f"○ [{sid}] snapshot branch=b{i+1} parent=[S0] seq=1 "
                f"domain=authority state_hash=h{i+1} "
                "at=2026-10-02T00:01:00Z"
            )

        conflict_count = 0
        for left, right in itertools.combinations(ids, 2):
            conflict_count += 1
            lines.append(
                f"◆ [CF{conflict_count}] conflict left=[{left}] right=[{right}] "
                "domain=authority status=open"
            )

        doc = parse_document("\n".join(lines))
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        split = [c for c in result["conflicts"] if c["rule"] == "V036"]
        self.assertEqual(len(split), 66)

    def test_concurrent_revoke_action_requires_reconciliation(self):
        doc = parse_document(
            "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
            "state_hash=grant_active at=2026-10-02T00:00:00Z\n"
            "○ [SA] snapshot branch=revoke_branch parent=[S0] seq=1 domain=authority "
            "state_hash=grant_revoked at=2026-10-02T00:01:00Z\n"
            "○ [SB] snapshot branch=action_branch parent=[S0] seq=1 domain=authority "
            "state_hash=action_pending at=2026-10-02T00:01:00Z\n"
            "◆ [CF1] conflict left=[SA] right=[SB] domain=authority status=open\n"
            "✓ [F1] final target=[SB] by=control_plane term=1 "
            "at=2026-10-02T00:02:00Z\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V041" for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
