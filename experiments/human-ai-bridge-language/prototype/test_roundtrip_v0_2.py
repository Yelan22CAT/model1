#!/usr/bin/env python3
"""Bridge-0 semantic round-trip tests v0.2."""

import copy
import unittest

from parser_v0_2 import BridgeParseError, parse_document
from renderer_v0_2 import render_document
from validator_v0_2 import validate_document


def semantic_projection(doc):
    """Drop presentation-only fields before equality comparison."""
    out = copy.deepcopy(doc)
    out["source_language"] = None
    out["labels"] = {}
    return out


class RoundTripTests(unittest.TestCase):
    def assert_round_trip(self, source):
        first = parse_document(source)
        self.assertTrue(validate_document(first)["valid"])

        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertTrue(validate_document(second)["valid"])

        self.assertEqual(
            semantic_projection(first),
            semantic_projection(second),
            msg=f"Round trip changed semantics.\nRendered:\n{rendered}",
        )

    def test_basic_claims(self):
        self.assert_round_trip(
            "○ [E1] agent\n"
            "■ [C1] agent.can_prepare = true\n"
            "△ [C2] delay.cause = supplier_failure\n"
            "? [C3] delivery_date\n"
        )

    def test_meta_claim(self):
        self.assert_round_trip(
            "△ [C1] component.safe = true\n"
            "■ [C2] agent_A asserted [C1]\n"
        )

    def test_conflicting_evidence(self):
        first = parse_document(
            "△ [C1] pressure = high\n"
            "◆ [V1] sensor_A supports [C1]\n"
            "◆ [V2] sensor_B opposes [C1]\n"
        )
        result = validate_document(first)
        self.assertEqual(len(result["conflicts"]), 1)

        rendered = render_document(first)
        second = parse_document(rendered)
        result2 = validate_document(second)
        self.assertEqual(len(result2["conflicts"]), 1)
        self.assertEqual(
            semantic_projection(first),
            semantic_projection(second),
        )

    def test_action_guard_verification_time(self):
        self.assert_round_trip(
            "→ [A1] agent prepare_change component\n"
            "! [G1] release requires human_owner.approval\n"
            "✓ [K1] [A1] verified_by dry_run\n"
            "⏱ [T1] source_v2.valid_from = 2026-10-01T00:00:00Z\n"
            "× [F1] agent self_merge\n"
        )

    def test_number_and_unit(self):
        self.assert_round_trip(
            "■ [C1] invoice.total = 4280 CAD\n"
            "■ [C2] confidence = 0.72\n"
        )

    def test_tool_failure_world_unknown(self):
        self.assert_round_trip(
            "■ [C1] lookup_tool.call_status = failed\n"
            "? [C2] target_record.exists\n"
        )

    def test_association_not_causation(self):
        self.assert_round_trip(
            "■ [C1] X associated_with Y\n"
            "△ [C2] X causes Y\n"
        )


class NegativeSyntaxTests(unittest.TestCase):
    def assert_rejected(self, source):
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_mixed_fact_unknown(self):
        self.assert_rejected("■ [C1] delivery_date = ?")

    def test_unknown_with_value(self):
        self.assert_rejected("? [C1] delivery_date = 2026-10-10")

    def test_missing_id(self):
        self.assert_rejected("■ delivery_date = tomorrow")

    def test_unknown_relation(self):
        self.assert_rejected("■ [C1] X probably_means Y")

    def test_trailing_tokens(self):
        self.assert_rejected("→ [A1] agent deploy target extra")

    def test_inline_comment_not_accepted(self):
        self.assert_rejected("■ [C1] a = true # inline comment")

    def test_malformed_reference(self):
        self.assert_rejected("◆ [V1] log supports [C 1]")

    def test_unregistered_marker(self):
        self.assert_rejected("★ [C1] a = true")


if __name__ == "__main__":
    unittest.main()
