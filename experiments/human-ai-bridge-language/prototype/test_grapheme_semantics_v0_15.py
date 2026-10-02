#!/usr/bin/env python3
"""Bridge-0 v0.15 Unicode-version / grapheme semantic tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_grapheme_v0_15 import (
    compile_node,
    compile_python,
    compile_unsafe_node_codepoints,
)
from parser_v0_2 import BridgeParseError
from parser_v0_15 import parse_document
from renderer_v0_15 import render_document
from validator_v0_15 import validate_document


VALID = (
    "⊙ [P1] program name=bridge0_v015_grapheme_identity "
    "targets=python312,node20 unicode_version=15.0\n"
    "→ [C1] compute op=grapheme_profile text_model=unicode_scalar "
    "normalization=NFC segmentation=extended_grapheme_cluster "
    "profile=bridge_uax29_subset_v1 "
    "values=0065+0301,1F44D+1F3FD,1F469+200D+1F4BB,1F1E8+1F1E6,"
    "0061+0308+0062,1F468+200D+1F469+200D+1F467+200D+1F466,"
    "000D+000A+0061,2764+FE0F observe=json_value\n"
)


class GraphemeSemanticTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_unicode_version_is_mandatory(self):
        source = VALID.replace(" unicode_version=15.0", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_wrong_unicode_version_is_rejected(self):
        source = VALID.replace("unicode_version=15.0", "unicode_version=14.0")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V096" for e in result["errors"]))

    def test_grapheme_contract_is_mandatory(self):
        source = VALID.replace("segmentation=extended_grapheme_cluster ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_codepoint_segmentation_contract_is_rejected(self):
        source = VALID.replace(
            "segmentation=extended_grapheme_cluster",
            "segmentation=code_point",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V098" for e in result["errors"]))

    def test_profile_is_pinned(self):
        source = VALID.replace(
            "profile=bridge_uax29_subset_v1",
            "profile=backend_default",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V098" for e in result["errors"]))

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_generated_python_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source = (experiment / "executable_v0.15.bridge").read_text(encoding="utf-8")
        expected = compile_python(parse_document(source))
        actual = (
            experiment / "generated" / "generated_v0_15.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_generated_node_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source = (experiment / "executable_v0.15.bridge").read_text(encoding="utf-8")
        expected = compile_node(parse_document(source))
        actual = (
            experiment / "generated" / "generated_v0_15.mjs"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_python_and_node_match_grapheme_contract(self):
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

    def test_expected_grapheme_counts_and_clusters(self):
        doc = parse_document(VALID)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "program.py"
            path.write_text(compile_python(doc), encoding="utf-8")
            payload = json.loads(
                subprocess.run(
                    [sys.executable, str(path)],
                    text=True,
                    capture_output=True,
                    check=True,
                ).stdout
            )
            p = payload["profiles"]

            self.assertEqual(p["0065+0301"]["clusters"], [{"$grapheme": "00E9"}])
            self.assertEqual(p["1F44D+1F3FD"]["count"], {"$exact_integer": "1"})
            self.assertEqual(p["1F469+200D+1F4BB"]["count"], {"$exact_integer": "1"})
            self.assertEqual(p["1F1E8+1F1E6"]["count"], {"$exact_integer": "1"})
            self.assertEqual(
                p["0061+0308+0062"]["clusters"],
                [{"$grapheme": "00E4"}, {"$grapheme": "0062"}],
            )
            self.assertEqual(
                p["1F468+200D+1F469+200D+1F467+200D+1F466"]["count"],
                {"$exact_integer": "1"},
            )
            self.assertEqual(
                p["000D+000A+0061"]["clusters"],
                [{"$grapheme": "000D+000A"}, {"$grapheme": "0061"}],
            )
            self.assertEqual(p["2764+FE0F"]["count"], {"$exact_integer": "1"})

    def test_unsafe_codepoint_backend_drifts(self):
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
                compile_unsafe_node_codepoints(doc),
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

    def test_python_runtime_unicode_attestation_fails_closed(self):
        code = compile_python(parse_document(VALID)).replace(
            "PINNED_UNICODE_VERSION = '15.0'",
            "PINNED_UNICODE_VERSION = '99.0'",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "program.py"
            path.write_text(code, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(path)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unicode data version mismatch", result.stderr)

    def test_node_runtime_unicode_attestation_fails_closed(self):
        if shutil.which("node") is None:
            self.skipTest("node executable unavailable")
        code = compile_node(parse_document(VALID)).replace(
            "const PINNED_UNICODE_VERSION = '15.0';",
            "const PINNED_UNICODE_VERSION = '99.0';",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "program.mjs"
            path.write_text(code, encoding="utf-8")
            result = subprocess.run(
                ["node", str(path)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unicode data version mismatch", result.stderr)

    def test_source_is_backend_independent(self):
        task = next(
            s for s in parse_document(VALID)["statements"]
            if s["kind"] == "semantic_compute"
        )
        encoded = json.dumps(task, sort_keys=True)
        self.assertNotIn("Intl.Segmenter", encoded)
        self.assertNotIn("unicodedata", encoded)
        self.assertEqual(task["segmentation"], "extended_grapheme_cluster")

    def test_missing_family_vector_is_rejected(self):
        source = VALID.replace(
            ",1F468+200D+1F469+200D+1F467+200D+1F466",
            "",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V099" for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
