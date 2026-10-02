#!/usr/bin/env python3
"""Bridge-0 v0.18 scoped known-loss authorization tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_loss_authorization_v0_18 import (
    canonical_digest,
    compile_node,
    compile_python,
    compile_unsafe_authority_only_node,
    evaluate,
    expected_result,
)
from compiler_migration_v0_17 import SOURCE_ARTIFACT
from parser_v0_2 import BridgeParseError
from parser_v0_18 import parse_document
from renderer_v0_18 import render_document
from validator_v0_18 import EXPECTED_DIGEST, EXPECTED_LOSS, validate_document


VALID = (
    "⊙ [P1] program name=bridge0_v018_scoped_loss_authorization "
    "targets=python312,node20\n"
    "→ [A1] authorize_loss domain=grapheme artifact=fixture_v1 "
    "route=v1_to_v3_compact "
    "loss_ack=$.units[*].id|$.units[*].label|$.units[*].confidence|$.provenance|$.notes "
    "authority=fixture_owner scope=exact_loss_manifest "
    "artifact_digest=07b88b41d6be837f8b370c27523053bf84b214eef0bc1d074633e1250db2db92 "
    "provenance=fixture_authority_record "
    "issued_at=2026-10-02T12:00:00Z expires_at=2026-10-02T13:00:00Z "
    "evaluate_at=2026-10-02T12:30:00Z observe=json_value\n"
)


class ScopedLossAuthorizationTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_loss_ack_is_mandatory(self):
        source = VALID.replace(
            "loss_ack=$.units[*].id|$.units[*].label|$.units[*].confidence|$.provenance|$.notes ",
            "",
        )
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_partial_loss_ack_is_rejected_at_validation(self):
        source = VALID.replace("|$.provenance", "")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V116" for e in result["errors"]))

    def test_wrong_authority_is_rejected_at_validation(self):
        source = VALID.replace("authority=fixture_owner", "authority=other_agent")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V117" for e in result["errors"]))

    def test_wrong_scope_is_rejected_at_validation(self):
        source = VALID.replace("scope=exact_loss_manifest", "scope=all_loss")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V117" for e in result["errors"]))

    def test_wrong_artifact_digest_is_rejected_at_validation(self):
        source = VALID.replace(EXPECTED_DIGEST, "0" * 64)
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V118" for e in result["errors"]))

    def test_noncanonical_time_is_rejected(self):
        source = VALID.replace(
            "evaluate_at=2026-10-02T12:30:00Z",
            "evaluate_at=2026-10-02T12:30Z",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V119" for e in result["errors"]))

    def test_artifact_digest_binds_exact_source_artifact(self):
        self.assertEqual(canonical_digest(SOURCE_ARTIFACT), EXPECTED_DIGEST)

    def test_exact_known_loss_is_authorized(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["authorized_exact"]
        self.assertTrue(result["execution_allowed"])
        self.assertEqual(result["decision"], "authorized_known_loss")
        self.assertTrue(all(result["checks"].values()))

    def test_expired_replay_is_denied(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["expired_replay"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["time_valid"])

    def test_expiry_boundary_is_exclusive(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "loss_authorization")
        result = evaluate(task, evaluate_at="2026-10-02T13:00:00Z")
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["time_valid"])

    def test_before_issue_is_denied(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "loss_authorization")
        result = evaluate(task, evaluate_at="2026-10-02T11:59:59Z")
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["time_valid"])

    def test_wrong_artifact_is_denied_at_runtime(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["wrong_artifact"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["artifact_bound"])

    def test_partial_ack_is_denied_at_runtime(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["partial_ack"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["loss_ack_exact"])

    def test_wrong_scope_is_denied_at_runtime(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["wrong_scope"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["scope_exact"])

    def test_wrong_authority_is_denied_at_runtime(self):
        doc = parse_document(VALID)
        result = expected_result(doc)["scenarios"]["wrong_authority"]
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["checks"]["authority_match"])

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_python_and_node_match_authorization_contract(self):
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

    def test_unsafe_authority_only_backend_drifts(self):
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
                compile_unsafe_authority_only_node(doc),
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
            self.assertTrue(
                unsafe["scenarios"]["expired_replay"]["execution_allowed"]
            )
            self.assertTrue(
                unsafe["scenarios"]["wrong_artifact"]["execution_allowed"]
            )
            self.assertTrue(
                unsafe["scenarios"]["partial_ack"]["execution_allowed"]
            )
            self.assertTrue(
                unsafe["scenarios"]["wrong_scope"]["execution_allowed"]
            )

    def test_authority_does_not_expand_scope(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "loss_authorization")
        result = evaluate(task, authority="fixture_owner", scope="all_future_loss")
        self.assertFalse(result["execution_allowed"])

    def test_acknowledgement_does_not_remove_expiry(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "loss_authorization")
        result = evaluate(
            task,
            loss_ack=sorted(EXPECTED_LOSS),
            evaluate_at="2026-10-02T13:00:01Z",
        )
        self.assertFalse(result["execution_allowed"])

    def test_source_contains_no_backend_specific_authorization_code(self):
        task = next(
            s for s in parse_document(VALID)["statements"]
            if s["kind"] == "loss_authorization"
        )
        encoded = json.dumps(task, sort_keys=True)
        self.assertNotIn("python", encoded.lower())
        self.assertNotIn("javascript", encoded.lower())
        self.assertNotIn("node", encoded.lower())


if __name__ == "__main__":
    unittest.main()
