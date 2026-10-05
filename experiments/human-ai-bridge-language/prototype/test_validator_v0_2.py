#!/usr/bin/env python3

import unittest

from parser_v0_2 import parse_document
from validator_v0_2 import validate_document


class ValidatorTests(unittest.TestCase):
    def test_valid_reference(self):
        doc = parse_document(
            "△ [C1] delay.cause = supplier_failure\n"
            "◆ [V1] log_17 supports [C1]\n"
        )
        result = validate_document(doc)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_missing_evidence_target(self):
        doc = parse_document("◆ [V1] log_17 supports [C404]")
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"][0]["rule"], "V004")

    def test_conflict_is_preserved_not_error(self):
        doc = parse_document(
            "△ [C1] pressure = high\n"
            "◆ [V1] sensor_A supports [C1]\n"
            "◆ [V2] sensor_B opposes [C1]\n"
        )
        result = validate_document(doc)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["conflicts"]), 1)
        self.assertEqual(result["conflicts"][0]["rule"], "V007")

    def test_missing_verification_target(self):
        doc = parse_document("✓ [K1] [C9] verified_by check")
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"][0]["rule"], "V012")

    def test_meta_claim_does_not_mutate_embedded_claim(self):
        doc = parse_document(
            "△ [C1] component.safe = true\n"
            "■ [C2] agent_A asserted [C1]\n"
        )
        result = validate_document(doc)
        self.assertTrue(result["valid"])
        self.assertEqual(
            doc["statements"][0]["epistemic_state"],
            "hypothesis",
        )
        self.assertTrue(any(w["rule"] == "V006" for w in result["warnings"]))

    def test_relation_class_mismatch_rejected(self):
        doc = {
            "language": "Bridge-0",
            "version": "0.2",
            "statements": [
                {
                    "id": "C1",
                    "kind": "claim",
                    "epistemic_state": "fact",
                    "subject": "X",
                    "predicate": "causes",
                    "object": "Y",
                    "relation_class": "descriptive",
                }
            ],
        }
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertEqual(result["errors"][0]["rule"], "V008")


if __name__ == "__main__":
    unittest.main()
