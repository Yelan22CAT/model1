#!/usr/bin/env python3
"""Bridge-0 v0.15 pinned Unicode/grapheme compiler.

This round intentionally carries a bounded Bridge-owned Unicode 15.0 profile
instead of trusting the backend runtime Unicode version.
"""

from __future__ import annotations

from typing import Any

from validator_v0_15 import csv_values, validate_document


class BridgeGraphemeCompileError(ValueError):
    pass


PINNED_NFC = {
    "0065+0301": "00E9",
    "0061+0308+0062": "00E4+0062",
}


def program_and_task(doc: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    validation = validate_document(doc)
    if not validation["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in validation["errors"]
        )
        raise BridgeGraphemeCompileError(detail)
    program = next(s for s in doc["statements"] if s.get("kind") == "program")
    task = next(s for s in doc["statements"] if s.get("kind") == "semantic_compute")
    return program, task


def compile_python(doc: dict[str, Any]) -> str:
    program, task = program_and_task(doc)
    tokens = csv_values(task["values"])
    version = str(program["unicode_version"])

    return (
        "# Generated from Bridge-0 v0.15. Do not hand-edit.\n"
        "import json\n"
        "import sys\n"
        "import unicodedata\n\n"
        f"SEMANTIC_UNICODE_VERSION = {version!r}\n"
        f"tokens = {tokens!r}\n"
        f"PINNED_NFC = {PINNED_NFC!r}\n\n"
        "print(\n"
        "    'BRIDGE_UNICODE_RUNTIME runtime=' + unicodedata.unidata_version\n"
        "    + ' semantic=' + SEMANTIC_UNICODE_VERSION\n"
        "    + ' mode=pinned_subset',\n"
        "    file=sys.stderr,\n"
        ")\n\n"
        "def normalize_token(token):\n"
        "    return PINNED_NFC.get(token, token)\n\n"
        "def parse_token(token):\n"
        "    return [int(part, 16) for part in token.split('+')]\n\n"
        "def scalar_token(cps):\n"
        "    return '+'.join(f'{cp:04X}' for cp in cps)\n\n"
        "def is_extend(cp):\n"
        "    return (\n"
        "        0xFE00 <= cp <= 0xFE0F\n"
        "        or 0xE0100 <= cp <= 0xE01EF\n"
        "        or 0x1F3FB <= cp <= 0x1F3FF\n"
        "    )\n\n"
        "def is_regional_indicator(cp):\n"
        "    return 0x1F1E6 <= cp <= 0x1F1FF\n\n"
        "def segment_subset(cps):\n"
        "    clusters = []\n"
        "    i = 0\n"
        "    while i < len(cps):\n"
        "        cp = cps[i]\n"
        "        cluster = [cp]\n"
        "        i += 1\n"
        "        if cp == 0x000D and i < len(cps) and cps[i] == 0x000A:\n"
        "            cluster.append(cps[i])\n"
        "            i += 1\n"
        "        elif is_regional_indicator(cp):\n"
        "            if i < len(cps) and is_regional_indicator(cps[i]):\n"
        "                cluster.append(cps[i])\n"
        "                i += 1\n"
        "        while i < len(cps) and is_extend(cps[i]):\n"
        "            cluster.append(cps[i])\n"
        "            i += 1\n"
        "        while i + 1 < len(cps) and cps[i] == 0x200D:\n"
        "            cluster.extend([cps[i], cps[i + 1]])\n"
        "            i += 2\n"
        "            while i < len(cps) and is_extend(cps[i]):\n"
        "                cluster.append(cps[i])\n"
        "                i += 1\n"
        "        clusters.append(cluster)\n"
        "    return clusters\n\n"
        "profiles = {}\n"
        "for token in tokens:\n"
        "    normalized_token = normalize_token(token)\n"
        "    cps = parse_token(normalized_token)\n"
        "    clusters = segment_subset(cps)\n"
        "    profiles[token] = {\n"
        "        'normalized': {'$unicode_nfc': normalized_token},\n"
        "        'clusters': [{'$grapheme': scalar_token(item)} for item in clusters],\n"
        "        'count': {'$exact_integer': str(len(clusters))},\n"
        "    }\n\n"
        "result = {\n"
        "    'unicode_version': SEMANTIC_UNICODE_VERSION,\n"
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
    pinned_pairs = ",".join(
        f"{key!r}:{value!r}" for key, value in PINNED_NFC.items()
    )

    return (
        "// Generated from Bridge-0 v0.15. Do not hand-edit.\n"
        f"const SEMANTIC_UNICODE_VERSION = {version!r};\n"
        f"const tokens = {js_tokens};\n"
        f"const PINNED_NFC = {{{pinned_pairs}}};\n\n"
        "console.error('BRIDGE_UNICODE_RUNTIME runtime=' + process.versions.unicode\n"
        "  + ' semantic=' + SEMANTIC_UNICODE_VERSION + ' mode=pinned_subset');\n\n"
        "function normalizeToken(token) {\n"
        "  return PINNED_NFC[token] || token;\n"
        "}\n\n"
        "function parseToken(token) {\n"
        "  return token.split('+').map((part) => parseInt(part, 16));\n"
        "}\n\n"
        "function scalarToken(cps) {\n"
        "  return cps.map((cp) => cp.toString(16).toUpperCase().padStart(4, '0')).join('+');\n"
        "}\n\n"
        "function isExtend(cp) {\n"
        "  return (cp >= 0xFE00 && cp <= 0xFE0F)\n"
        "    || (cp >= 0xE0100 && cp <= 0xE01EF)\n"
        "    || (cp >= 0x1F3FB && cp <= 0x1F3FF);\n"
        "}\n\n"
        "function isRegionalIndicator(cp) {\n"
        "  return cp >= 0x1F1E6 && cp <= 0x1F1FF;\n"
        "}\n\n"
        "function segmentSubset(cps) {\n"
        "  const clusters = [];\n"
        "  let i = 0;\n"
        "  while (i < cps.length) {\n"
        "    const cp = cps[i];\n"
        "    const cluster = [cp];\n"
        "    i += 1;\n"
        "    if (cp === 0x000D && i < cps.length && cps[i] === 0x000A) {\n"
        "      cluster.push(cps[i]);\n"
        "      i += 1;\n"
        "    } else if (isRegionalIndicator(cp)) {\n"
        "      if (i < cps.length && isRegionalIndicator(cps[i])) {\n"
        "        cluster.push(cps[i]);\n"
        "        i += 1;\n"
        "      }\n"
        "    }\n"
        "    while (i < cps.length && isExtend(cps[i])) {\n"
        "      cluster.push(cps[i]);\n"
        "      i += 1;\n"
        "    }\n"
        "    while (i + 1 < cps.length && cps[i] === 0x200D) {\n"
        "      cluster.push(cps[i], cps[i + 1]);\n"
        "      i += 2;\n"
        "      while (i < cps.length && isExtend(cps[i])) {\n"
        "        cluster.push(cps[i]);\n"
        "        i += 1;\n"
        "      }\n"
        "    }\n"
        "    clusters.push(cluster);\n"
        "  }\n"
        "  return clusters;\n"
        "}\n\n"
        "const profiles = {};\n"
        "for (const token of tokens) {\n"
        "  const normalizedToken = normalizeToken(token);\n"
        "  const cps = parseToken(normalizedToken);\n"
        "  const clusters = segmentSubset(cps);\n"
        "  profiles[token] = {\n"
        "    normalized: { $unicode_nfc: normalizedToken },\n"
        "    clusters: clusters.map((item) => ({ $grapheme: scalarToken(item) })),\n"
        "    count: { $exact_integer: String(clusters.length) },\n"
        "  };\n"
        "}\n"
        "const result = {\n"
        "  unicode_version: SEMANTIC_UNICODE_VERSION,\n"
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
        f"const SEMANTIC_UNICODE_VERSION = {version!r};\n"
        f"const tokens = {js_tokens};\n"
        "const profiles = {};\n"
        "for (const token of tokens) {\n"
        "  const cps = token.split('+');\n"
        "  profiles[token] = {\n"
        "    normalized: { $unicode_nfc: token },\n"
        "    clusters: cps.map((item) => ({ $grapheme: item })),\n"
        "    count: { $exact_integer: String(cps.length) },\n"
        "  };\n"
        "}\n"
        "process.stdout.write(JSON.stringify({ unicode_version: SEMANTIC_UNICODE_VERSION, profile: 'bridge_uax29_subset_v1', profiles }) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeGraphemeCompileError(f"unsupported target: {target}")
