#!/usr/bin/env python3
"""Bridge-0 v0.9 multi-backend semantic-equivalence tests."""

import pathlib
import tempfile
import unittest

from compare_observables_v0_9 import equivalent
from compiler_github_v0_9 import compile_github_actions
from local_runner_v0_9 import run_local
from parser_v0_9 import parse_document
from renderer_v0_9 import render_document
from validator_v0_9 import validate_document


VALID = (
    "⊙ [W1] workflow name=bridge0_v09_backend_equivalence "
    "runner=ubuntu-latest trigger=push "
    "branch=experiment/human-ai-bridge-v0.1\n"
    "→ [T1] task kind=checkout\n"
    "→ [T2] task kind=setup_python version=3.12\n"
    "→ [T3] task kind=python_module module=bridge_probe_v0_9 "
    "cwd=experiments/human-ai-bridge-language/prototype observe=stdout\n"
)


class MultiBackendTests(unittest.TestCase):
    def test_round_trip_preserves_observable(self):
        first = parse_document(VALID)
        self.assertTrue(validate_document(first)["valid"])
        rendered = render_document(first)
        second = parse_document(rendered)
        self.assertEqual(first, second)

    def test_compiler_emits_two_backend_paths(self):
        doc = parse_document(VALID)
        output = compile_github_actions(doc)
        self.assertIn("bridge_probe_v0_9 > .bridge-github-T3.stdout", output)
        self.assertIn("local_runner_v0_9.py", output)
        self.assertIn("compare_observables_v0_9.py", output)

    def test_compiler_is_deterministic(self):
        doc = parse_document(VALID)
        self.assertEqual(
            compile_github_actions(doc),
            compile_github_actions(doc),
        )

    def test_unsupported_observable_rejected(self):
        source = VALID.replace("observe=stdout", "observe=stderr")
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V068" for e in result["errors"]))

    def test_observable_on_checkout_rejected(self):
        source = VALID.replace(
            "→ [T1] task kind=checkout",
            "→ [T1] task kind=checkout observe=stdout",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V068" for e in result["errors"]))

    def test_unknown_compiler_field_rejected(self):
        source = VALID.replace(
            "observe=stdout",
            "observe=stdout mystery=value",
        )
        result = validate_document(parse_document(source))
        self.assertFalse(result["valid"])
        self.assertTrue(any(e["rule"] == "V069" for e in result["errors"]))

    def test_equal_observables_compare_equal(self):
        with tempfile.TemporaryDirectory() as tmp:
            left = pathlib.Path(tmp) / "a"
            right = pathlib.Path(tmp) / "b"
            left.write_text("same\n", encoding="utf-8")
            right.write_text("same\n", encoding="utf-8")
            self.assertTrue(equivalent(left, right))

    def test_line_ending_normalization_is_nonsemantic(self):
        with tempfile.TemporaryDirectory() as tmp:
            left = pathlib.Path(tmp) / "a"
            right = pathlib.Path(tmp) / "b"
            left.write_bytes(b"same\r\n")
            right.write_bytes(b"same\n")
            self.assertTrue(equivalent(left, right))

    def test_backend_drift_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            left = pathlib.Path(tmp) / "a"
            right = pathlib.Path(tmp) / "b"
            left.write_text("result=A\n", encoding="utf-8")
            right.write_text("result=B\n", encoding="utf-8")
            self.assertFalse(equivalent(left, right))

    def test_checked_in_generated_v09_matches_compiler(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        repo_root = experiment.parent.parent
        source_path = experiment / "executable_v0.9.bridge"
        generated_path = repo_root / ".github" / "workflows" / "bridge0-generated-v09.yml"

        doc = parse_document(source_path.read_text(encoding="utf-8"))
        expected = compile_github_actions(doc)
        actual = generated_path.read_text(encoding="utf-8")
        self.assertEqual(expected, actual)

    def test_local_backend_executes_same_probe(self):
        here = pathlib.Path(__file__).resolve()
        experiment = here.parent.parent
        source_path = experiment / "executable_v0.9.bridge"

        outputs = run_local(source_path)
        self.assertEqual(len(outputs), 1)
        payload = outputs[0].read_text(encoding="utf-8")
        self.assertEqual(
            payload,
            '{"bridge":"0.9","observable":"backend-equivalence","result":42,"state":"stable"}\n',
        )

    def test_twenty_observable_tasks_get_unique_comparisons(self):
        lines = [
            "⊙ [W1] workflow name=stress runner=ubuntu-latest "
            "trigger=workflow_dispatch",
            "→ [T1] task kind=checkout",
            "→ [T2] task kind=setup_python version=3.12",
        ]
        for i in range(1, 21):
            lines.append(
                f"→ [P{i}] task kind=python_module module=bridge_probe_v0_9 "
                "cwd=experiments/human-ai-bridge-language/prototype observe=stdout"
            )

        doc = parse_document("\n".join(lines))
        self.assertTrue(validate_document(doc)["valid"])
        output = compile_github_actions(doc)
        self.assertEqual(output.count("Compare backend observable P"), 20)
        for i in range(1, 21):
            self.assertIn(f".bridge-github-P{i}.stdout", output)
            self.assertIn(f".bridge-local-P{i}.stdout", output)


if __name__ == "__main__":
    unittest.main()
