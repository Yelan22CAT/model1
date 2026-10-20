#!/usr/bin/env python3
"""Bridge-0 v0.19 revocation / replay-resistance tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_replay_v0_19 import (
    attempt,
    compile_node,
    compile_python,
    compile_unsafe_stateless_node,
    expected_result,
    fresh_state,
)
from parser_v0_2 import BridgeParseError
from parser_v0_19 import parse_document
from renderer_v0_19 import render_document
from validator_v0_19 import (
    EXPECTED_DIGEST,
    EXPECTED_LOSS,
    EXPECTED_REVOCATION_EPOCH,
    validate_document,
)


VALID = (
    "⊙ [P1] program name=bridge0_v019_replay_resistance "
    "targets=python312,node20\n"
    "→ [A1] authorize_once domain=grapheme artifact=fixture_v1 "
    "route=v1_to_v3_compact authorization_id=auth:v019:0001 "
    "nonce=nonce_v019_0001 "
    "loss_ack=$.units[*].id|$.units[*].label|$.units[*].confidence|$.provenance|$.notes "
    "authority=fixture_owner scope=exact_loss_manifest "
    "artifact_digest=07b88b41d6be837f8b370c27523053bf84b214eef0bc1d074633e1250db2db92 "
    "provenance=fixture_authority_record revocation_epoch=7 usage=single_use "
    "issued_at=2026-10-02T12:00:00Z expires_at=2026-10-02T13:00:00Z "
    "evaluate_at=2026-10-02T12:30:00Z observe=json_value\n"
)


class ReplayResistanceTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_authorization_id_is_mandatory(self):
        source = VALID.replace("authorization_id=auth:v019:0001 ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_nonce_is_mandatory(self):
        source = VALID.replace("nonce=nonce_v019_0001 ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_invalid_authorization_id_is_rejected(self):
        source = VALID.replace("auth:v019:0001", "bad")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V125" for e in result["errors"]))

    def test_invalid_nonce_is_rejected(self):
        source = VALID.replace("nonce_v019_0001", "x")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V125" for e in result["errors"]))

    def test_partial_loss_ack_is_rejected(self):
        source = VALID.replace("|$.provenance", "")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V126" for e in result["errors"]))

    def test_wrong_artifact_digest_is_rejected(self):
        source = VALID.replace(EXPECTED_DIGEST, "0" * 64)
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V128" for e in result["errors"]))

    def test_wrong_revocation_epoch_is_rejected(self):
        source = VALID.replace("revocation_epoch=7", "revocation_epoch=6")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V129" for e in result["errors"]))

    def test_reusable_usage_is_rejected(self):
        source = VALID.replace("usage=single_use", "usage=reusable")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V129" for e in result["errors"]))

    def test_first_use_is_allowed_and_consumes_token(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["first_use"]
        self.assertTrue(result["execution_allowed"])
        self.assertEqual(result["decision"], "authorized_once")
        self.assertIn("auth:v019:0001", result["state_after"]["used_authorization_ids"])
        self.assertIn("nonce_v019_0001", result["state_after"]["used_nonces"])

    def test_replay_same_token_is_denied(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["replay_same_token"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["authorization_id_unused"])
        self.assertFalse(result["checks"]["nonce_unused"])

    def test_revoked_before_use_is_denied(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["revoked_before_use"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["not_revoked"])

    def test_stale_revocation_epoch_is_denied(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["stale_revocation_epoch"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["revocation_epoch_current"])

    def test_tampered_nonce_is_denied(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["tampered_nonce"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["nonce_match"])

    def test_expired_token_is_denied(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["expired_token"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["time_valid"])

    def test_denied_attempt_does_not_consume_nonce(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "single_use_authorization")
        state = fresh_state()
        result = attempt(task, state, presented_nonce="nonce-tampered-0001")
        self.assertFalse(result["execution_allowed"])
        self.assertEqual(state["used_nonces"], [])
        self.assertEqual(state["used_authorization_ids"], [])

    def test_revocation_wins_even_inside_valid_window(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "single_use_authorization")
        state = fresh_state(revoked=[task["authorization_id"]])
        result = attempt(task, state, evaluate_at="2026-10-02T12:15:00Z")
        self.assertFalse(result["execution_allowed"])
        self.assertTrue(result["checks"]["time_valid"])
        self.assertFalse(result["checks"]["not_revoked"])

    def test_epoch_freshness_wins_even_if_not_revoked(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "single_use_authorization")
        state = fresh_state(current_epoch=EXPECTED_REVOCATION_EPOCH + 1)
        result = attempt(task, state)
        self.assertFalse(result["execution_allowed"])
        self.assertTrue(result["checks"]["not_revoked"])
        self.assertFalse(result["checks"]["revocation_epoch_current"])

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_python_and_node_match_replay_contract(self):
        if shutil.which("node") is None:
            self.skipTest("node executable unavailable")

        doc = parse_document(VALID)
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            py_path = root / "program.py"
            js_path = root / "program.mjs"
            py_out = root / "python.json"
            js_out = root / "node.json"

            py_path.write_text(compile_python(doc), encoding="utf-8")
            js_path.write_text(compile_node(doc), encoding="utf-8")

            py_out.write_text(
                subprocess.run(
                    [sys.executable, str(py_path)],
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout,
                encoding="utf-8",
            )
            js_out.write_text(
                subprocess.run(
                    ["node", str(js_path)],
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout,
                encoding="utf-8",
            )

            equal, digest = compare([py_out, js_out])
            self.assertTrue(equal)
            self.assertEqual(len(digest), 64)
            self.assertEqual(
                json.loads(py_out.read_text(encoding="utf-8")),
                expected_result(doc),
            )

    def test_unsafe_stateless_backend_drifts(self):
        if shutil.which("node") is None:
            self.skipTest("node executable unavailable")

        doc = parse_document(VALID)
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            py_path = root / "program.py"
            unsafe_path = root / "unsafe.mjs"
            py_out = root / "python.json"
            unsafe_out = root / "unsafe.json"

            py_path.write_text(compile_python(doc), encoding="utf-8")
            unsafe_path.write_text(
                compile_unsafe_stateless_node(doc),
                encoding="utf-8",
            )

            py_out.write_text(
                subprocess.run(
                    [sys.executable, str(py_path)],
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout,
                encoding="utf-8",
            )
            unsafe_out.write_text(
                subprocess.run(
                    ["node", str(unsafe_path)],
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout,
                encoding="utf-8",
            )

            equal, _ = compare([py_out, unsafe_out])
            self.assertFalse(equal)

            unsafe = json.loads(unsafe_out.read_text(encoding="utf-8"))
            self.assertTrue(unsafe["scenarios"]["replay_same_token"]["execution_allowed"])
            self.assertTrue(unsafe["scenarios"]["revoked_before_use"]["execution_allowed"])
            self.assertTrue(unsafe["scenarios"]["stale_revocation_epoch"]["execution_allowed"])

    def test_known_loss_manifest_remains_exact(self):
        self.assertEqual(
            EXPECTED_LOSS,
            {
                "$.units[*].id",
                "$.units[*].label",
                "$.units[*].confidence",
                "$.provenance",
                "$.notes",
            },
        )

    def test_source_contains_no_backend_specific_replay_code(self):
        task = next(
            s for s in parse_document(VALID)["statements"]
            if s["kind"] == "single_use_authorization"
        )
        encoded = json.dumps(task, sort_keys=True)
        self.assertNotIn("python", encoded.lower())
        self.assertNotIn("javascript", encoded.lower())
        self.assertNotIn("node", encoded.lower())


if __name__ == "__main__":
    unittest.main()
