#!/usr/bin/env python3
"""Bridge-0 v0.14 Unicode text-identity compiler.

Canonical rules in this prototype:
- text is a sequence of Unicode scalar values;
- canonical normalization is NFC;
- text identity is equality of the NFC-normalized scalar sequence;
- backend raw string/code-unit representation is not authoritative.
"""

from __future__ import annotations

from typing import Any

from validator_v0_14 import csv_values, validate_document


class BridgeUnicodeCompileError(ValueError):
    pass


def compute_task(doc: dict[str, Any]) -> dict[str, Any]:
    validation = validate_document(doc)
    if not validation["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in validation["errors"]
        )
        raise BridgeUnicodeCompileError(detail)
    return next(
        s for s in doc["statements"]
        if s.get("kind") == "semantic_compute"
    )


def compile_python(doc: dict[str, Any]) -> str:
    task = compute_task(doc)
    tokens = csv_values(task["values"])

    return (
        "# Generated from Bridge-0 v0.14. Do not hand-edit.\n"
        "import json\n"
        "import unicodedata\n\n"
        f"tokens = {tokens!r}\n\n"
        "def decode(token):\n"
        "    return ''.join(chr(int(part, 16)) for part in token.split('+'))\n\n"
        "def scalar_token(text):\n"
        "    return '+'.join(f'{ord(ch):04X}' for ch in text)\n\n"
        "normalized = {}\n"
        "for token in tokens:\n"
        "    text = decode(token)\n"
        "    nfc = unicodedata.normalize('NFC', text)\n"
        "    normalized[token] = {'$unicode_nfc': scalar_token(nfc)}\n\n"
        "result = {'normalized': normalized}\n"
        "print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    task = compute_task(doc)
    tokens = csv_values(task["values"])
    js_tokens = "[" + ",".join(repr(token) for token in tokens) + "]"

    return (
        "// Generated from Bridge-0 v0.14. Do not hand-edit.\n"
        f"const tokens = {js_tokens};\n\n"
        "function decode(token) {\n"
        "  return String.fromCodePoint(...token.split('+').map((part) => parseInt(part, 16)));\n"
        "}\n\n"
        "function scalarToken(text) {\n"
        "  return Array.from(text, (ch) => ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')).join('+');\n"
        "}\n\n"
        "const normalized = {};\n"
        "for (const token of tokens) {\n"
        "  const text = decode(token);\n"
        "  const nfc = text.normalize('NFC');\n"
        "  normalized[token] = { $unicode_nfc: scalarToken(nfc) };\n"
        "}\n"
        "const result = { normalized };\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_unsafe_node_raw(doc: dict[str, Any]) -> str:
    """Negative control: raw scalar sequence is incorrectly treated as identity."""
    task = compute_task(doc)
    tokens = csv_values(task["values"])
    js_tokens = "[" + ",".join(repr(token) for token in tokens) + "]"

    return (
        "// UNSAFE NEGATIVE CONTROL: raw code-point sequence as text identity.\n"
        f"const tokens = {js_tokens};\n"
        "const normalized = {};\n"
        "for (const token of tokens) {\n"
        "  normalized[token] = { $unicode_nfc: token };\n"
        "}\n"
        "process.stdout.write(JSON.stringify({ normalized }) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeUnicodeCompileError(f"unsupported target: {target}")
