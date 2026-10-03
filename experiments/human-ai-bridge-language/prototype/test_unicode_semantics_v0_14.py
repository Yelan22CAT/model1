#!/usr/bin/env python3
"""Bridge-0 v0.14 Unicode text-identity semantic tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_unicode_v0_14 import (
    compile_node,
    compile_python,
    compile_unsafe_node_raw,
)
from parser_v0_2 import BridgeParseError
from parser_v0_14 import parse_document
from renderer_v0_14 import render_document
from validator_v0_14 import validate_document


VALID = (
    "⊙ [P1] program name=bridge0_v014_unicode_identity "
    "targets=python312,node20\n"
    "→ [C1] compute op=text_profile text_model=unicode_scalar "
    "normalization=NFC identity=normalized_scalar_sequence "
    "values=00E9,0065+0301,00C5,0041+030A,212B,AC00,1100+1161,"
    "0065+0323+0301,0065+0301+0323,1F600,1F469+200D+1F4BB "
    "observe=json_value\n"
)


class UnicodeIdentityTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_normalization_contract_is_mandatory(self):
        source = VALID.replace("normalization=NFC ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_backend_default_normalization_is_rejected(self):
        source = VALID.replace("normalization=NFC", "normalization=backend_default")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V092" for e in result["errors"]))

    def test_raw_identity_contract_is_rejected(self):
        source = VALID.replace(
            "identity=normalized_scalar_sequence",
            "identity=raw_scalar_sequence",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V092" for e in result["errors"]))

    def test_lowercase_hex_token_is_rejected(self):
        source = VALID.replace("00E9", "00e9")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V093" for e in result["errors"]))

    def test_surrogate_scalar_is_rejected(self):
        source = VALID.replace("1F600", "D800")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V093" for e in result["errors"]))

    def test_out_of_range_scalar_is_rejected(self):
        source = VALID.replace("1F600", "110000")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V093" for e in result["errors"]))

    def test_duplicate_vector_is_rejected(self):
        source = VALID.replace("values=00E9,", "values=00E9,00E9,")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V093" for e in result["errors"]))

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_generated_python_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source = (experiment / "executable_v0.14.bridge").read_text(encoding="utf-8")
        expected = compile_python(parse_document(source))
        actual = (
            experiment / "generated" / "generated_v0_14.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_generated_node_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source = (experiment / "executable_v0.14.bridge").read_text(encoding="utf-8")
        expected = compile_node(parse_document(source))
        actual = (
            experiment / "generated" / "generated_v0_14.mjs"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_python_and_node_match_unicode_contract(self):
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

            payload = json.loads(py_out.read_text(encoding="utf-8"))["normalized"]
            self.assertEqual(payload["00E9"], payload["0065+0301"])
            self.assertEqual(payload["00C5"], payload["0041+030A"])
            self.assertEqual(payload["00C5"], payload["212B"])
            self.assertEqual(payload["AC00"], payload["1100+1161"])
            self.assertEqual(
                payload["0065+0323+0301"],
                payload["0065+0301+0323"],
            )

    def test_expected_nfc_scalar_sequences(self):
        if shutil.which("node") is None:
            self.skipTest("node executable unavailable")
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
            )["normalized"]

            self.assertEqual(payload["0065+0301"], {"$unicode_nfc": "00E9"})
            self.assertEqual(payload["212B"], {"$unicode_nfc": "00C5"})
            self.assertEqual(payload["1100+1161"], {"$unicode_nfc": "AC00"})
            self.assertEqual(
                payload["0065+0301+0323"],
                {"$unicode_nfc": "1EB9+0301"},
            )

    def test_supplementary_scalar_is_preserved_as_one_scalar(self):
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
            )["normalized"]
            self.assertEqual(payload["1F600"], {"$unicode_nfc": "1F600"})
            self.assertEqual(
                payload["1F469+200D+1F4BB"],
                {"$unicode_nfc": "1F469+200D+1F4BB"},
            )

    def test_unsafe_raw_backend_drifts(self):
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
            unsafe_path.write_text(compile_unsafe_node_raw(doc), encoding="utf-8")

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

    def test_bridge_source_contains_no_backend_normalize_instruction(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "semantic_compute")
        source_repr = json.dumps(task, sort_keys=True)
        self.assertNotIn("unicodedata", source_repr)
        self.assertNotIn(".normalize", source_repr)
        self.assertEqual(task["normalization"], "NFC")

    def test_missing_required_conformance_vector_is_rejected(self):
        source = VALID.replace(",212B", "")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V093" for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
