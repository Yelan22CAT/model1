#!/usr/bin/env python3
"""Bridge-0 v0.10 heterogeneous-runtime / typed-observable tests."""

from __future__ import annotations

import pathlib
import tempfile
import unittest

from compare_typed_observables_v0_10 import (
    TypedObservableError,
    compare,
    load_semantic,
)
from compiler_github_v0_10 import compile_github_actions
from parser_v0_10 import parse_document
from renderer_v0_10 import render_document
from validator_v0_10 import validate_document


VALID = (
    "⊙ [W1] workflow name=bridge0_v010_typed_equivalence "
    "runner=ubuntu-latest trigger=push "
    "branch=experiment/human-ai-bridge-v0.1 "
    "targets=ubuntu-latest,windows-latest,macos-latest\n"
    "→ [T1] task kind=checkout\n"
    "→ [T2] task kind=setup_python version=3.12\n"
    "→ [T3] task kind=python_module module=bridge_probe_v0_10 "
    "cwd=experiments/human-ai-bridge-language/prototype "
    "observe=json_value\n"
)


class HeterogeneousRuntimeTests(unittest.TestCase):
    def test_valid_program_round_trip(self):
        first = parse_document(VALID)
        result = validate_document(first)
        self.assertTrue(result["valid"], result["errors"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_compiler_emits_three_heterogeneous_backends(self):
        output = compile_github_actions(parse_document(VALID))
        self.assertIn("runs-on: ubuntu-latest", output)
        self.assertIn("runs-on: windows-latest", output)
        self.assertIn("runs-on: macos-latest", output)
        self.assertIn("compare_backends:", output)

    def test_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(compile_github_actions(doc), compile_github_actions(doc))

    def test_single_target_is_rejected(self):
        source = VALID.replace(
            "targets=ubuntu-latest,windows-latest,macos-latest",
            "targets=ubuntu-latest",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V071" for e in result["errors"]))

    def test_duplicate_target_is_rejected(self):
        source = VALID.replace(
            "targets=ubuntu-latest,windows-latest,macos-latest",
            "targets=ubuntu-latest,ubuntu-latest",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V071" for e in result["errors"]))

    def test_unknown_target_is_rejected(self):
        source = VALID.replace("macos-latest", "plan9-latest")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V071" for e in result["errors"]))

    def test_stdout_observable_is_rejected_in_v010(self):
        source = VALID.replace("observe=json_value", "observe=stdout")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V072" for e in result["errors"]))

    def test_no_typed_observable_is_rejected(self):
        source = VALID.replace(" observe=json_value", "")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V074" for e in result["errors"]))

    def test_json_key_order_and_whitespace_are_nonsemantic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = pathlib.Path(tmp) / "a.json"
            b = pathlib.Path(tmp) / "b.json"
            a.write_text('{"b":2,"a":[1,true]}\n', encoding="utf-8")
            b.write_text('{\n  "a": [1.0, true],\n  "b": 2.0\n}\n', encoding="utf-8")
            equal, _ = compare([a, b])
            self.assertTrue(equal)

    def test_json_semantic_drift_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = pathlib.Path(tmp) / "a.json"
            b = pathlib.Path(tmp) / "b.json"
            a.write_text('{"result":42}\n', encoding="utf-8")
            b.write_text('{"result":43}\n', encoding="utf-8")
            equal, detail = compare([a, b])
            self.assertFalse(equal)
            self.assertIn("a.json=", detail)
            self.assertIn("b.json=", detail)

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "bad.json"
            path.write_text('{"result": NaN}', encoding="utf-8")
            with self.assertRaises(TypedObservableError):
                load_semantic(path)

    def test_three_way_semantic_equivalence(self):
        with tempfile.TemporaryDirectory() as tmp:
            p1 = pathlib.Path(tmp) / "ubuntu.json"
            p2 = pathlib.Path(tmp) / "windows.json"
            p3 = pathlib.Path(tmp) / "macos.json"
            p1.write_text('{"state":{"ready":true},"result":42}', encoding="utf-8")
            p2.write_text('{\n"result":42.0,"state":{"ready":true}\n}', encoding="utf-8")
            p3.write_text('{"result":42,"state":{"ready":true}}\n', encoding="utf-8")
            equal, digest = compare([p1, p2, p3])
            self.assertTrue(equal)
            self.assertEqual(len(digest), 64)

    def test_checked_in_generated_v010_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        repo_root = experiment.parent.parent
        source_path = experiment / "executable_v0.10.bridge"
        generated_path = repo_root / ".github" / "workflows" / "bridge0-generated-v010.yml"

        doc = parse_document(source_path.read_text(encoding="utf-8"))
        expected = compile_github_actions(doc)
        actual = generated_path.read_text(encoding="utf-8")
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
