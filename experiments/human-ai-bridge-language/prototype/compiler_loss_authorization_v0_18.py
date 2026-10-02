#!/usr/bin/env python3
"""Bridge-0 v0.18 scoped authorization compiler.

Known semantic loss may be permitted only when acknowledgement, authority,
scope, artifact binding, provenance and time window all match.

Core rule:
    acknowledged loss != blanket permission
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from validator_v0_17 import EXPECTED_LOSS
from validator_v0_18 import EXPECTED_DIGEST, validate_document
from compiler_migration_v0_17 import SOURCE_ARTIFACT


class BridgeLossAuthorizationCompileError(ValueError):
    pass


def validate_source(doc: dict[str, Any]) -> None:
    result = validate_document(doc)
    if not result["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in result["errors"]
        )
        raise BridgeLossAuthorizationCompileError(detail)


def auth_task(doc: dict[str, Any]) -> dict[str, Any]:
    validate_source(doc)
    return next(
        s for s in doc["statements"]
        if s.get("kind") == "loss_authorization"
    )


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def evaluate(
    task: dict[str, Any],
    *,
    artifact_digest: str | None = None,
    loss_ack: list[str] | None = None,
    authority: str | None = None,
    scope: str | None = None,
    provenance: str | None = None,
    evaluate_at: str | None = None,
) -> dict[str, Any]:
    actual_digest = artifact_digest or canonical_digest(SOURCE_ARTIFACT)
    ack = sorted(loss_ack if loss_ack is not None else str(task["loss_ack"]).split("|"))
    expected_loss = sorted(EXPECTED_LOSS)
    auth = authority or str(task["authority"])
    scp = scope or str(task["scope"])
    prov = provenance or str(task["provenance"])
    at = evaluate_at or str(task["evaluate_at"])

    issued = parse_utc(str(task["issued_at"]))
    expires = parse_utc(str(task["expires_at"]))
    evaluated = parse_utc(at)

    checks = {
        "route_match": task["route"] == "v1_to_v3_compact",
        "loss_ack_exact": ack == expected_loss,
        "authority_match": auth == "fixture_owner",
        "scope_exact": scp == "exact_loss_manifest",
        "artifact_bound": actual_digest == str(task["artifact_digest"]) == EXPECTED_DIGEST,
        "provenance_bound": prov == "fixture_authority_record",
        "time_valid": issued <= evaluated < expires,
    }
    allowed = all(checks.values())

    return {
        "checks": checks,
        "execution_allowed": allowed,
        "decision": "authorized_known_loss" if allowed else "deny",
        "evaluated_at": at,
        "artifact_digest": actual_digest,
        "acknowledged_loss": ack,
    }


def expected_result(doc: dict[str, Any]) -> dict[str, Any]:
    task = auth_task(doc)
    valid = evaluate(task)
    expired = evaluate(task, evaluate_at="2026-10-02T13:00:00Z")
    wrong_artifact = evaluate(task, artifact_digest="0" * 64)
    partial_ack = evaluate(
        task,
        loss_ack=sorted(EXPECTED_LOSS - {"$.provenance"}),
    )
    wrong_scope = evaluate(task, scope="all_future_loss")
    wrong_authority = evaluate(task, authority="untrusted_agent")

    return {
        "policy": {
            "loss": "known_only",
            "scope": "exact_loss_manifest",
            "time_window": "issued_at<=evaluate_at<expires_at",
            "default": "deny",
        },
        "scenarios": {
            "authorized_exact": valid,
            "expired_replay": expired,
            "wrong_artifact": wrong_artifact,
            "partial_ack": partial_ack,
            "wrong_scope": wrong_scope,
            "wrong_authority": wrong_authority,
        },
    }


def compile_python(doc: dict[str, Any]) -> str:
    task = auth_task(doc)
    task_json = json.dumps(task, sort_keys=True, separators=(",", ":"))
    source_json = json.dumps(SOURCE_ARTIFACT, sort_keys=True, separators=(",", ":"))
    loss_json = json.dumps(sorted(EXPECTED_LOSS), separators=(",", ":"))

    return (
        "# Generated from Bridge-0 v0.18. Do not hand-edit.\n"
        "import hashlib\n"
        "import json\n"
        "from datetime import datetime, timezone\n\n"
        f"task = json.loads({task_json!r})\n"
        f"source = json.loads({source_json!r})\n"
        f"expected_loss = {loss_json}\n"
        f"expected_digest = {EXPECTED_DIGEST!r}\n\n"
        "def digest(value):\n"
        "    payload = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')\n"
        "    return hashlib.sha256(payload).hexdigest()\n\n"
        "def parse_utc(value):\n"
        "    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)\n\n"
        "def evaluate(*, artifact_digest=None, loss_ack=None, authority=None, scope=None, provenance=None, evaluate_at=None):\n"
        "    actual_digest = artifact_digest or digest(source)\n"
        "    ack = sorted(loss_ack if loss_ack is not None else task['loss_ack'].split('|'))\n"
        "    auth = authority or task['authority']\n"
        "    scp = scope or task['scope']\n"
        "    prov = provenance or task['provenance']\n"
        "    at = evaluate_at or task['evaluate_at']\n"
        "    issued = parse_utc(task['issued_at'])\n"
        "    expires = parse_utc(task['expires_at'])\n"
        "    evaluated = parse_utc(at)\n"
        "    checks = {\n"
        "        'route_match': task['route'] == 'v1_to_v3_compact',\n"
        "        'loss_ack_exact': ack == expected_loss,\n"
        "        'authority_match': auth == 'fixture_owner',\n"
        "        'scope_exact': scp == 'exact_loss_manifest',\n"
        "        'artifact_bound': actual_digest == task['artifact_digest'] == expected_digest,\n"
        "        'provenance_bound': prov == 'fixture_authority_record',\n"
        "        'time_valid': issued <= evaluated < expires,\n"
        "    }\n"
        "    allowed = all(checks.values())\n"
        "    return {\n"
        "        'checks': checks,\n"
        "        'execution_allowed': allowed,\n"
        "        'decision': 'authorized_known_loss' if allowed else 'deny',\n"
        "        'evaluated_at': at,\n"
        "        'artifact_digest': actual_digest,\n"
        "        'acknowledged_loss': ack,\n"
        "    }\n\n"
        "result = {\n"
        "    'policy': {\n"
        "        'loss': 'known_only',\n"
        "        'scope': 'exact_loss_manifest',\n"
        "        'time_window': 'issued_at<=evaluate_at<expires_at',\n"
        "        'default': 'deny',\n"
        "    },\n"
        "    'scenarios': {\n"
        "        'authorized_exact': evaluate(),\n"
        "        'expired_replay': evaluate(evaluate_at='2026-10-02T13:00:00Z'),\n"
        "        'wrong_artifact': evaluate(artifact_digest='0' * 64),\n"
        "        'partial_ack': evaluate(loss_ack=[x for x in expected_loss if x != '$.provenance']),\n"
        "        'wrong_scope': evaluate(scope='all_future_loss'),\n"
        "        'wrong_authority': evaluate(authority='untrusted_agent'),\n"
        "    },\n"
        "}\n"
        "print(json.dumps(result, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    task = auth_task(doc)
    task_json = json.dumps(task, sort_keys=True, separators=(",", ":"))
    source_json = json.dumps(SOURCE_ARTIFACT, sort_keys=True, separators=(",", ":"))
    loss_json = json.dumps(sorted(EXPECTED_LOSS), separators=(",", ":"))

    return (
        "// Generated from Bridge-0 v0.18. Do not hand-edit.\n"
        "import { createHash } from 'node:crypto';\n"
        f"const task = {task_json};\n"
        f"const source = {source_json};\n"
        f"const expectedLoss = {loss_json};\n"
        f"const expectedDigest = {json.dumps(EXPECTED_DIGEST)};\n\n"
        "function digest(value) {\n"
        "  return createHash('sha256').update(JSON.stringify(value)).digest('hex');\n"
        "}\n\n"
        "function evaluate(overrides = {}) {\n"
        "  const actualDigest = overrides.artifact_digest ?? digest(source);\n"
        "  const ack = [...(overrides.loss_ack ?? task.loss_ack.split('|'))].sort();\n"
        "  const auth = overrides.authority ?? task.authority;\n"
        "  const scope = overrides.scope ?? task.scope;\n"
        "  const provenance = overrides.provenance ?? task.provenance;\n"
        "  const at = overrides.evaluate_at ?? task.evaluate_at;\n"
        "  const issued = Date.parse(task.issued_at);\n"
        "  const expires = Date.parse(task.expires_at);\n"
        "  const evaluated = Date.parse(at);\n"
        "  const checks = {\n"
        "    route_match: task.route === 'v1_to_v3_compact',\n"
        "    loss_ack_exact: JSON.stringify(ack) === JSON.stringify(expectedLoss),\n"
        "    authority_match: auth === 'fixture_owner',\n"
        "    scope_exact: scope === 'exact_loss_manifest',\n"
        "    artifact_bound: actualDigest === task.artifact_digest && task.artifact_digest === expectedDigest,\n"
        "    provenance_bound: provenance === 'fixture_authority_record',\n"
        "    time_valid: issued <= evaluated && evaluated < expires,\n"
        "  };\n"
        "  const allowed = Object.values(checks).every(Boolean);\n"
        "  return {\n"
        "    checks,\n"
        "    execution_allowed: allowed,\n"
        "    decision: allowed ? 'authorized_known_loss' : 'deny',\n"
        "    evaluated_at: at,\n"
        "    artifact_digest: actualDigest,\n"
        "    acknowledged_loss: ack,\n"
        "  };\n"
        "}\n\n"
        "const result = {\n"
        "  policy: {\n"
        "    loss: 'known_only',\n"
        "    scope: 'exact_loss_manifest',\n"
        "    time_window: 'issued_at<=evaluate_at<expires_at',\n"
        "    default: 'deny',\n"
        "  },\n"
        "  scenarios: {\n"
        "    authorized_exact: evaluate(),\n"
        "    expired_replay: evaluate({ evaluate_at: '2026-10-02T13:00:00Z' }),\n"
        "    wrong_artifact: evaluate({ artifact_digest: '0'.repeat(64) }),\n"
        "    partial_ack: evaluate({ loss_ack: expectedLoss.filter((x) => x !== '$.provenance') }),\n"
        "    wrong_scope: evaluate({ scope: 'all_future_loss' }),\n"
        "    wrong_authority: evaluate({ authority: 'untrusted_agent' }),\n"
        "  },\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_unsafe_authority_only_node(doc: dict[str, Any]) -> str:
    """Negative control: authority label alone becomes blanket permission."""
    task = auth_task(doc)
    task_json = json.dumps(task, sort_keys=True, separators=(",", ":"))
    source_json = json.dumps(SOURCE_ARTIFACT, sort_keys=True, separators=(",", ":"))

    return (
        "// UNSAFE NEGATIVE CONTROL: authority label grants blanket permission.\n"
        f"const task = {task_json};\n"
        f"const source = {source_json};\n"
        "function unsafe(label, evaluatedAt) {\n"
        "  const allowed = label === 'fixture_owner';\n"
        "  return {\n"
        "    checks: { authority_match: allowed },\n"
        "    execution_allowed: allowed,\n"
        "    decision: allowed ? 'authorized_known_loss' : 'deny',\n"
        "    evaluated_at: evaluatedAt,\n"
        "    artifact_digest: task.artifact_digest,\n"
        "    acknowledged_loss: task.loss_ack.split('|').sort(),\n"
        "  };\n"
        "}\n"
        "const result = {\n"
        "  policy: { loss: 'known_only', scope: 'exact_loss_manifest', time_window: 'issued_at<=evaluate_at<expires_at', default: 'deny' },\n"
        "  scenarios: {\n"
        "    authorized_exact: unsafe(task.authority, task.evaluate_at),\n"
        "    expired_replay: unsafe(task.authority, '2026-10-02T13:00:00Z'),\n"
        "    wrong_artifact: unsafe(task.authority, task.evaluate_at),\n"
        "    partial_ack: unsafe(task.authority, task.evaluate_at),\n"
        "    wrong_scope: unsafe(task.authority, task.evaluate_at),\n"
        "    wrong_authority: unsafe('untrusted_agent', task.evaluate_at),\n"
        "  },\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeLossAuthorizationCompileError(f"unsupported target: {target}")
