#!/usr/bin/env python3
"""Bridge-0 v0.3 authority-drift adversarial tests."""

import copy
import unittest

from parser_v0_3 import parse_document
from renderer_v0_3 import render_document
from validator_v0_3 import validate_document


class AuthorityDriftTests(unittest.TestCase):
    def round_trip(self, source):
        first = parse_document(source)
        self.assertTrue(validate_document(first)["valid"])
        second = parse_document(render_document(first))
        self.assertTrue(validate_document(second)["valid"])
        return first, second

    def test_handoff_does_not_delegate_permission(self):
        first, second = self.round_trip(
            "△ [C1] finding = true\n"
            "! [P1] permission actor=executor action=read resource=repo scope=/docs/**\n"
            "→ [H1] handoff from=executor to=analyst artifact=[C1] "
            "scope=analysis state=preserve provenance=preserve\n"
        )
        permissions = [s for s in second["statements"] if s["kind"] == "permission"]
        self.assertEqual(len(permissions), 1)
        self.assertEqual(permissions[0]["actor"], "executor")
        self.assertFalse(any(p["actor"] == "analyst" for p in permissions))

    def test_irreversible_transition_wrong_guard_kind_rejected(self):
        doc = parse_document(
            "■ [C1] approval = true\n"
            "→ [S1] transition subject=payment.state from=pending to=sent "
            "irreversible=true when=[C1] authority=human_owner\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V023" for e in result["errors"]))

    def test_irreversible_transition_authority_removal_rejected(self):
        doc = parse_document(
            "! [G1] transfer requires human_owner.approval\n"
            "→ [S1] transition subject=payment.state from=pending to=sent "
            "irreversible=true when=[G1] authority=human_owner\n"
        )
        mutated = copy.deepcopy(doc)
        transition = next(s for s in mutated["statements"] if s["id"] == "S1")
        del transition["authority"]
        result = validate_document(mutated)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V023" for e in result["errors"]))

    def test_handoff_provenance_reset_rejected(self):
        doc = parse_document(
            "△ [C1] finding = true\n"
            "→ [H1] handoff from=a to=b artifact=[C1] scope=review "
            "state=preserve provenance=reset\n"
        )
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V022" for e in result["errors"]))

    def test_provenance_does_not_change_parent_epistemic_state(self):
        first, second = self.round_trip(
            "△ [C1] source_claim = true\n"
            "△ [C2] derived_claim = true\n"
            "◆ [PV1] provenance artifact=[C2] parent=[C1] actor=analyst transform=derive\n"
        )
        parent = next(s for s in second["statements"] if s["id"] == "C1")
        child = next(s for s in second["statements"] if s["id"] == "C2")
        self.assertEqual(parent["epistemic_state"], "hypothesis")
        self.assertEqual(child["epistemic_state"], "hypothesis")

    def test_superseded_source_remains_addressable(self):
        first, second = self.round_trip(
            "○ [E1] source_v1\n"
            "○ [E2] source_v2\n"
            "■ [C1] source_v2 supersedes source_v1\n"
            "⏱ [T1] source_v1.valid_until = 2026-09-30T23:59:59Z\n"
            "⏱ [T2] source_v2.valid_from = 2026-10-01T00:00:00Z\n"
        )
        ids = {s["id"] for s in second["statements"]}
        self.assertIn("E1", ids)
        self.assertIn("E2", ids)
        self.assertIn("C1", ids)

    def test_conflict_survives_handoff(self):
        first, second = self.round_trip(
            "△ [C1] pressure = high\n"
            "◆ [V1] sensor_A supports [C1]\n"
            "◆ [V2] sensor_B opposes [C1]\n"
            "→ [H1] handoff from=analyst to=judge artifact=[C1] "
            "scope=review state=preserve provenance=preserve\n"
        )
        result = validate_document(second)
        self.assertEqual(len(result["conflicts"]), 1)
        self.assertEqual(result["conflicts"][0]["target"], "C1")

    def test_fifty_handoffs_preserve_one_hypothesis(self):
        lines = ["△ [C1] system.safe = true"]
        for i in range(1, 51):
            lines.append(
                f"→ [H{i}] handoff from=agent_{i} to=agent_{i+1} "
                "artifact=[C1] scope=review state=preserve provenance=preserve"
            )
        first, second = self.round_trip("\n".join(lines))
        claim = next(s for s in second["statements"] if s["id"] == "C1")
        self.assertEqual(claim["epistemic_state"], "hypothesis")
        handoffs = [s for s in second["statements"] if s["kind"] == "handoff"]
        self.assertEqual(len(handoffs), 50)

    def test_hundred_permissions_do_not_merge(self):
        lines = []
        for i in range(1, 101):
            lines.append(
                f"! [P{i}] permission actor=agent_{i} action=read "
                f"resource=repo scope=/team_{i}/**"
            )
        first, second = self.round_trip("\n".join(lines))
        permissions = [s for s in second["statements"] if s["kind"] == "permission"]
        self.assertEqual(len(permissions), 100)
        self.assertEqual({p["actor"] for p in permissions}, {f"agent_{i}" for i in range(1, 101)})


if __name__ == "__main__":
    unittest.main()
