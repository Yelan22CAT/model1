#!/usr/bin/env python3
"""Bridge-0 v0.12 exact-integer semantic constitution tests."""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_exact_integer_v0_12 import (
    compile_node,
    compile_python,
    compile_unsafe_node_number,
)
from parser_v0_2 import BridgeParseError
from parser_v0_12 import parse_document
from renderer_v0_12 import render_document
from validator_v0_12 import validate_document


VALID = (
    "⊙ [P1] program name=bridge0_v012_exact_integer "
    "targets=python312,node20\n"
    "→ [C1] compute op=stats numeric=exact_integer "
    "values=9007199254740991,9007199254740993,-9007199254740995,"
    "18446744073709551617 observe=json_value\n"
)

EXPECTED = {
    "count": {"$exact_integer": "4"},
    "max": {"$exact_integer": "18446744073709551617"},
    "min": {"$exact_integer": "-9007199254740995"},
    "sum": {"$exact_integer": "18455751272964292606"},
}


class ExactIntegerTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_numeric_contract_is_mandatory(self):
        source = VALID.replace("numeric=exact_integer ", "")
        with self.assertRaises(BridgeParseError):
            parse_document(source)

    def test_backend_default_numeric_contract_is_rejected(self):
        source = VALID.replace("numeric=exact_integer", "numeric=backend_default")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V082" for e in result["errors"]))

    def test_decimal_input_is_rejected(self):
        source = VALID.replace(
            "9007199254740993",
            "9007199254740993.0",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V083" for e in result["errors"]))

    def test_leading_zero_integer_is_rejected(self):
        source = VALID.replace(
            "9007199254740991",
            "09007199254740991",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V083" for e in result["errors"]))

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_generated_python_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source = (experiment / "executable_v0.12.bridge").read_text(encoding="utf-8")
        expected = compile_python(parse_document(source))
        actual = (
            experiment / "generated" / "generated_v0_12.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_generated_node_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source = (experiment / "executable_v0.12.bridge").read_text(encoding="utf-8")
        expected = compile_node(parse_document(source))
        actual = (
            experiment / "generated" / "generated_v0_12.mjs"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_node_backend_uses_bigint_not_number(self):
        js = compile_node(parse_document(VALID))
        self.assertIn("9007199254740993n", js)
        self.assertIn("18446744073709551617n", js)
        self.assertNotIn("Math.max", js)

    def test_python_and_bigint_node_match_exact_semantics(self):
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
            self.assertEqual(json.loads(py_out.read_text(encoding="utf-8")), EXPECTED)
            self.assertEqual(json.loads(js_out.read_text(encoding="utf-8")), EXPECTED)

    def test_unsafe_javascript_number_backend_drifts(self):
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
                compile_unsafe_node_number(doc),
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

    def test_bridge_source_contains_no_bigint_or_python_int_instruction(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "semantic_compute")
        source_repr = json.dumps(task, sort_keys=True)
        self.assertNotIn("BigInt", source_repr)
        self.assertNotIn("python", source_repr.lower())
        self.assertEqual(task["numeric"], "exact_integer")

    def test_256_large_integer_stress_compiles_both_targets(self):
        base = 9007199254740993
        values = ",".join(str(base + i * 10000000000000000) for i in range(256))
        source = (
            "⊙ [P1] program name=stress targets=python312,node20\n"
            "→ [C1] compute op=stats numeric=exact_integer "
            f"values={values} observe=json_value\n"
        )
        doc = parse_document(source)
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        self.assertIn("$exact_integer", compile_python(doc))
        self.assertIn("BigInt", compile_node(doc))

    def test_257_values_are_rejected(self):
        values = ",".join(str(i) for i in range(257))
        source = (
            "⊙ [P1] program name=too_many targets=python312,node20\n"
            "→ [C1] compute op=stats numeric=exact_integer "
            f"values={values} observe=json_value\n"
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V083" for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
