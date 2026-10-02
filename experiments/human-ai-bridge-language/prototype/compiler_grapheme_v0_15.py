#!/usr/bin/env python3
"""Bridge-0 v0.15 Unicode-version + grapheme compiler."""

from __future__ import annotations

from typing import Any

from validator_v0_15 import csv_values, validate_document


class BridgeGraphemeCompileError(ValueError):
    pass


def program_and_task(doc: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    validation = validate_document(doc)
    if not validation["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in validation["errors"]
        )
        raise BridgeGraphemeCompileError(detail)

    program = next(s for s in doc["statements"] if s.get("kind") == "program")
    task = next(
        s for s in doc["statements"]
        if s.get("kind") == "semantic_compute"
    )
    return program, task


def compile_python(doc: dict[str, Any]) -> str:
    program, task = program_and_task(doc)
    tokens = csv_values(task["values"])
    version = str(program["unicode_version"])

    return (
        "# Generated from Bridge-0 v0.15. Do not hand-edit.\n"
        "import json\n"
        "import unicodedata\n\n"
        f"PINNED_UNICODE_VERSION = {version!r}\n"
        f"tokens = {tokens!r}\n\n"
        "def version_matches(runtime, pinned):\n"
        "    return runtime == pinned or runtime.startswith(pinned + '.')\n\n"
        "if not version_matches(unicodedata.unidata_version, PINNED_UNICODE_VERSION):\n"
        "    raise RuntimeError(\n"
        "        'Unicode data version mismatch: ' + unicodedata.unidata_version\n"
        "        + ' != ' + PINNED_UNICODE_VERSION\n"
        "    )\n\n"
        "def decode(token):\n"
        "    return ''.join(chr(int(part, 16)) for part in token.split('+'))\n\n"
        "def scalar_token(text):\n"
        "    return '+'.join(f'{ord(ch):04X}' for ch in text)\n\n"
        "def is_extend(cp):\n"
        "    return (\n"
        "        unicodedata.category(chr(cp)).startswith('M')\n"
        "        or 0xFE00 <= cp <= 0xFE0F\n"
        "        or 0xE0100 <= cp <= 0xE01EF\n"
        "        or 0x1F3FB <= cp <= 0x1F3FF\n"
        "    )\n\n"
        "def is_regional_indicator(cp):\n"
        "    return 0x1F1E6 <= cp <= 0x1F1FF\n\n"
        "def segment_subset(text):\n"
        "    cps = [ord(ch) for ch in text]\n"
        "    clusters = []\n"
        "    i = 0\n"
        "    ri_run = 0\n"
        "    while i < len(cps):\n"
        "        cp = cps[i]\n"
        "        cluster = [cp]\n"
        "        i += 1\n"
        "        if cp == 0x000D and i < len(cps) and cps[i] == 0x000A:\n"
        "            cluster.append(cps[i])\n"
        "            i += 1\n"
        "            ri_run = 0\n"
        "        elif is_regional_indicator(cp):\n"
        "            ri_run += 1\n"
        "            if i < len(cps) and is_regional_indicator(cps[i]) and ri_run % 2 == 1:\n"
        "                cluster.append(cps[i])\n"
        "                i += 1\n"
        "                ri_run += 1\n"
        "        else:\n"
        "            ri_run = 0\n"
        "        while i < len(cps) and is_extend(cps[i]):\n"
        "            cluster.append(cps[i])\n"
        "            i += 1\n"
        "        while i + 1 < len(cps) and cps[i] == 0x200D:\n"
        "            cluster.append(cps[i])\n"
        "            cluster.append(cps[i + 1])\n"
        "            i += 2\n"
        "            while i < len(cps) and is_extend(cps[i]):\n"
        "                cluster.append(cps[i])\n"
        "                i += 1\n"
        "        clusters.append(''.join(chr(value) for value in cluster))\n"
        "    return clusters\n\n"
        "profiles = {}\n"
        "for token in tokens:\n"
        "    nfc = unicodedata.normalize('NFC', decode(token))\n"
        "    clusters = segment_subset(nfc)\n"
        "    profiles[token] = {\n"
        "        'normalized': {'$unicode_nfc': scalar_token(nfc)},\n"
        "        'clusters': [{'$grapheme': scalar_token(item)} for item in clusters],\n"
        "        'count': {'$exact_integer': str(len(clusters))},\n"
        "    }\n\n"
        "result = {\n"
        "    'unicode_version': PINNED_UNICODE_VERSION,\n"
        "    'profile': 'bridge_uax29_subset_v1',\n"
        "    'profiles': profiles,\n"
        "}\n"
        "print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    program, task = program_and_task(doc)
    tokens = csv_values(task["values"])
    version = str(program["unicode_version"])
    js_tokens = "[" + ",".join(repr(token) for token in tokens) + "]"

    return (
        "// Generated from Bridge-0 v0.15. Do not hand-edit.\n"
        f"const PINNED_UNICODE_VERSION = {version!r};\n"
        f"const tokens = {js_tokens};\n\n"
        "function versionMatches(runtime, pinned) {\n"
        "  return runtime === pinned || runtime.startsWith(pinned + '.');\n"
        "}\n\n"
        "if (!versionMatches(process.versions.unicode, PINNED_UNICODE_VERSION)) {\n"
        "  throw new Error('Unicode data version mismatch: ' + process.versions.unicode + ' != ' + PINNED_UNICODE_VERSION);\n"
        "}\n\n"
        "function decode(token) {\n"
        "  return String.fromCodePoint(...token.split('+').map((part) => parseInt(part, 16)));\n"
        "}\n\n"
        "function scalarToken(text) {\n"
        "  return Array.from(text, (ch) => ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')).join('+');\n"
        "}\n\n"
        "const segmenter = new Intl.Segmenter('en', { granularity: 'grapheme' });\n"
        "const profiles = {};\n"
        "for (const token of tokens) {\n"
        "  const nfc = decode(token).normalize('NFC');\n"
        "  const clusters = Array.from(segmenter.segment(nfc), (entry) => entry.segment);\n"
        "  profiles[token] = {\n"
        "    normalized: { $unicode_nfc: scalarToken(nfc) },\n"
        "    clusters: clusters.map((item) => ({ $grapheme: scalarToken(item) })),\n"
        "    count: { $exact_integer: String(clusters.length) },\n"
        "  };\n"
        "}\n"
        "const result = {\n"
        "  unicode_version: PINNED_UNICODE_VERSION,\n"
        "  profile: 'bridge_uax29_subset_v1',\n"
        "  profiles,\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_unsafe_node_codepoints(doc: dict[str, Any]) -> str:
    program, task = program_and_task(doc)
    tokens = csv_values(task["values"])
    version = str(program["unicode_version"])
    js_tokens = "[" + ",".join(repr(token) for token in tokens) + "]"

    return (
        "// UNSAFE NEGATIVE CONTROL: code points masquerading as graphemes.\n"
        f"const PINNED_UNICODE_VERSION = {version!r};\n"
        f"const tokens = {js_tokens};\n"
        "function decode(token) {\n"
        "  return String.fromCodePoint(...token.split('+').map((part) => parseInt(part, 16)));\n"
        "}\n"
        "function scalarToken(text) {\n"
        "  return Array.from(text, (ch) => ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')).join('+');\n"
        "}\n"
        "const profiles = {};\n"
        "for (const token of tokens) {\n"
        "  const nfc = decode(token).normalize('NFC');\n"
        "  const clusters = Array.from(nfc);\n"
        "  profiles[token] = {\n"
        "    normalized: { $unicode_nfc: scalarToken(nfc) },\n"
        "    clusters: clusters.map((item) => ({ $grapheme: scalarToken(item) })),\n"
        "    count: { $exact_integer: String(clusters.length) },\n"
        "  };\n"
        "}\n"
        "process.stdout.write(JSON.stringify({ unicode_version: PINNED_UNICODE_VERSION, profile: 'bridge_uax29_subset_v1', profiles }) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeGraphemeCompileError(f"unsupported target: {target}")
