#!/usr/bin/env python3
"""Bridge-0 v0.16 semantic-profile evolution compiler.

The compatibility decision is based on a behavioral manifest, not only on a
version label. v3_breaking intentionally carries a same-major version while
changing one existing behavior, so a semver-only policy becomes a negative
control.
"""

from __future__ import annotations

import json
from typing import Any

from validator_v0_16 import validate_document


class BridgeCompatibilityCompileError(ValueError):
    pass


PROFILES = {
    "grapheme_v1": {
        "version": "1.0.0",
        "behavior": {
            "0065+0301": ["00E9"],
            "1F469+200D+1F4BB": ["1F469+200D+1F4BB"],
            "1F1E8+1F1E6": ["1F1E8+1F1E6"],
        },
    },
    "grapheme_v2": {
        "version": "1.1.0",
        "behavior": {
            "0065+0301": ["00E9"],
            "1F469+200D+1F4BB": ["1F469+200D+1F4BB"],
            "1F1E8+1F1E6": ["1F1E8+1F1E6"],
            "2764+FE0F": ["2764+FE0F"],
        },
    },
    "grapheme_v3_breaking": {
        "version": "1.2.0",
        "behavior": {
            "0065+0301": ["00E9"],
            "1F469+200D+1F4BB": ["1F469", "200D", "1F4BB"],
            "1F1E8+1F1E6": ["1F1E8+1F1E6"],
            "2764+FE0F": ["2764+FE0F"],
        },
    },
}


def compatibility(base: dict[str, Any], other: dict[str, Any]) -> dict[str, Any]:
    b = base["behavior"]
    o = other["behavior"]
    base_keys = set(b)
    other_keys = set(o)

    removed = sorted(base_keys - other_keys)
    added = sorted(other_keys - base_keys)
    changed = sorted(key for key in base_keys & other_keys if b[key] != o[key])

    if removed or changed:
        relation = "breaking"
        exchange_allowed = False
        migration_required = True
    elif added:
        relation = "backward_compatible_extension"
        exchange_allowed = True
        migration_required = False
    else:
        relation = "equivalent"
        exchange_allowed = True
        migration_required = False

    base_major = str(base["version"]).split(".", 1)[0]
    other_major = str(other["version"]).split(".", 1)[0]
    semver_same_major_claim = base_major == other_major

    return {
        "relation": relation,
        "exchange_allowed": exchange_allowed,
        "migration_required": migration_required,
        "added": added,
        "removed": removed,
        "changed": changed,
        "semver_same_major_claim": semver_same_major_claim,
    }


def expected_result() -> dict[str, Any]:
    base = PROFILES["grapheme_v1"]
    return {
        "policy": "behavioral_manifest",
        "migration": "explicit",
        "profiles": {
            name: {
                "version": data["version"],
                "behavior": data["behavior"],
            }
            for name, data in PROFILES.items()
        },
        "comparisons": {
            "grapheme_v1->grapheme_v2": compatibility(base, PROFILES["grapheme_v2"]),
            "grapheme_v1->grapheme_v3_breaking": compatibility(
                base, PROFILES["grapheme_v3_breaking"]
            ),
        },
    }


def validate_source(doc: dict[str, Any]) -> None:
    result = validate_document(doc)
    if not result["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in result["errors"]
        )
        raise BridgeCompatibilityCompileError(detail)


def compile_python(doc: dict[str, Any]) -> str:
    validate_source(doc)
    payload = json.dumps(PROFILES, sort_keys=True, separators=(",", ":"))
    return (
        "# Generated from Bridge-0 v0.16. Do not hand-edit.\n"
        "import json\n\n"
        f"profiles = json.loads({payload!r})\n\n"
        "def compatibility(base, other):\n"
        "    b = base['behavior']\n"
        "    o = other['behavior']\n"
        "    base_keys = set(b)\n"
        "    other_keys = set(o)\n"
        "    removed = sorted(base_keys - other_keys)\n"
        "    added = sorted(other_keys - base_keys)\n"
        "    changed = sorted(k for k in base_keys & other_keys if b[k] != o[k])\n"
        "    breaking = bool(removed or changed)\n"
        "    relation = 'breaking' if breaking else ('backward_compatible_extension' if added else 'equivalent')\n"
        "    return {\n"
        "        'relation': relation,\n"
        "        'exchange_allowed': not breaking,\n"
        "        'migration_required': breaking,\n"
        "        'added': added,\n"
        "        'removed': removed,\n"
        "        'changed': changed,\n"
        "        'semver_same_major_claim': base['version'].split('.', 1)[0] == other['version'].split('.', 1)[0],\n"
        "    }\n\n"
        "base = profiles['grapheme_v1']\n"
        "result = {\n"
        "    'policy': 'behavioral_manifest',\n"
        "    'migration': 'explicit',\n"
        "    'profiles': profiles,\n"
        "    'comparisons': {\n"
        "        'grapheme_v1->grapheme_v2': compatibility(base, profiles['grapheme_v2']),\n"
        "        'grapheme_v1->grapheme_v3_breaking': compatibility(base, profiles['grapheme_v3_breaking']),\n"
        "    },\n"
        "}\n"
        "print(json.dumps(result, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    validate_source(doc)
    payload = json.dumps(PROFILES, sort_keys=True, separators=(",", ":"))
    return (
        "// Generated from Bridge-0 v0.16. Do not hand-edit.\n"
        f"const profiles = {payload};\n\n"
        "function compatibility(base, other) {\n"
        "  const baseKeys = Object.keys(base.behavior);\n"
        "  const otherKeys = Object.keys(other.behavior);\n"
        "  const removed = baseKeys.filter((k) => !(k in other.behavior)).sort();\n"
        "  const added = otherKeys.filter((k) => !(k in base.behavior)).sort();\n"
        "  const changed = baseKeys.filter((k) => (k in other.behavior)\n"
        "    && JSON.stringify(base.behavior[k]) !== JSON.stringify(other.behavior[k])).sort();\n"
        "  const breaking = removed.length > 0 || changed.length > 0;\n"
        "  const relation = breaking ? 'breaking' : (added.length ? 'backward_compatible_extension' : 'equivalent');\n"
        "  return {\n"
        "    relation,\n"
        "    exchange_allowed: !breaking,\n"
        "    migration_required: breaking,\n"
        "    added,\n"
        "    removed,\n"
        "    changed,\n"
        "    semver_same_major_claim: base.version.split('.', 1)[0] === other.version.split('.', 1)[0],\n"
        "  };\n"
        "}\n\n"
        "const base = profiles.grapheme_v1;\n"
        "const result = {\n"
        "  policy: 'behavioral_manifest',\n"
        "  migration: 'explicit',\n"
        "  profiles,\n"
        "  comparisons: {\n"
        "    'grapheme_v1->grapheme_v2': compatibility(base, profiles.grapheme_v2),\n"
        "    'grapheme_v1->grapheme_v3_breaking': compatibility(base, profiles.grapheme_v3_breaking),\n"
        "  },\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_unsafe_semver_only_node(doc: dict[str, Any]) -> str:
    """Negative control: accepts same-major versions without behavioral diff."""
    validate_source(doc)
    payload = json.dumps(PROFILES, sort_keys=True, separators=(",", ":"))
    return (
        "// UNSAFE NEGATIVE CONTROL: semver-major only compatibility.\n"
        f"const profiles = {payload};\n"
        "const base = profiles.grapheme_v1;\n"
        "const comparisons = {};\n"
        "for (const name of ['grapheme_v2', 'grapheme_v3_breaking']) {\n"
        "  const other = profiles[name];\n"
        "  const sameMajor = base.version.split('.', 1)[0] === other.version.split('.', 1)[0];\n"
        "  comparisons['grapheme_v1->' + name] = {\n"
        "    relation: sameMajor ? 'compatible_by_label' : 'breaking',\n"
        "    exchange_allowed: sameMajor,\n"
        "    migration_required: !sameMajor,\n"
        "    added: [], removed: [], changed: [],\n"
        "    semver_same_major_claim: sameMajor,\n"
        "  };\n"
        "}\n"
        "process.stdout.write(JSON.stringify({ policy: 'behavioral_manifest', migration: 'explicit', profiles, comparisons }) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeCompatibilityCompileError(f"unsupported target: {target}")
