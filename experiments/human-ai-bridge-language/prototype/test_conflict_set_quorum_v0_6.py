#!/usr/bin/env python3
"""Bridge-0 v0.6 conflict-set / quorum / certificate tests."""

import unittest

from parser_v0_6 import parse_document
from renderer_v0_6 import render_document
from validator_v0_6 import validate_document


ROOT = (
    "○ [S0] snapshot branch=root parent=none seq=0 domain=authority "
    "state_hash=h0 at=2026-10-02T00:00:00Z"
)


def fork(count: int) -> list[str]:
    lines = [ROOT]
    for i in range(1, count + 1):
        lines.append(
            f"○ [S{i}] snapshot branch=b{i} parent=[S0] seq=1 domain=authority "
            f"state_hash=h{i} at=2026-10-02T00:01:00Z"
        )
    return lines


def happy_path() -> str:
    lines = fork(5)
    lines += [
        "◆ [CS1] conflict_set members=S1,S2,S3,S4,S5 domain=authority status=open",
        "→ [P1] propose conflict_set=[CS1] strategy=explicit result_hash=hm "
        "at=2026-10-02T00:02:00Z",
        "! [Q1] quorum voters=validator_a,validator_b,validator_c,validator_d,validator_e "
        "threshold=3 independence_min=3",
        "◆ [V1] vote voter=validator_a proposal=[P1] decision=approve "
        "independence=model_family_a evidence_hash=ev1 at=2026-10-02T00:03:00Z",
        "◆ [V2] vote voter=validator_b proposal=[P1] decision=approve "
        "independence=model_family_b evidence_hash=ev2 at=2026-10-02T00:03:01Z",
        "◆ [V3] vote voter=validator_c proposal=[P1] decision=approve "
        "independence=human_review evidence_hash=ev3 at=2026-10-02T00:03:02Z",
        "✓ [FC1] certificate proposal=[P1] quorum=[Q1] votes=V1,V2,V3 "
        "issued_by=control_plane term=1 at=2026-10-02T00:04:00Z",
        "→ [X1] execute actor=agent_a action=deploy state=[P1] finality=[FC1] "
        "at=2026-10-02T00:05:00Z",
    ]
    return "\n".join(lines)


class ConflictSetQuorumTests(unittest.TestCase):
    def assert_round_trip_valid(self, source: str):
        first = parse_document(source)
        r1 = validate_document(first)
        self.assertTrue(r1["valid"], r1["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        r2 = validate_document(second)
        self.assertTrue(r2["valid"], r2["errors"])
        self.assertEqual(first, second)
        return second

    def test_happy_path_round_trip(self):
        self.assert_round_trip_valid(happy_path())

    def test_missing_conflict_member_rejected(self):
        lines = fork(5)
        lines.append(
            "◆ [CS1] conflict_set members=S1,S2,S3,S4 domain=authority status=open"
        )
        result = validate_document(parse_document("\n".join(lines)))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V046" for e in result["errors"]))

    def test_false_conflict_set_rejected(self):
        source = "\n".join([
            ROOT,
            "○ [S1] snapshot branch=a parent=[S0] seq=1 domain=authority "
            "state_hash=h1 at=2026-10-02T00:01:00Z",
            "○ [S2] snapshot branch=b parent=[S0] seq=1 domain=authority "
            "state_hash=h1 at=2026-10-02T00:01:00Z",
            "◆ [CS1] conflict_set members=S1,S2 domain=authority status=open",
        ])
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V045" for e in result["errors"]))

    def test_last_writer_proposal_rejected(self):
        lines = fork(3)
        lines += [
            "◆ [CS1] conflict_set members=S1,S2,S3 domain=authority status=open",
            "→ [P1] propose conflict_set=[CS1] strategy=last_writer result_hash=hm "
            "at=2026-10-02T00:02:00Z",
        ]
        result = validate_document(parse_document("\n".join(lines)))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V047" for e in result["errors"]))

    def test_invalid_quorum_threshold_rejected(self):
        result = validate_document(parse_document(
            "! [Q1] quorum voters=a,b,c threshold=4 independence_min=3"
        ))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V048" for e in result["errors"]))

    def test_duplicate_quorum_voter_rejected(self):
        result = validate_document(parse_document(
            "! [Q1] quorum voters=a,b,b threshold=2 independence_min=2"
        ))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V048" for e in result["errors"]))

    def test_insufficient_votes_rejected(self):
        source = happy_path().replace(
            "votes=V1,V2,V3", "votes=V1,V2"
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V052" for e in result["errors"]))

    def test_duplicate_voter_cannot_inflate_quorum(self):
        source = happy_path().replace(
            "voter=validator_c proposal=[P1]",
            "voter=validator_a proposal=[P1]",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V052" for e in result["errors"]))

    def test_same_independence_domain_cannot_inflate_independence(self):
        source = happy_path()
        source = source.replace("independence=model_family_b", "independence=model_family_a")
        source = source.replace("independence=human_review", "independence=model_family_a")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V052" for e in result["errors"]))

    def test_unauthorized_voter_rejected(self):
        source = happy_path().replace("voter=validator_c", "voter=outsider")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V051" for e in result["errors"]))

    def test_reject_vote_cannot_be_counted_in_certificate(self):
        source = happy_path().replace(
            "voter=validator_c proposal=[P1] decision=approve",
            "voter=validator_c proposal=[P1] decision=reject",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V051" for e in result["errors"]))

    def test_vote_for_other_proposal_rejected(self):
        source = happy_path().replace(
            "◆ [V3] vote voter=validator_c proposal=[P1]",
            "◆ [V3] vote voter=validator_c proposal=[P404]",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        rules = {e["rule"] for e in result["errors"]}
        self.assertTrue("V049" in rules or "V051" in rules)

    def test_untrusted_certificate_issuer_rejected(self):
        source = happy_path().replace(
            "issued_by=control_plane", "issued_by=agent_a"
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V050" for e in result["errors"]))

    def test_execution_certificate_must_match_state(self):
        source = happy_path().replace(
            "state=[P1] finality=[FC1]",
            "state=[P404] finality=[FC1]",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V054" for e in result["errors"]))

    def test_execution_cannot_precede_certificate(self):
        source = happy_path().replace(
            "at=2026-10-02T00:05:00Z",
            "at=2026-10-02T00:03:30Z",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V054" for e in result["errors"]))

    def test_duplicate_certificate_term_rejected(self):
        source = happy_path() + "\n" + (
            "✓ [FC2] certificate proposal=[P1] quorum=[Q1] votes=V1,V2,V3 "
            "issued_by=control_plane term=1 at=2026-10-02T00:04:30Z"
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V053" for e in result["errors"]))

    def test_certificate_does_not_create_fact_claim(self):
        doc = self.assert_round_trip_valid(happy_path())
        facts = [
            s for s in doc["statements"]
            if s.get("kind") == "claim" and s.get("epistemic_state") == "fact"
        ]
        self.assertEqual(facts, [])

    def test_hundred_way_fork_uses_one_conflict_set(self):
        lines = fork(100)
        members = ",".join(f"S{i}" for i in range(1, 101))
        lines.append(
            f"◆ [CS1] conflict_set members={members} domain=authority status=open"
        )
        doc = parse_document("\n".join(lines))
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        sets = [s for s in doc["statements"] if s["kind"] == "conflict_set"]
        self.assertEqual(len(sets), 1)
        many_way = [c for c in result["conflicts"] if c["rule"] == "V046"]
        self.assertEqual(len(many_way), 1)
        self.assertEqual(len(many_way[0]["members"]), 100)


    def test_101_voter_quorum_certificate_scales_linearly(self):
        lines = fork(2)
        lines += [
            "◆ [CS1] conflict_set members=S1,S2 domain=authority status=open",
            "→ [P1] propose conflict_set=[CS1] strategy=explicit result_hash=hm "
            "at=2026-10-02T00:02:00Z",
        ]

        voter_names = [f"validator_{i}" for i in range(1, 102)]
        lines.append(
            "! [Q1] quorum voters=" + ",".join(voter_names) +
            " threshold=67 independence_min=67"
        )

        vote_ids = []
        for i in range(1, 68):
            vote_ids.append(f"V{i}")
            lines.append(
                f"◆ [V{i}] vote voter=validator_{i} proposal=[P1] "
                f"decision=approve independence=domain_{i} evidence_hash=ev_{i} "
                "at=2026-10-02T00:03:00Z"
            )

        lines.append(
            "✓ [FC1] certificate proposal=[P1] quorum=[Q1] votes=" +
            ",".join(vote_ids) +
            " issued_by=control_plane term=1 at=2026-10-02T00:04:00Z"
        )

        doc = parse_document("\n".join(lines))
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        certs = [
            s for s in doc["statements"]
            if s["kind"] == "finality_certificate"
        ]
        self.assertEqual(len(certs), 1)


if __name__ == "__main__":
    unittest.main()
