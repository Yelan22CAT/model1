#!/usr/bin/env python3
"""Bridge-0 v0.17 executable migration / information-loss audit tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_migration_v0_17 import (
    SOURCE_ARTIFACT,
    compile_node,
    compile_python,
    compile_unsafe_success_only_node,
    expected_result,
)
from parser_v0_2 import BridgeParseError
from parser_v0_17 import parse_document
from renderer_v0_17 import render_document
from validator_v0_17 import validate_document


VALID = (
    "⊙ [P1] program name=bridge0_v017_semantic_migration "
    "targets=python312,node20\n"
    "→ [M1] migrate domain=grapheme artifact=fixture_v1 "
    "routes=v1_to_v2,v1_to_v3_compact "
    "loss_policy=reject_unacknowledged roundtrip=audit "
    "execution=gate_on_audit observe=json_value\n"
)


class SemanticMigrationTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_loss_policy_is_mandatory(self):
        source = VALID.replace("loss_policy=reject_unacknowledged ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_unsafe_loss_policy_is_rejected(self):
        source = VALID.replace(
            "loss_policy=reject_unacknowledged",
            "loss_policy=allow_silent_loss",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V110" for e in result["errors"]))

    def test_roundtrip_audit_is_required(self):
        source = VALID.replace("roundtrip=audit", "roundtrip=skip")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V110" for e in result["errors"]))

    def test_execution_must_gate_on_audit(self):
        source = VALID.replace("execution=gate_on_audit", "execution=on_conversion")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V110" for e in result["errors"]))

    def test_route_set_is_pinned(self):
        source = VALID.replace(",v1_to_v3_compact", "")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V109" for e in result["errors"]))

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_lossless_route_roundtrips_and_executes(self):
        route = expected_result()["routes"]["v1_to_v2"]
        self.assertTrue(route["conversion_success"])
        self.assertTrue(route["roundtrip"]["recovered_source"])
        self.assertTrue(route["loss"]["lossless"])
        self.assertEqual(route["loss"]["lost_paths"], [])
        self.assertTrue(route["execution_allowed"])

    def test_lossy_route_converts_but_is_blocked(self):
        route = expected_result()["routes"]["v1_to_v3_compact"]
        self.assertTrue(route["conversion_success"])
        self.assertFalse(route["roundtrip"]["recovered_source"])
        self.assertFalse(route["loss"]["lossless"])
        self.assertFalse(route["execution_allowed"])

    def test_loss_manifest_names_dropped_semantics(self):
        route = expected_result()["routes"]["v1_to_v3_compact"]
        lost = route["loss"]["lost_paths"]
        self.assertIn("$.units[*].label", lost)
        self.assertIn("$.units[*].confidence", lost)
        self.assertIn("$.provenance", lost)
        self.assertIn("$.notes", lost)

    def test_source_artifact_contains_semantics_that_compact_route_drops(self):
        self.assertIn("provenance", SOURCE_ARTIFACT)
        self.assertIn("notes", SOURCE_ARTIFACT)
        self.assertTrue(all("label" in unit for unit in SOURCE_ARTIFACT["units"]))
        compact = expected_result()["routes"]["v1_to_v3_compact"]["migrated"]
        self.assertNotIn("provenance", compact)
        self.assertNotIn("notes", compact)
        self.assertNotIn("units", compact)

    def test_python_and_node_match_migration_audit(self):
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
                expected_result(),
            )

    def test_unsafe_success_only_backend_drifts(self):
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
                compile_unsafe_success_only_node(doc),
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
            route = unsafe["routes"]["v1_to_v3_compact"]
            self.assertTrue(route["conversion_success"])
            self.assertTrue(route["execution_allowed"])
            self.assertFalse(route["roundtrip"]["attempted"])

    def test_conversion_success_does_not_imply_execution_permission(self):
        route = expected_result()["routes"]["v1_to_v3_compact"]
        self.assertTrue(route["conversion_success"])
        self.assertFalse(route["execution_allowed"])

    def test_source_contains_no_backend_specific_migration_code(self):
        task = next(
            s for s in parse_document(VALID)["statements"]
            if s["kind"] == "semantic_migration"
        )
        encoded = json.dumps(task, sort_keys=True)
        self.assertNotIn("python", encoded.lower())
        self.assertNotIn("javascript", encoded.lower())
        self.assertNotIn("node", encoded.lower())


if __name__ == "__main__":
    unittest.main()
