#!/usr/bin/env python3
"""Bridge-0 v0.16 semantic-profile evolution / handshake tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_compatibility_v0_16 import (
    compile_node,
    compile_python,
    compile_unsafe_semver_only_node,
    expected_result,
)
from parser_v0_2 import BridgeParseError
from parser_v0_16 import parse_document
from renderer_v0_16 import render_document
from validator_v0_16 import validate_document


VALID = (
    "⊙ [P1] program name=bridge0_v016_semantic_compatibility "
    "targets=python312,node20\n"
    "→ [C1] compatibility domain=grapheme "
    "profiles=grapheme_v1,grapheme_v2,grapheme_v3_breaking "
    "policy=behavioral_manifest migration=explicit observe=json_value\n"
)


class SemanticCompatibilityTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_behavioral_manifest_policy_is_mandatory(self):
        source = VALID.replace("policy=behavioral_manifest ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_semver_only_policy_is_rejected(self):
        source = VALID.replace(
            "policy=behavioral_manifest",
            "policy=semver_only",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V104" for e in result["errors"]))

    def test_explicit_migration_is_required(self):
        source = VALID.replace("migration=explicit", "migration=implicit")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V104" for e in result["errors"]))

    def test_profile_set_is_pinned(self):
        source = VALID.replace(",grapheme_v3_breaking", "")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V103" for e in result["errors"]))

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_v2_is_backward_compatible_extension(self):
        result = expected_result()["comparisons"]["grapheme_v1->grapheme_v2"]
        self.assertEqual(result["relation"], "backward_compatible_extension")
        self.assertTrue(result["exchange_allowed"])
        self.assertFalse(result["migration_required"])
        self.assertEqual(result["changed"], [])
        self.assertEqual(result["removed"], [])
        self.assertEqual(result["added"], ["2764+FE0F"])

    def test_v3_breaking_is_rejected_despite_same_major_label(self):
        result = expected_result()["comparisons"]["grapheme_v1->grapheme_v3_breaking"]
        self.assertTrue(result["semver_same_major_claim"])
        self.assertEqual(result["relation"], "breaking")
        self.assertFalse(result["exchange_allowed"])
        self.assertTrue(result["migration_required"])
        self.assertEqual(result["changed"], ["1F469+200D+1F4BB"])

    def test_python_and_node_match_behavioral_manifest(self):
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

    def test_unsafe_semver_only_backend_drifts(self):
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
                compile_unsafe_semver_only_node(doc),
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
            bad = unsafe["comparisons"]["grapheme_v1->grapheme_v3_breaking"]
            self.assertTrue(bad["exchange_allowed"])
            self.assertEqual(bad["relation"], "compatible_by_label")

    def test_same_major_version_is_not_authority(self):
        result = expected_result()["comparisons"]["grapheme_v1->grapheme_v3_breaking"]
        self.assertTrue(result["semver_same_major_claim"])
        self.assertFalse(result["exchange_allowed"])

    def test_source_contains_no_backend_specific_compatibility_code(self):
        task = next(
            s for s in parse_document(VALID)["statements"]
            if s["kind"] == "semantic_compatibility"
        )
        encoded = json.dumps(task, sort_keys=True)
        self.assertNotIn("python", encoded.lower())
        self.assertNotIn("javascript", encoded.lower())
        self.assertNotIn("node", encoded.lower())

    def test_unknown_domain_is_rejected(self):
        source = VALID.replace("domain=grapheme", "domain=filesystem")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V102" for e in result["errors"]))

    def test_duplicate_profile_is_rejected(self):
        source = VALID.replace(
            "profiles=grapheme_v1,grapheme_v2,grapheme_v3_breaking",
            "profiles=grapheme_v1,grapheme_v2,grapheme_v2,grapheme_v3_breaking",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V103" for e in result["errors"]))

    def test_behavior_change_is_reported_not_hidden(self):
        result = expected_result()["comparisons"]["grapheme_v1->grapheme_v3_breaking"]
        self.assertEqual(result["added"], ["2764+FE0F"])
        self.assertEqual(result["removed"], [])
        self.assertEqual(result["changed"], ["1F469+200D+1F4BB"])


if __name__ == "__main__":
    unittest.main()
