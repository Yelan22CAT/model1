#!/usr/bin/env python3
"""Bridge-0 v0.13 binary64 floating semantic constitution tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_float_v0_13 import (
    compile_node,
    compile_python,
    compile_unsafe_node_defaults,
)
from parser_v0_2 import BridgeParseError
from parser_v0_13 import parse_document
from renderer_v0_13 import render_document
from validator_v0_13 import validate_document


VALID = (
    "⊙ [P1] program name=bridge0_v013_float_constitution "
    "targets=python312,node20\n"
    "→ [C1] compute op=float_profile numeric=binary64 rounding=ties_to_even "
    "values=nan,+inf,-inf,-0,+0,2.5,3.5,-2.5,-3.5 observe=json_value\n"
)

EXPECTED_ROUNDED = {
    "2.5": {"$exact_integer": "2"},
    "3.5": {"$exact_integer": "4"},
    "-2.5": {"$exact_integer": "-2"},
    "-3.5": {"$exact_integer": "-4"},
}


class FloatConstitutionTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_numeric_contract_is_mandatory(self):
        source = VALID.replace("numeric=binary64 ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_rounding_contract_is_mandatory(self):
        source = VALID.replace("rounding=ties_to_even ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_backend_default_rounding_is_rejected(self):
        source = VALID.replace("rounding=ties_to_even", "rounding=backend_default")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V087" for e in result["errors"]))

    def test_backend_default_numeric_is_rejected(self):
        source = VALID.replace("numeric=binary64", "numeric=backend_default")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V087" for e in result["errors"]))

    def test_missing_edge_vector_is_rejected(self):
        source = VALID.replace(",nan", "")
        if source == VALID:
            source = VALID.replace("values=nan,", "values=")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V088" for e in result["errors"]))

    def test_noncanonical_float_token_is_rejected(self):
        source = VALID.replace("2.5", "2.50")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V088" for e in result["errors"]))

    def test_duplicate_float_token_is_rejected(self):
        source = VALID.replace(
            "values=nan,+inf",
            "values=nan,nan,+inf",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V088" for e in result["errors"]))

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_generated_python_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source = (experiment / "executable_v0.13.bridge").read_text(encoding="utf-8")
        expected = compile_python(parse_document(source))
        actual = (
            experiment / "generated" / "generated_v0_13.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_generated_node_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source = (experiment / "executable_v0.13.bridge").read_text(encoding="utf-8")
        expected = compile_node(parse_document(source))
        actual = (
            experiment / "generated" / "generated_v0_13.mjs"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_node_compiler_implements_ties_to_even(self):
        js = compile_node(parse_document(VALID))
        self.assertIn("roundTiesToEven", js)
        self.assertNotIn("Math.round(value)", js)

    def test_python_and_node_match_float_contract(self):
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

            payload = json.loads(py_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["rounded"], EXPECTED_ROUNDED)
            self.assertEqual(payload["classes"]["nan"], {"$binary64": "nan"})
            self.assertEqual(payload["classes"]["+inf"], {"$binary64": "+inf"})
            self.assertEqual(payload["classes"]["-inf"], {"$binary64": "-inf"})
            self.assertEqual(payload["classes"]["-0"], {"$binary64": "-0"})
            self.assertEqual(payload["classes"]["+0"], {"$binary64": "+0"})

    def test_unsafe_javascript_defaults_drift(self):
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
                compile_unsafe_node_defaults(doc),
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

            unsafe_payload = json.loads(unsafe_out.read_text(encoding="utf-8"))
            self.assertIsNone(unsafe_payload["classes"]["nan"])
            self.assertIsNone(unsafe_payload["classes"]["+inf"])
            self.assertEqual(unsafe_payload["classes"]["-0"], 0)
            self.assertEqual(unsafe_payload["rounded"]["2.5"], 3)
            self.assertEqual(unsafe_payload["rounded"]["-3.5"], -3)

    def test_bridge_source_contains_no_backend_rounding_instruction(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "semantic_compute")
        source_repr = json.dumps(task, sort_keys=True)
        self.assertNotIn("Math.round", source_repr)
        self.assertNotIn("python", source_repr.lower())
        self.assertEqual(task["rounding"], "ties_to_even")

    def test_special_values_are_not_raw_json_numbers(self):
        if shutil.which("node") is None:
            self.skipTest("node executable unavailable")

        doc = parse_document(VALID)
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "program.mjs"
            path.write_text(compile_node(doc), encoding="utf-8")
            output = subprocess.run(
                ["node", str(path)],
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            payload = json.loads(output)
            self.assertIsInstance(payload["classes"]["nan"], dict)
            self.assertIsInstance(payload["classes"]["+inf"], dict)
            self.assertIsInstance(payload["classes"]["-0"], dict)


if __name__ == "__main__":
    unittest.main()
