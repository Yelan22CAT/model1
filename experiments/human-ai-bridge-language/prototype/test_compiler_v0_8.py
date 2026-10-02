#!/usr/bin/env python3
"""Bridge-0 v0.8 executable-source/compiler tests."""

import pathlib
import unittest

from compiler_github_v0_8 import BridgeCompileError, compile_github_actions
from parser_v0_2 import BridgeParseError
from parser_v0_8 import parse_document
from renderer_v0_8 import render_document
from validator_v0_8 import validate_document


VALID = (
    "⊙ [W1] workflow name=bridge0_v08_generated runner=ubuntu-latest "
    "trigger=push branch=experiment/human-ai-bridge-v0.1\n"
    "→ [T1] task kind=checkout\n"
    "→ [T2] task kind=setup_python version=3.12\n"
    "→ [T3] task kind=python_module module=unittest "
    "cwd=experiments/human-ai-bridge-language/prototype "
    "args=-v,test_parser_v0_2.py\n"
)


class CompilerTests(unittest.TestCase):
    def test_valid_program_compiles(self):
        doc = parse_document(VALID)
        result = validate_document(doc)
        self.assertTrue(result["valid"], result["errors"])
        output = compile_github_actions(doc)
        self.assertIn("uses: actions/checkout@v4", output)
        self.assertIn("uses: actions/setup-python@v5", output)
        self.assertIn("'python' '-m' 'unittest'", output)

    def test_compilation_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(
            compile_github_actions(doc),
            compile_github_actions(doc),
        )

    def test_bridge_round_trip_preserves_compiler_input(self):
        first = parse_document(VALID)
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)
        self.assertEqual(
            compile_github_actions(first),
            compile_github_actions(second),
        )

    def test_raw_shell_is_rejected(self):
        source = (
            "⊙ [W1] workflow name=x runner=ubuntu-latest trigger=workflow_dispatch\n"
            "→ [T1] task kind=raw_shell command=echo_hi\n"
        )
        doc = parse_document(source)
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V066" for e in result["errors"]))
        with self.assertRaises(BridgeCompileError):
            compile_github_actions(doc)

    def test_shell_metacharacter_argument_is_rejected(self):
        source = (
            "⊙ [W1] workflow name=x runner=ubuntu-latest trigger=workflow_dispatch\n"
            "→ [T1] task kind=python_module module=unittest args=-v;rm\n"
        )
        doc = parse_document(source)
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V067" for e in result["errors"]))

    def test_path_traversal_is_rejected(self):
        source = (
            "⊙ [W1] workflow name=x runner=ubuntu-latest trigger=workflow_dispatch\n"
            "→ [T1] task kind=python_module module=unittest cwd=../../tmp args=-v\n"
        )
        doc = parse_document(source)
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V067" for e in result["errors"]))

    def test_unsupported_runner_is_rejected(self):
        source = (
            "⊙ [W1] workflow name=x runner=self-hosted trigger=workflow_dispatch\n"
            "→ [T1] task kind=checkout\n"
        )
        doc = parse_document(source)
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V065" for e in result["errors"]))

    def test_push_requires_branch(self):
        source = (
            "⊙ [W1] workflow name=x runner=ubuntu-latest trigger=push\n"
            "→ [T1] task kind=checkout\n"
        )
        doc = parse_document(source)
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V065" for e in result["errors"]))

    def test_checkout_does_not_accept_arbitrary_action(self):
        source = (
            "⊙ [W1] workflow name=x runner=ubuntu-latest trigger=workflow_dispatch\n"
            "→ [T1] task kind=checkout action=evil/action@main\n"
        )
        doc = parse_document(source)
        result = validate_document(doc)
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V067" for e in result["errors"]))

    def test_checked_in_generated_workflow_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source_path = experiment / "executable_v0.8.bridge"
        repo_root = experiment.parent.parent
        generated_path = repo_root / ".github" / "workflows" / "bridge0-generated-v08.yml"

        doc = parse_document(source_path.read_text(encoding="utf-8"))
        expected = compile_github_actions(doc)
        actual = generated_path.read_text(encoding="utf-8")
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
