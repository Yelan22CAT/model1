#!/usr/bin/env python3
"""Bridge-0 v0.3 authority/provenance composition tests."""

import copy
import unittest

from parser_v0_3 import BridgeParseError, parse_document
from renderer_v0_3 import render_document
from validator_v0_3 import validate_document


def semantic(doc):
    out = copy.deepcopy(doc)
    out["labels"] = {}
    out["source_language"] = None
    return out


class StructuredSemanticsTests(unittest.TestCase):
    def assert_round_trip(self, source):
        first = parse_document(source)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        result2 = validate_document(second)
        self.assertTrue(result2["valid"], result2["errors"])
        self.assertEqual(semantic(first), semantic(second))
        return first

    def test_permission_tuple_round_trip(self):
        self.assert_round_trip(
            "! [P1] permission actor=agent action=read resource=repo "
            "scope=/docs/** condition=human_owner.approval "
            "valid_from=2026-10-01T00:00:00Z "
            "valid_until=2026-10-31T23:59:59Z"
        )

    def test_permission_scope_mutation_is_detectable(self):
        original = parse_document(
            "! [P1] permission actor=agent action=read resource=repo scope=/docs/**"
        )
        mutated = copy.deepcopy(original)
        mutated["statements"][0]["scope"] = "/**"
        self.assertNotEqual(semantic(original), semantic(mutated))

    def test_permission_action_mutation_is_detectable(self):
        original = parse_document(
            "! [P1] permission actor=agent action=read resource=repo scope=/docs/**"
        )
        mutated = copy.deepcopy(original)
        mutated["statements"][0]["action"] = "write"
        self.assertNotEqual(semantic(original), semantic(mutated))

    def test_permission_invalid_time_window_rejected(self):
        doc = parse_document(
            "! [P1] permission actor=agent action=read resource=repo "
            "scope=/docs/** valid_from=2026-11-01T00:00:00Z "
            "valid_until=2026-10-01T00:00:00Z"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V020" for e in result["errors"]))

    def test_handoff_round_trip_preserves_state_and_provenance(self):
        self.assert_round_trip(
            "△ [C1] component.safe = true\n"
            "→ [H1] handoff from=analyst to=judge artifact=[C1] "
            "scope=review state=preserve provenance=preserve transform=restatement\n"
        )

    def test_handoff_missing_artifact_rejected(self):
        doc = parse_document(
            "→ [H1] handoff from=analyst to=judge artifact=[C404] "
            "scope=review state=preserve provenance=preserve"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V021" for e in result["errors"]))

    def test_handoff_cannot_reset_epistemic_state(self):
        doc = parse_document(
            "△ [C1] component.safe = true\n"
            "→ [H1] handoff from=analyst to=judge artifact=[C1] "
            "scope=review state=reset provenance=preserve"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V022" for e in result["errors"]))

    def test_irreversible_transition_requires_guard_and_authority(self):
        doc = parse_document(
            "→ [S1] transition subject=payment.state from=pending to=sent irreversible=true"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        rules = {e["rule"] for e in result["errors"]}
        self.assertIn("V023", rules)

    def test_irreversible_transition_valid_with_guard_and_authority(self):
        self.assert_round_trip(
            "! [G1] transfer requires human_owner.approval\n"
            "→ [S1] transition subject=payment.state from=pending to=sent "
            "irreversible=true when=[G1] authority=human_owner\n"
        )

    def test_reversible_transition_does_not_require_authority(self):
        self.assert_round_trip(
            "→ [S1] transition subject=draft.state from=open to=saved irreversible=false"
        )

    def test_provenance_chain_round_trip(self):
        self.assert_round_trip(
            "△ [C1] source_claim = true\n"
            "△ [C2] derived_claim = true\n"
            "◆ [PV1] provenance artifact=[C2] parent=[C1] "
            "actor=analyst transform=derive time=2026-10-02T00:00:00Z\n"
        )

    def test_provenance_missing_parent_rejected(self):
        doc = parse_document(
            "△ [C2] derived_claim = true\n"
            "◆ [PV1] provenance artifact=[C2] parent=[C404] "
            "actor=analyst transform=derive"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V024" for e in result["errors"]))

    def test_provenance_cycle_rejected(self):
        doc = parse_document(
            "△ [C1] a = true\n"
            "△ [C2] b = true\n"
            "◆ [PV1] provenance artifact=[C1] parent=[C2] actor=agent transform=derive\n"
            "◆ [PV2] provenance artifact=[C2] parent=[C1] actor=agent transform=derive\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V025" for e in result["errors"]))

    def test_composed_agent_path(self):
        doc = self.assert_round_trip(
            "△ [C1] component.safe = true\n"
            "◆ [V1] limited_test supports [C1]\n"
            "! [P1] permission actor=executor action=read resource=repo scope=/tests/**\n"
            "→ [H1] handoff from=executor to=analyst artifact=[C1] "
            "scope=analysis state=preserve provenance=preserve transform=analyze\n"
            "△ [C2] component.release_ready = true\n"
            "◆ [PV1] provenance artifact=[C2] parent=[C1] actor=analyst transform=derive\n"
            "! [G1] release requires human_owner.approval\n"
            "→ [S1] transition subject=release.state from=pending to=released "
            "irreversible=true when=[G1] authority=human_owner\n"
        )
        c1 = next(s for s in doc["statements"] if s["id"] == "C1")
        self.assertEqual(c1["epistemic_state"], "hypothesis")

    def test_duplicate_structured_key_rejected(self):
        with self.assertRaises(BridgeParseError):
            parse_document(
                "! [P1] permission actor=agent actor=other action=read "
                "resource=repo scope=/docs/**"
            )


if __name__ == "__main__":
    unittest.main()
