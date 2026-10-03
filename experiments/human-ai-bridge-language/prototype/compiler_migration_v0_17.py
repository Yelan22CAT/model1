#!/usr/bin/env python3
"""Bridge-0 v0.17 executable semantic migration compiler.

Core rule:
    successful conversion != lossless semantic migration

Two routes are compiled:
- v1_to_v2: reversible/lossless for the fixture.
- v1_to_v3_compact: convertible but intentionally lossy.

The audit, not mere conversion success, controls execution permission.
"""

from __future__ import annotations

import json
from typing import Any

from validator_v0_17 import validate_document


class BridgeMigrationCompileError(ValueError):
    pass


SOURCE_ARTIFACT = {
    "profile": "grapheme_v1",
    "artifact_id": "fixture_v1",
    "units": [
        {
            "id": "u1",
            "cluster": "1F469+200D+1F4BB",
            "label": "coder",
            "confidence": "verified",
        },
        {
            "id": "u2",
            "cluster": "00E9",
            "label": "accented_e",
            "confidence": "verified",
        },
    ],
    "provenance": {
        "source": "fixture",
        "evidence": "manual_conformance",
    },
    "notes": {
        "human_hint": "preserve semantic annotations",
    },
}


def validate_source(doc: dict[str, Any]) -> None:
    result = validate_document(doc)
    if not result["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in result["errors"]
        )
        raise BridgeMigrationCompileError(detail)


def audit_v1_to_v2(source: dict[str, Any]) -> dict[str, Any]:
    migrated = json.loads(json.dumps(source))
    migrated["profile"] = "grapheme_v2"

    reversed_artifact = json.loads(json.dumps(migrated))
    reversed_artifact["profile"] = "grapheme_v1"

    return {
        "route": "v1_to_v2",
        "conversion_success": True,
        "migrated": migrated,
        "roundtrip": {
            "attempted": True,
            "recovered_source": reversed_artifact == source,
        },
        "loss": {
            "lossless": True,
            "lost_paths": [],
        },
        "execution_allowed": True,
    }


def audit_v1_to_v3_compact(source: dict[str, Any]) -> dict[str, Any]:
    migrated = {
        "profile": "grapheme_v3_compact",
        "artifact_id": source["artifact_id"],
        "clusters": [unit["cluster"] for unit in source["units"]],
    }

    reconstructed = {
        "profile": "grapheme_v1",
        "artifact_id": migrated["artifact_id"],
        "units": [
            {"id": f"recovered_{index + 1}", "cluster": cluster}
            for index, cluster in enumerate(migrated["clusters"])
        ],
    }

    lost_paths = [
        "$.units[*].id",
        "$.units[*].label",
        "$.units[*].confidence",
        "$.provenance",
        "$.notes",
    ]

    return {
        "route": "v1_to_v3_compact",
        "conversion_success": True,
        "migrated": migrated,
        "roundtrip": {
            "attempted": True,
            "recovered_source": reconstructed == source,
        },
        "loss": {
            "lossless": False,
            "lost_paths": lost_paths,
        },
        "execution_allowed": False,
    }


def expected_result() -> dict[str, Any]:
    return {
        "policy": {
            "loss_policy": "reject_unacknowledged",
            "roundtrip": "audit",
            "execution": "gate_on_audit",
        },
        "source": SOURCE_ARTIFACT,
        "routes": {
            "v1_to_v2": audit_v1_to_v2(SOURCE_ARTIFACT),
            "v1_to_v3_compact": audit_v1_to_v3_compact(SOURCE_ARTIFACT),
        },
    }


def compile_python(doc: dict[str, Any]) -> str:
    validate_source(doc)
    source_json = json.dumps(SOURCE_ARTIFACT, sort_keys=True, separators=(",", ":"))
    return (
        "# Generated from Bridge-0 v0.17. Do not hand-edit.\n"
        "import copy\n"
        "import json\n\n"
        f"source = json.loads({source_json!r})\n\n"
        "def audit_v1_to_v2(source):\n"
        "    migrated = copy.deepcopy(source)\n"
        "    migrated['profile'] = 'grapheme_v2'\n"
        "    reversed_artifact = copy.deepcopy(migrated)\n"
        "    reversed_artifact['profile'] = 'grapheme_v1'\n"
        "    return {\n"
        "        'route': 'v1_to_v2',\n"
        "        'conversion_success': True,\n"
        "        'migrated': migrated,\n"
        "        'roundtrip': {'attempted': True, 'recovered_source': reversed_artifact == source},\n"
        "        'loss': {'lossless': True, 'lost_paths': []},\n"
        "        'execution_allowed': True,\n"
        "    }\n\n"
        "def audit_v1_to_v3_compact(source):\n"
        "    migrated = {\n"
        "        'profile': 'grapheme_v3_compact',\n"
        "        'artifact_id': source['artifact_id'],\n"
        "        'clusters': [unit['cluster'] for unit in source['units']],\n"
        "    }\n"
        "    reconstructed = {\n"
        "        'profile': 'grapheme_v1',\n"
        "        'artifact_id': migrated['artifact_id'],\n"
        "        'units': [\n"
        "            {'id': f'recovered_{i + 1}', 'cluster': cluster}\n"
        "            for i, cluster in enumerate(migrated['clusters'])\n"
        "        ],\n"
        "    }\n"
        "    lost_paths = [\n"
        "        '$.units[*].id', '$.units[*].label', '$.units[*].confidence',\n"
        "        '$.provenance', '$.notes',\n"
        "    ]\n"
        "    return {\n"
        "        'route': 'v1_to_v3_compact',\n"
        "        'conversion_success': True,\n"
        "        'migrated': migrated,\n"
        "        'roundtrip': {'attempted': True, 'recovered_source': reconstructed == source},\n"
        "        'loss': {'lossless': False, 'lost_paths': lost_paths},\n"
        "        'execution_allowed': False,\n"
        "    }\n\n"
        "result = {\n"
        "    'policy': {\n"
        "        'loss_policy': 'reject_unacknowledged',\n"
        "        'roundtrip': 'audit',\n"
        "        'execution': 'gate_on_audit',\n"
        "    },\n"
        "    'source': source,\n"
        "    'routes': {\n"
        "        'v1_to_v2': audit_v1_to_v2(source),\n"
        "        'v1_to_v3_compact': audit_v1_to_v3_compact(source),\n"
        "    },\n"
        "}\n"
        "print(json.dumps(result, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    validate_source(doc)
    source_json = json.dumps(SOURCE_ARTIFACT, sort_keys=True, separators=(",", ":"))
    return (
        "// Generated from Bridge-0 v0.17. Do not hand-edit.\n"
        f"const source = {source_json};\n\n"
        "const clone = (value) => JSON.parse(JSON.stringify(value));\n"
        "const canonical = (value) => JSON.stringify(value, Object.keys(value).sort());\n"
        "const deepEqual = (a, b) => JSON.stringify(a) === JSON.stringify(b);\n\n"
        "function auditV1ToV2(source) {\n"
        "  const migrated = clone(source);\n"
        "  migrated.profile = 'grapheme_v2';\n"
        "  const reversedArtifact = clone(migrated);\n"
        "  reversedArtifact.profile = 'grapheme_v1';\n"
        "  return {\n"
        "    route: 'v1_to_v2',\n"
        "    conversion_success: true,\n"
        "    migrated,\n"
        "    roundtrip: { attempted: true, recovered_source: deepEqual(reversedArtifact, source) },\n"
        "    loss: { lossless: true, lost_paths: [] },\n"
        "    execution_allowed: true,\n"
        "  };\n"
        "}\n\n"
        "function auditV1ToV3Compact(source) {\n"
        "  const migrated = {\n"
        "    profile: 'grapheme_v3_compact',\n"
        "    artifact_id: source.artifact_id,\n"
        "    clusters: source.units.map((unit) => unit.cluster),\n"
        "  };\n"
        "  const reconstructed = {\n"
        "    profile: 'grapheme_v1',\n"
        "    artifact_id: migrated.artifact_id,\n"
        "    units: migrated.clusters.map((cluster, i) => ({ id: 'recovered_' + (i + 1), cluster })),\n"
        "  };\n"
        "  const lostPaths = [\n"
        "    '$.units[*].id', '$.units[*].label', '$.units[*].confidence',\n"
        "    '$.provenance', '$.notes',\n"
        "  ];\n"
        "  return {\n"
        "    route: 'v1_to_v3_compact',\n"
        "    conversion_success: true,\n"
        "    migrated,\n"
        "    roundtrip: { attempted: true, recovered_source: deepEqual(reconstructed, source) },\n"
        "    loss: { lossless: false, lost_paths: lostPaths },\n"
        "    execution_allowed: false,\n"
        "  };\n"
        "}\n\n"
        "const result = {\n"
        "  policy: {\n"
        "    loss_policy: 'reject_unacknowledged',\n"
        "    roundtrip: 'audit',\n"
        "    execution: 'gate_on_audit',\n"
        "  },\n"
        "  source,\n"
        "  routes: {\n"
        "    v1_to_v2: auditV1ToV2(source),\n"
        "    v1_to_v3_compact: auditV1ToV3Compact(source),\n"
        "  },\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_unsafe_success_only_node(doc: dict[str, Any]) -> str:
    """Negative control: conversion success is incorrectly treated as permission."""
    validate_source(doc)
    source_json = json.dumps(SOURCE_ARTIFACT, sort_keys=True, separators=(",", ":"))
    return (
        "// UNSAFE NEGATIVE CONTROL: conversion success implies execution permission.\n"
        f"const source = {source_json};\n"
        "const migratedV2 = JSON.parse(JSON.stringify(source));\n"
        "migratedV2.profile = 'grapheme_v2';\n"
        "const migratedV3 = {\n"
        "  profile: 'grapheme_v3_compact',\n"
        "  artifact_id: source.artifact_id,\n"
        "  clusters: source.units.map((unit) => unit.cluster),\n"
        "};\n"
        "const result = {\n"
        "  policy: { loss_policy: 'reject_unacknowledged', roundtrip: 'audit', execution: 'gate_on_audit' },\n"
        "  source,\n"
        "  routes: {\n"
        "    v1_to_v2: {\n"
        "      route: 'v1_to_v2', conversion_success: true, migrated: migratedV2,\n"
        "      roundtrip: { attempted: false, recovered_source: null },\n"
        "      loss: { lossless: null, lost_paths: [] }, execution_allowed: true,\n"
        "    },\n"
        "    v1_to_v3_compact: {\n"
        "      route: 'v1_to_v3_compact', conversion_success: true, migrated: migratedV3,\n"
        "      roundtrip: { attempted: false, recovered_source: null },\n"
        "      loss: { lossless: null, lost_paths: [] }, execution_allowed: true,\n"
        "    },\n"
        "  },\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeMigrationCompileError(f"unsupported target: {target}")
