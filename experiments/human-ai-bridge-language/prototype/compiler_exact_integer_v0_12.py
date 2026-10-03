#!/usr/bin/env python3
"""Bridge-0 v0.12 exact-integer cross-language compiler.

Canonical semantic rule:
- integers are mathematical exact integers;
- backend default numeric semantics are not authoritative;
- Python lowers to arbitrary-precision int;
- Node lowers to BigInt;
- JSON observables use an explicit tagged decimal-string representation.
"""

from __future__ import annotations

from typing import Any

from validator_v0_12 import exact_int_values, validate_document


class BridgeExactIntegerCompileError(ValueError):
    pass


def compute_task(doc: dict[str, Any]) -> dict[str, Any]:
    validation = validate_document(doc)
    if not validation["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in validation["errors"]
        )
        raise BridgeExactIntegerCompileError(detail)
    return next(
        s for s in doc["statements"]
        if s.get("kind") == "semantic_compute"
    )


def compile_python(doc: dict[str, Any]) -> str:
    task = compute_task(doc)
    values = exact_int_values(task["values"])
    assert values is not None

    return (
        "# Generated from Bridge-0 v0.12. Do not hand-edit.\n"
        "import json\n\n"
        f"values = {values!r}\n"
        "def exact(value):\n"
        "    return {'$exact_integer': str(value)}\n\n"
        "result = {\n"
        "    'count': exact(len(values)),\n"
        "    'max': exact(max(values)),\n"
        "    'min': exact(min(values)),\n"
        "    'sum': exact(sum(values)),\n"
        "}\n"
        "print(json.dumps(result, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    task = compute_task(doc)
    values = exact_int_values(task["values"])
    assert values is not None
    js_values = "[" + ",".join(f"{v}n" for v in values) + "]"

    return (
        "// Generated from Bridge-0 v0.12. Do not hand-edit.\n"
        f"const values = {js_values};\n"
        "const exact = (value) => ({ $exact_integer: value.toString() });\n"
        "const sum = values.reduce((a, b) => a + b, 0n);\n"
        "const max = values.reduce((a, b) => (a > b ? a : b));\n"
        "const min = values.reduce((a, b) => (a < b ? a : b));\n"
        "const result = {\n"
        "  count: exact(BigInt(values.length)),\n"
        "  max: exact(max),\n"
        "  min: exact(min),\n"
        "  sum: exact(sum),\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_unsafe_node_number(doc: dict[str, Any]) -> str:
    """Negative-control backend that intentionally inherits JS Number semantics."""
    task = compute_task(doc)
    values = exact_int_values(task["values"])
    assert values is not None
    js_values = "[" + ",".join(str(v) for v in values) + "]"

    return (
        "// UNSAFE NEGATIVE CONTROL: JavaScript Number semantics.\n"
        f"const values = {js_values};\n"
        "const exact = (value) => ({ $exact_integer: Math.trunc(value).toString() });\n"
        "const sum = values.reduce((a, b) => a + b, 0);\n"
        "const result = {\n"
        "  count: exact(values.length),\n"
        "  max: exact(Math.max(...values)),\n"
        "  min: exact(Math.min(...values)),\n"
        "  sum: exact(sum),\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeExactIntegerCompileError(f"unsupported target: {target}")
