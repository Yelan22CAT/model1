#!/usr/bin/env python3
"""Bridge-0 v0.11 cross-language compiler.

One canonical semantic_compute operation is compiled into Python 3.12
or Node.js 20 source. Both backends must satisfy the same JSON observable.
"""

from __future__ import annotations

from typing import Any

from validator_v0_11 import int_values, validate_document


class BridgeCrossLanguageCompileError(ValueError):
    pass


def compute_task(doc: dict[str, Any]) -> dict[str, Any]:
    validation = validate_document(doc)
    if not validation["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in validation["errors"]
        )
        raise BridgeCrossLanguageCompileError(detail)
    return next(
        s for s in doc["statements"]
        if s.get("kind") == "semantic_compute"
    )


def compile_python(doc: dict[str, Any]) -> str:
    task = compute_task(doc)
    values = int_values(task["values"])
    assert values is not None

    return (
        "# Generated from Bridge-0 v0.11. Do not hand-edit.\n"
        "import json\n\n"
        f"values = {values!r}\n"
        "result = {\n"
        "    'count': len(values),\n"
        "    'max': max(values),\n"
        "    'min': min(values),\n"
        "    'sum': sum(values),\n"
        "}\n"
        "print(json.dumps(result, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    task = compute_task(doc)
    values = int_values(task["values"])
    assert values is not None
    js_values = "[" + ",".join(str(v) for v in values) + "]"

    return (
        "// Generated from Bridge-0 v0.11. Do not hand-edit.\n"
        f"const values = {js_values};\n"
        "const result = {\n"
        "  count: values.length,\n"
        "  max: Math.max(...values),\n"
        "  min: Math.min(...values),\n"
        "  sum: values.reduce((a, b) => a + b, 0),\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeCrossLanguageCompileError(f"unsupported target: {target}")
