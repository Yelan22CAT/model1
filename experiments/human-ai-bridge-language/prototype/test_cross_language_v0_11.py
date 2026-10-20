#!/usr/bin/env python3
"""Bridge-0 v0.11 cross-language compiler/equivalence tests."""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from compare_typed_observables_v0_10 import compare
from compiler_crosslang_v0_11 import compile_node, compile_python
from parser_v0_11 import parse_document
from renderer_v0_11 import render_document
from validator_v0_11 import validate_document


VALID = (
    "⊙ [P1] program name=bridge0_v011_cross_language "
    "targets=python312,node20\n"
    "→ [C1] compute op=stats values=2,3,5,7,11,13 observe=json_value\n"
)


class CrossLanguageTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_source_contains_no_backend_specific_command(self):
        doc = parse_document(VALID)
        task = next(s for s in doc["statements"] if s["kind"] == "semantic_compute")
        self.assertNotIn("module", task)
        self.assertNotIn("command", task)
        self.assertNotIn("python", task)
        self.assertNotIn("node", task)

    def test_python_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_python(doc), compile_python(doc))

    def test_node_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_node(doc), compile_node(doc))

    def test_generated_python_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        expected = compile_python(parse_document(
            (experiment / "executable_v0.11.bridge").read_text(encoding="utf-8")
        ))
        actual = (
            experiment / "generated" / "generated_v0_11.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_generated_node_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        expected = compile_node(parse_document(
            (experiment / "executable_v0.11.bridge").read_text(encoding="utf-8")
        ))
        actual = (
            experiment / "generated" / "generated_v0_11.mjs"
        ).read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_missing_target_is_rejected(self):
        source = VALID.replace("targets=python312,node20", "targets=python312")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V076" for e in result["errors"]))

    def test_unknown_target_is_rejected(self):
        source = VALID.replace("node20", "ruby")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V076" for e in result["errors"]))

    def test_unknown_operation_is_rejected(self):
        source = VALID.replace("op=stats", "op=eval")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V077" for e in result["errors"]))

    def test_non_integer_input_is_rejected(self):
        source = VALID.replace("values=2,3,5,7,11,13", "values=2,3.5,5")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V078" for e in result["errors"]))

    def test_backend_sources_are_structurally_different(self):
        doc = parse_document(VALID)
        py = compile_python(doc)
        js = compile_node(doc)
        self.assertNotEqual(py, js)
        self.assertIn("import json", py)
        self.assertIn("Math.max", js)

    def test_python_and_node_observables_match(self):
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

            py_result = subprocess.run(
                [sys.executable, str(py_path)],
                capture_output=True,
                text=True,
                check=True,
            )
            node_result = subprocess.run(
                ["node", str(js_path)],
                capture_output=True,
                text=True,
                check=True,
            )
            py_out.write_text(py_result.stdout, encoding="utf-8")
            js_out.write_text(node_result.stdout, encoding="utf-8")

            equal, digest = compare([py_out, js_out])
            self.assertTrue(equal)
            self.assertEqual(len(digest), 64)

    def test_mutated_backend_is_detected_as_drift(self):
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
            mutated_js = compile_node(doc).replace(
                "sum: values.reduce((a, b) => a + b, 0),",
                "sum: values.reduce((a, b) => a + b, 0) + 1,",
            )
            js_path.write_text(mutated_js, encoding="utf-8")

            py_out.write_text(
                subprocess.run(
                    [sys.executable, str(py_path)],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout,
                encoding="utf-8",
            )
            js_out.write_text(
                subprocess.run(
                    ["node", str(js_path)],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout,
                encoding="utf-8",
            )

            equal, _ = compare([py_out, js_out])
            self.assertFalse(equal)

    def test_256_integer_stress_compiles_both_targets(self):
        values = ",".join(str(i) for i in range(-128, 128))
        source = (
            "⊙ [P1] program name=stress targets=python312,node20\n"
            f"→ [C1] compute op=stats values={values} observe=json_value\n"
        )
        doc = parse_document(source)
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        self.assertIn("values = [", compile_python(doc))
        self.assertIn("const values = [", compile_node(doc))


if __name__ == "__main__":
    unittest.main()
