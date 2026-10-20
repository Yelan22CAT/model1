#!/usr/bin/env python3
"""Bridge-0 v0.13 binary64 floating semantic compiler.

Canonical rules covered in this prototype:
- IEEE-754 binary64 value domain;
- NaN, +Infinity, -Infinity, +0 and -0 remain distinct semantic classes;
- finite half-integers round with ties-to-even;
- JSON transport uses explicit tags for exceptional/signed-zero values.
"""

from __future__ import annotations

from typing import Any

from validator_v0_13 import csv_values, validate_document


class BridgeFloatCompileError(ValueError):
    pass


def compute_task(doc: dict[str, Any]) -> dict[str, Any]:
    validation = validate_document(doc)
    if not validation["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in validation["errors"]
        )
        raise BridgeFloatCompileError(detail)
    return next(
        s for s in doc["statements"]
        if s.get("kind") == "semantic_compute"
    )


def compile_python(doc: dict[str, Any]) -> str:
    task = compute_task(doc)
    tokens = csv_values(task["values"])

    return (
        "# Generated from Bridge-0 v0.13. Do not hand-edit.\n"
        "import json\n"
        "import math\n\n"
        f"tokens = {tokens!r}\n\n"
        "def decode(token):\n"
        "    if token == 'nan':\n"
        "        return float('nan')\n"
        "    if token == '+inf':\n"
        "        return float('inf')\n"
        "    if token == '-inf':\n"
        "        return float('-inf')\n"
        "    if token == '-0':\n"
        "        return -0.0\n"
        "    if token == '+0':\n"
        "        return 0.0\n"
        "    return float(token)\n\n"
        "def classify(value):\n"
        "    if math.isnan(value):\n"
        "        return {'$binary64': 'nan'}\n"
        "    if math.isinf(value):\n"
        "        return {'$binary64': '+inf' if value > 0 else '-inf'}\n"
        "    if value == 0.0:\n"
        "        return {'$binary64': '-0' if math.copysign(1.0, value) < 0 else '+0'}\n"
        "    return {'$binary64': format(value, '.17g')}\n\n"
        "def exact_integer(value):\n"
        "    return {'$exact_integer': str(value)}\n\n"
        "values = [(token, decode(token)) for token in tokens]\n"
        "result = {\n"
        "    'classes': {token: classify(value) for token, value in values},\n"
        "    'rounded': {\n"
        "        token: exact_integer(round(value))\n"
        "        for token, value in values\n"
        "        if token.endswith('.5')\n"
        "    },\n"
        "}\n"
        "print(json.dumps(result, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    task = compute_task(doc)
    tokens = csv_values(task["values"])
    js_tokens = "[" + ",".join(repr(token) for token in tokens) + "]"

    return (
        "// Generated from Bridge-0 v0.13. Do not hand-edit.\n"
        f"const tokens = {js_tokens};\n\n"
        "function decode(token) {\n"
        "  if (token === 'nan') return Number.NaN;\n"
        "  if (token === '+inf') return Number.POSITIVE_INFINITY;\n"
        "  if (token === '-inf') return Number.NEGATIVE_INFINITY;\n"
        "  if (token === '-0') return -0;\n"
        "  if (token === '+0') return 0;\n"
        "  return Number(token);\n"
        "}\n\n"
        "function classify(value) {\n"
        "  if (Number.isNaN(value)) return { $binary64: 'nan' };\n"
        "  if (value === Number.POSITIVE_INFINITY) return { $binary64: '+inf' };\n"
        "  if (value === Number.NEGATIVE_INFINITY) return { $binary64: '-inf' };\n"
        "  if (Object.is(value, -0)) return { $binary64: '-0' };\n"
        "  if (Object.is(value, 0)) return { $binary64: '+0' };\n"
        "  return { $binary64: value.toPrecision(17).replace(/(?:\\.0+|(?:(\\.[0-9]*?)0+))$/, '$1') };\n"
        "}\n\n"
        "function roundTiesToEven(value) {\n"
        "  const floor = Math.floor(value);\n"
        "  const fraction = value - floor;\n"
        "  if (fraction < 0.5) return floor;\n"
        "  if (fraction > 0.5) return floor + 1;\n"
        "  return floor % 2 === 0 ? floor : floor + 1;\n"
        "}\n\n"
        "const exactInteger = (value) => ({ $exact_integer: String(value) });\n"
        "const values = tokens.map((token) => [token, decode(token)]);\n"
        "const classes = {};\n"
        "const rounded = {};\n"
        "for (const [token, value] of values) {\n"
        "  classes[token] = classify(value);\n"
        "  if (token.endsWith('.5')) rounded[token] = exactInteger(roundTiesToEven(value));\n"
        "}\n"
        "const result = { classes, rounded };\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_unsafe_node_defaults(doc: dict[str, Any]) -> str:
    """Negative control: JS defaults lose special-value and rounding semantics."""
    task = compute_task(doc)
    tokens = csv_values(task["values"])
    js_tokens = "[" + ",".join(repr(token) for token in tokens) + "]"

    return (
        "// UNSAFE NEGATIVE CONTROL: backend-default float semantics.\n"
        f"const tokens = {js_tokens};\n"
        "const decode = (token) => {\n"
        "  if (token === 'nan') return Number.NaN;\n"
        "  if (token === '+inf') return Number.POSITIVE_INFINITY;\n"
        "  if (token === '-inf') return Number.NEGATIVE_INFINITY;\n"
        "  if (token === '-0') return -0;\n"
        "  if (token === '+0') return 0;\n"
        "  return Number(token);\n"
        "};\n"
        "const result = { classes: {}, rounded: {} };\n"
        "for (const token of tokens) {\n"
        "  const value = decode(token);\n"
        "  result.classes[token] = value;\n"
        "  if (token.endsWith('.5')) result.rounded[token] = Math.round(value);\n"
        "}\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeFloatCompileError(f"unsupported target: {target}")
