#!/usr/bin/env python3
"""Bridge-0 v0.7 identity / attestation / evidence-provenance tests."""

import unittest

from parser_v0_7 import parse_document
from renderer_v0_7 import render_document
from validator_v0_7 import validate_document


PREFIX = [
    "○ [S0] snapshot branch=root parent=none seq=0 domain=authority state_hash=h0 at=2026-10-02T00:00:00Z",
    "○ [S1] snapshot branch=a parent=[S0] seq=1 domain=authority state_hash=h1 at=2026-10-02T00:01:00Z",
    "○ [S2] snapshot branch=b parent=[S0] seq=1 domain=authority state_hash=h2 at=2026-10-02T00:01:00Z",
    "◆ [CS1] conflict_set members=S1,S2 domain=authority status=open",
    "→ [P1] propose conflict_set=[CS1] strategy=explicit result_hash=hm at=2026-10-02T00:02:00Z",
]


def identity_block(
    idx: int,
    subject: str,
    control: str,
    model: str,
    runtime: str,
    origin: str,
    evidence_hash: str,
) -> list[str]:
    return [
        f"○ [I{idx}] identity subject={subject} control_domain={control} "
        f"model_lineage={model} runtime_origin={runtime}",
        f"◆ [AT{idx}] attest identity=[I{idx}] issuer=identity_ca status=valid "
        "valid_from=2026-10-01T00:00:00Z valid_until=2026-10-31T23:59:59Z",
        f"◆ [EP{idx}] evidence_provenance evidence_hash={evidence_hash} "
        f"source_identity=[I{idx}] attestation=[AT{idx}] origin={origin} "
        "parent=none at=2026-10-02T00:02:30Z",
    ]


def happy_path() -> str:
    lines = list(PREFIX)
    lines += identity_block(1, "validator_a", "org_a", "model_a", "runtime_a", "sensor_a", "ev1")
    lines += identity_block(2, "validator_b", "org_b", "model_b", "runtime_b", "sensor_b", "ev2")
    lines += identity_block(3, "validator_c", "org_c", "human_review", "runtime_c", "record_c", "ev3")
    lines += [
        "! [Q1] quorum voters=validator_a,validator_b,validator_c "
        "threshold=3 independence_min=3 evidence_min=3",
        "◆ [V1] vote voter=validator_a proposal=[P1] decision=approve "
        "independence=org_a evidence_hash=ev1 identity=[I1] attestation=[AT1] "
        "provenance=[EP1] at=2026-10-02T00:03:00Z",
        "◆ [V2] vote voter=validator_b proposal=[P1] decision=approve "
        "independence=org_b evidence_hash=ev2 identity=[I2] attestation=[AT2] "
        "provenance=[EP2] at=2026-10-02T00:03:01Z",
        "◆ [V3] vote voter=validator_c proposal=[P1] decision=approve "
        "independence=org_c evidence_hash=ev3 identity=[I3] attestation=[AT3] "
        "provenance=[EP3] at=2026-10-02T00:03:02Z",
        "✓ [FC1] certificate proposal=[P1] quorum=[Q1] votes=V1,V2,V3 "
        "issued_by=control_plane term=1 at=2026-10-02T00:04:00Z",
        "→ [X1] execute actor=agent_a action=deploy state=[P1] finality=[FC1] "
        "at=2026-10-02T00:05:00Z",
    ]
    return "\n".join(lines)


class IdentityProvenanceTests(unittest.TestCase):
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

    def test_untrusted_attestation_issuer_rejected(self):
        source = happy_path().replace(
            "issuer=identity_ca status=valid",
            "issuer=unknown_ca status=valid",
            1,
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V056" for e in result["errors"]))

    def test_expired_attestation_rejected_for_vote(self):
        source = happy_path().replace(
            "valid_until=2026-10-31T23:59:59Z",
            "valid_until=2026-10-02T00:02:59Z",
            1,
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        rules = {e["rule"] for e in result["errors"]}
        self.assertTrue("V059" in rules or "V058" in rules)

    def test_revoked_attestation_rejected_for_later_vote(self):
        source = happy_path().replace(
            "◆ [V1] vote voter=validator_a",
            "× [AR1] revoke_attestation target=[AT1] by=identity_ca "
            "at=2026-10-02T00:02:50Z\n"
            "◆ [V1] vote voter=validator_a",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V059" for e in result["errors"]))

    def test_wrong_attestation_revoker_rejected(self):
        source = happy_path().replace(
            "◆ [V1] vote voter=validator_a",
            "× [AR1] revoke_attestation target=[AT1] by=outsider "
            "at=2026-10-02T00:02:50Z\n"
            "◆ [V1] vote voter=validator_a",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V057" for e in result["errors"]))

    def test_voter_alias_subject_mismatch_rejected(self):
        source = happy_path().replace(
            "voter=validator_a proposal=[P1]",
            "voter=alias_a proposal=[P1]",
            1,
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V059" for e in result["errors"]))

    def test_fake_independence_label_rejected(self):
        source = happy_path().replace(
            "independence=org_a",
            "independence=fake_org",
            1,
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V059" for e in result["errors"]))

    def test_shared_model_lineage_fails_attested_independence(self):
        source = happy_path().replace(
            "model_lineage=model_b",
            "model_lineage=model_a",
            1,
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V063" for e in result["errors"]))

    def test_shared_runtime_origin_fails_attested_independence(self):
        source = happy_path().replace(
            "runtime_origin=runtime_b",
            "runtime_origin=runtime_a",
            1,
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V063" for e in result["errors"]))

    def test_copied_evidence_root_fails_evidence_independence(self):
        source = happy_path()
        source = source.replace(
            "◆ [EP2] evidence_provenance evidence_hash=ev2 "
            "source_identity=[I2] attestation=[AT2] origin=sensor_b "
            "parent=none at=2026-10-02T00:02:30Z",
            "◆ [EP2ROOT] evidence_provenance evidence_hash=ev1 "
            "source_identity=[I2] attestation=[AT2] origin=sensor_a "
            "parent=none at=2026-10-02T00:02:20Z\n"
            "◆ [EP2] evidence_provenance evidence_hash=ev2 "
            "source_identity=[I2] attestation=[AT2] origin=copy_process "
            "parent=[EP2ROOT] at=2026-10-02T00:02:30Z",
        )
        source = source.replace(
            "◆ [EP1] evidence_provenance evidence_hash=ev1 "
            "source_identity=[I1] attestation=[AT1] origin=sensor_a "
            "parent=none at=2026-10-02T00:02:30Z",
            "◆ [EP1] evidence_provenance evidence_hash=ev1 "
            "source_identity=[I1] attestation=[AT1] origin=sensor_a "
            "parent=none at=2026-10-02T00:02:30Z",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V064" for e in result["errors"]))

    def test_vote_hash_must_match_provenance(self):
        source = happy_path().replace(
            "independence=org_a evidence_hash=ev1",
            "independence=org_a evidence_hash=wrong_hash",
            1,
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V060" for e in result["errors"]))

    def test_provenance_cycle_rejected(self):
        source = happy_path().replace(
            "parent=none at=2026-10-02T00:02:30Z",
            "parent=[EPX] at=2026-10-02T00:02:30Z",
            1,
        )
        source += (
            "\n◆ [EPX] evidence_provenance evidence_hash=evx "
            "source_identity=[I1] attestation=[AT1] origin=x "
            "parent=[EP1] at=2026-10-02T00:02:31Z"
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V062" for e in result["errors"]))

    def test_certificate_still_does_not_create_truth(self):
        doc = self.assert_round_trip_valid(happy_path())
        facts = [
            s for s in doc["statements"]
            if s.get("kind") == "claim" and s.get("epistemic_state") == "fact"
        ]
        self.assertEqual(facts, [])

    def test_67_attested_independent_voters_scale(self):
        lines = list(PREFIX)
        voters = []
        vote_ids = []
        for i in range(1, 68):
            subject = f"validator_{i}"
            voters.append(subject)
            vote_ids.append(f"V{i}")
            lines += identity_block(
                i,
                subject,
                f"org_{i}",
                f"model_{i}",
                f"runtime_{i}",
                f"source_{i}",
                f"ev_{i}",
            )

        lines.append(
            "! [Q1] quorum voters=" + ",".join(voters)
            + " threshold=67 independence_min=67 evidence_min=67"
        )

        for i in range(1, 68):
            lines.append(
                f"◆ [V{i}] vote voter=validator_{i} proposal=[P1] decision=approve "
                f"independence=org_{i} evidence_hash=ev_{i} identity=[I{i}] "
                f"attestation=[AT{i}] provenance=[EP{i}] at=2026-10-02T00:03:00Z"
            )

        lines.append(
            "✓ [FC1] certificate proposal=[P1] quorum=[Q1] votes="
            + ",".join(vote_ids)
            + " issued_by=control_plane term=1 at=2026-10-02T00:04:00Z"
        )

        result = validate_document(parse_document("\n".join(lines)))
        self.assertTrue(result["valid"], result["errors"])


if __name__ == "__main__":
    unittest.main()
