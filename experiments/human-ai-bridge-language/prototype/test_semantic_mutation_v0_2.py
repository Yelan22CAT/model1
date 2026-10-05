#!/usr/bin/env python3
"""Bridge-0 semantic mutation tests v0.2.

These tests check that meaning-changing mutations are observable rather than
being normalized away by parser/renderer/validator behavior.
"""

import copy
import unittest

from parser_v0_2 import parse_document
from renderer_v0_2 import render_document
from validator_v0_2 import validate_document


def semantic_core(doc):
    out = copy.deepcopy(doc)
    out["labels"] = {}
    out["source_language"] = None
    return out


class SemanticMutationTests(unittest.TestCase):
    def test_hypothesis_to_fact_is_detectable(self):
        original = parse_document("△ [C1] component.safe = true")
        mutated = copy.deepcopy(original)
        mutated["statements"][0]["epistemic_state"] = "fact"
        self.assertNotEqual(semantic_core(original), semantic_core(mutated))

    def test_association_to_causation_is_detectable(self):
        original = parse_document("■ [C1] X associated_with Y")
        mutated = copy.deepcopy(original)
        mutated["statements"][0]["predicate"] = "causes"
        mutated["statements"][0]["relation_class"] = "causal"
        self.assertNotEqual(semantic_core(original), semantic_core(mutated))

    def test_evidence_target_change_is_detectable(self):
        original = parse_document(
            "△ [C1] a = true\n"
            "△ [C2] b = true\n"
            "◆ [V1] source supports [C1]\n"
        )
        mutated = copy.deepcopy(original)
        mutated["statements"][2]["target"] = "C2"
        self.assertNotEqual(semantic_core(original), semantic_core(mutated))
        self.assertTrue(validate_document(mutated)["valid"])

    def test_missing_reference_is_rejected_by_validator(self):
        original = parse_document(
            "△ [C1] a = true\n"
            "◆ [V1] source supports [C1]\n"
        )
        mutated = copy.deepcopy(original)
        mutated["statements"][1]["target"] = "C404"
        result = validate_document(mutated)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V004" for e in result["errors"]))

    def test_localized_labels_do_not_change_surface_semantics(self):
        original = parse_document("? [C1] delivery_date")
        localized = copy.deepcopy(original)
        localized["labels"] = {
            "C1": {
                "en": "delivery date",
                "zh": "交付日期",
                "ja": "納品日",
            }
        }
        self.assertEqual(render_document(original), render_document(localized))
        self.assertEqual(semantic_core(original), semantic_core(localized))

    def test_conflict_survives_render_round_trip(self):
        original = parse_document(
            "△ [C1] pressure = high\n"
            "◆ [V1] sensor_A supports [C1]\n"
            "◆ [V2] sensor_B opposes [C1]\n"
        )
        first = validate_document(original)
        self.assertEqual(len(first["conflicts"]), 1)

        rendered = render_document(original)
        reparsed = parse_document(rendered)
        second = validate_document(reparsed)
        self.assertEqual(len(second["conflicts"]), 1)
        self.assertEqual(first["conflicts"][0]["target"], second["conflicts"][0]["target"])

    def test_meta_claim_does_not_promote_embedded_claim_after_round_trip(self):
        original = parse_document(
            "△ [C1] component.safe = true\n"
            "■ [C2] agent_A asserted [C1]\n"
        )
        rendered = render_document(original)
        reparsed = parse_document(rendered)
        c1 = next(s for s in reparsed["statements"] if s["id"] == "C1")
        self.assertEqual(c1["epistemic_state"], "hypothesis")

    def test_generated_claim_batch_round_trip(self):
        lines = []
        for i in range(1, 101):
            marker = "■" if i % 2 == 0 else "△"
            value = "true" if i % 3 else "false"
            lines.append(f"{marker} [C{i}] object_{i}.state = {value}")
        source = "\n".join(lines)

        original = parse_document(source)
        rendered = render_document(original)
        reparsed = parse_document(rendered)

        self.assertEqual(semantic_core(original), semantic_core(reparsed))
        self.assertTrue(validate_document(reparsed)["valid"])


if __name__ == "__main__":
    unittest.main()
