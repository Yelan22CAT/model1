#!/usr/bin/env python3
"""Minimal tests for Bridge-0 parser prototype v0.2."""

import unittest

from parser_v0_2 import BridgeParseError, parse_document


class BridgeParserTests(unittest.TestCase):
    def test_fact_unknown_separation(self):
        doc = parse_document("? [C1] delivery_date")
        self.assertEqual(doc["statements"][0]["kind"], "unknown")

    def test_reject_fact_with_unknown_value(self):
        with self.assertRaises(BridgeParseError):
            parse_document("■ [C1] delivery_date = ?")

    def test_meta_claim_reference(self):
        doc = parse_document(
            "△ [C1] component.safe = true\n"
            "■ [C2] agent_A asserted [C1]\n"
        )
        c2 = doc["statements"][1]
        self.assertEqual(c2["predicate"], "asserted")
        self.assertEqual(c2["object"], {"ref": "C1"})
        self.assertEqual(doc["statements"][0]["epistemic_state"], "hypothesis")

    def test_evidence_reference(self):
        doc = parse_document(
            "△ [C1] delay.cause = supplier_failure\n"
            "◆ [V1] log_17 supports [C1]\n"
        )
        evidence = doc["statements"][1]
        self.assertEqual(evidence["target"], "C1")
        self.assertEqual(evidence["relation"], "supports")

    def test_duplicate_id_rejected(self):
        with self.assertRaises(BridgeParseError):
            parse_document(
                "■ [C1] a = true\n"
                "△ [C1] b = true\n"
            )

    def test_unknown_relation_rejected(self):
        with self.assertRaises(BridgeParseError):
            parse_document("■ [C1] X magically_means Y")

    def test_tool_failure_keeps_world_unknown(self):
        doc = parse_document(
            "■ [C1] lookup_tool.call_status = failed\n"
            "? [C2] target_record.exists\n"
        )
        self.assertEqual(doc["statements"][0]["value"], "failed")
        self.assertEqual(doc["statements"][1]["kind"], "unknown")

    def test_time_binding(self):
        doc = parse_document(
            "⏱ [T1] source_v2.valid_from = 2026-10-01T00:00:00Z"
        )
        self.assertEqual(
            doc["statements"][0]["timestamp"],
            "2026-10-01T00:00:00Z",
        )

    def test_action_and_guard(self):
        doc = parse_document(
            "→ [A1] agent transfer_funds payment_17\n"
            "! [G1] transfer_funds requires human_owner.approval\n"
        )
        self.assertEqual(doc["statements"][0]["kind"], "action")
        self.assertEqual(doc["statements"][1]["kind"], "guard")

    def test_localized_labels_are_not_parser_identity(self):
        doc = parse_document("? [C1] delivery_date")
        self.assertEqual(doc["statements"][0]["id"], "C1")
        self.assertEqual(doc["statements"][0]["path"], "delivery_date")


if __name__ == "__main__":
    unittest.main()
