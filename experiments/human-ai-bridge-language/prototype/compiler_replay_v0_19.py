#!/usr/bin/env python3
"""Bridge-0 v0.19 revocation / replay-resistance compiler.

Core rules:
- valid once != valid forever
- authority token identity and nonce are consumed on successful use
- revocation state wins over otherwise-valid authorization
- stale revocation epoch is denied
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from validator_v0_19 import (
    EXPECTED_DIGEST,
    EXPECTED_LOSS,
    EXPECTED_REVOCATION_EPOCH,
    validate_document,
)


class BridgeReplayCompileError(ValueError):
    pass


def validate_source(doc: dict[str, Any]) -> None:
    result = validate_document(doc)
    if not result["valid"]:
        detail = "; ".join(
            f"{e.get('rule')}: {e.get('message')}"
            for e in result["errors"]
        )
        raise BridgeReplayCompileError(detail)


def auth_task(doc: dict[str, Any]) -> dict[str, Any]:
    validate_source(doc)
    return next(
        s for s in doc["statements"]
        if s.get("kind") == "single_use_authorization"
    )


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def fresh_state(
    *,
    current_epoch: int = EXPECTED_REVOCATION_EPOCH,
    revoked: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "current_revocation_epoch": current_epoch,
        "revoked_authorization_ids": sorted(revoked or []),
        "used_authorization_ids": [],
        "used_nonces": [],
    }


def attempt(
    task: dict[str, Any],
    state: dict[str, Any],
    *,
    presented_authorization_id: str | None = None,
    presented_nonce: str | None = None,
    evaluate_at: str | None = None,
) -> dict[str, Any]:
    auth_id = presented_authorization_id or str(task["authorization_id"])
    nonce = presented_nonce or str(task["nonce"])
    at = evaluate_at or str(task["evaluate_at"])

    issued = parse_utc(str(task["issued_at"]))
    expires = parse_utc(str(task["expires_at"]))
    evaluated = parse_utc(at)

    ack = sorted(str(task["loss_ack"]).split("|"))
    token_epoch = int(str(task["revocation_epoch"]))

    checks = {
        "authorization_id_match": auth_id == str(task["authorization_id"]),
        "nonce_match": nonce == str(task["nonce"]),
        "loss_ack_exact": ack == sorted(EXPECTED_LOSS),
        "authority_match": task["authority"] == "fixture_owner",
        "scope_exact": task["scope"] == "exact_loss_manifest",
        "artifact_bound": task["artifact_digest"] == EXPECTED_DIGEST,
        "provenance_bound": task["provenance"] == "fixture_authority_record",
        "time_valid": issued <= evaluated < expires,
        "revocation_epoch_current": token_epoch == int(state["current_revocation_epoch"]),
        "not_revoked": auth_id not in state["revoked_authorization_ids"],
        "authorization_id_unused": auth_id not in state["used_authorization_ids"],
        "nonce_unused": nonce not in state["used_nonces"],
        "single_use": task["usage"] == "single_use",
    }

    allowed = all(checks.values())
    before = json.loads(json.dumps(state))

    if allowed:
        state["used_authorization_ids"].append(auth_id)
        state["used_authorization_ids"].sort()
        state["used_nonces"].append(nonce)
        state["used_nonces"].sort()

    after = json.loads(json.dumps(state))
    return {
        "checks": checks,
        "decision": "authorized_once" if allowed else "deny",
        "execution_allowed": allowed,
        "evaluate_at": at,
        "presented_authorization_id": auth_id,
        "presented_nonce": nonce,
        "state_before": before,
        "state_after": after,
    }


def expected_result(doc: dict[str, Any]) -> dict[str, Any]:
    task = auth_task(doc)

    replay_state = fresh_state()
    first_use = attempt(task, replay_state)
    replay = attempt(task, replay_state)

    revoked_state = fresh_state(revoked=[str(task["authorization_id"])])
    revoked = attempt(task, revoked_state)

    stale_epoch_state = fresh_state(current_epoch=EXPECTED_REVOCATION_EPOCH + 1)
    stale_epoch = attempt(task, stale_epoch_state)

    tampered_nonce_state = fresh_state()
    tampered_nonce = attempt(
        task,
        tampered_nonce_state,
        presented_nonce="nonce-tampered-0001",
    )

    expired_state = fresh_state()
    expired = attempt(
        task,
        expired_state,
        evaluate_at=str(task["expires_at"]),
    )

    return {
        "policy": {
            "usage": "single_use",
            "revocation": "deny_if_revoked",
            "freshness": "revocation_epoch_must_match",
            "replay": "consume_authorization_id_and_nonce",
            "default": "deny",
        },
        "scenarios": {
            "first_use": first_use,
            "replay_same_token": replay,
            "revoked_before_use": revoked,
            "stale_revocation_epoch": stale_epoch,
            "tampered_nonce": tampered_nonce,
            "expired_token": expired,
        },
    }


def compile_python(doc: dict[str, Any]) -> str:
    task = auth_task(doc)
    task_json = json.dumps(task, sort_keys=True, separators=(",", ":"))
    expected_loss_json = json.dumps(sorted(EXPECTED_LOSS), separators=(",", ":"))
    return (
        "# Generated from Bridge-0 v0.19. Do not hand-edit.\n"
        "import copy\n"
        "import json\n"
        "from datetime import datetime, timezone\n\n"
        f"task = json.loads({task_json!r})\n"
        f"expected_loss = {expected_loss_json}\n"
        f"expected_digest = {EXPECTED_DIGEST!r}\n"
        f"expected_epoch = {EXPECTED_REVOCATION_EPOCH}\n\n"
        "def parse_utc(value):\n"
        "    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)\n\n"
        "def fresh_state(current_epoch=expected_epoch, revoked=None):\n"
        "    return {\n"
        "        'current_revocation_epoch': current_epoch,\n"
        "        'revoked_authorization_ids': sorted(revoked or []),\n"
        "        'used_authorization_ids': [],\n"
        "        'used_nonces': [],\n"
        "    }\n\n"
        "def attempt(state, authorization_id=None, nonce=None, evaluate_at=None):\n"
        "    auth_id = authorization_id or task['authorization_id']\n"
        "    nonce_value = nonce or task['nonce']\n"
        "    at = evaluate_at or task['evaluate_at']\n"
        "    issued = parse_utc(task['issued_at'])\n"
        "    expires = parse_utc(task['expires_at'])\n"
        "    evaluated = parse_utc(at)\n"
        "    ack = sorted(task['loss_ack'].split('|'))\n"
        "    checks = {\n"
        "        'authorization_id_match': auth_id == task['authorization_id'],\n"
        "        'nonce_match': nonce_value == task['nonce'],\n"
        "        'loss_ack_exact': ack == expected_loss,\n"
        "        'authority_match': task['authority'] == 'fixture_owner',\n"
        "        'scope_exact': task['scope'] == 'exact_loss_manifest',\n"
        "        'artifact_bound': task['artifact_digest'] == expected_digest,\n"
        "        'provenance_bound': task['provenance'] == 'fixture_authority_record',\n"
        "        'time_valid': issued <= evaluated < expires,\n"
        "        'revocation_epoch_current': int(task['revocation_epoch']) == int(state['current_revocation_epoch']),\n"
        "        'not_revoked': auth_id not in state['revoked_authorization_ids'],\n"
        "        'authorization_id_unused': auth_id not in state['used_authorization_ids'],\n"
        "        'nonce_unused': nonce_value not in state['used_nonces'],\n"
        "        'single_use': task['usage'] == 'single_use',\n"
        "    }\n"
        "    allowed = all(checks.values())\n"
        "    before = copy.deepcopy(state)\n"
        "    if allowed:\n"
        "        state['used_authorization_ids'] = sorted(state['used_authorization_ids'] + [auth_id])\n"
        "        state['used_nonces'] = sorted(state['used_nonces'] + [nonce_value])\n"
        "    after = copy.deepcopy(state)\n"
        "    return {\n"
        "        'checks': checks,\n"
        "        'decision': 'authorized_once' if allowed else 'deny',\n"
        "        'execution_allowed': allowed,\n"
        "        'evaluate_at': at,\n"
        "        'presented_authorization_id': auth_id,\n"
        "        'presented_nonce': nonce_value,\n"
        "        'state_before': before,\n"
        "        'state_after': after,\n"
        "    }\n\n"
        "replay_state = fresh_state()\n"
        "first_use = attempt(replay_state)\n"
        "replay = attempt(replay_state)\n"
        "revoked = attempt(fresh_state(revoked=[task['authorization_id']]))\n"
        "stale = attempt(fresh_state(current_epoch=expected_epoch + 1))\n"
        "tampered = attempt(fresh_state(), nonce='nonce-tampered-0001')\n"
        "expired = attempt(fresh_state(), evaluate_at=task['expires_at'])\n"
        "result = {\n"
        "    'policy': {\n"
        "        'usage': 'single_use',\n"
        "        'revocation': 'deny_if_revoked',\n"
        "        'freshness': 'revocation_epoch_must_match',\n"
        "        'replay': 'consume_authorization_id_and_nonce',\n"
        "        'default': 'deny',\n"
        "    },\n"
        "    'scenarios': {\n"
        "        'first_use': first_use,\n"
        "        'replay_same_token': replay,\n"
        "        'revoked_before_use': revoked,\n"
        "        'stale_revocation_epoch': stale,\n"
        "        'tampered_nonce': tampered,\n"
        "        'expired_token': expired,\n"
        "    },\n"
        "}\n"
        "print(json.dumps(result, sort_keys=True, separators=(',', ':')))\n"
    )


def compile_node(doc: dict[str, Any]) -> str:
    task = auth_task(doc)
    task_json = json.dumps(task, sort_keys=True, separators=(",", ":"))
    expected_loss_json = json.dumps(sorted(EXPECTED_LOSS), separators=(",", ":"))
    return (
        "// Generated from Bridge-0 v0.19. Do not hand-edit.\n"
        f"const task = {task_json};\n"
        f"const expectedLoss = {expected_loss_json};\n"
        f"const expectedDigest = {json.dumps(EXPECTED_DIGEST)};\n"
        f"const expectedEpoch = {EXPECTED_REVOCATION_EPOCH};\n\n"
        "const clone = (value) => JSON.parse(JSON.stringify(value));\n"
        "function freshState(currentEpoch = expectedEpoch, revoked = []) {\n"
        "  return {\n"
        "    current_revocation_epoch: currentEpoch,\n"
        "    revoked_authorization_ids: [...revoked].sort(),\n"
        "    used_authorization_ids: [],\n"
        "    used_nonces: [],\n"
        "  };\n"
        "}\n\n"
        "function attempt(state, overrides = {}) {\n"
        "  const authId = overrides.authorization_id ?? task.authorization_id;\n"
        "  const nonce = overrides.nonce ?? task.nonce;\n"
        "  const at = overrides.evaluate_at ?? task.evaluate_at;\n"
        "  const issued = Date.parse(task.issued_at);\n"
        "  const expires = Date.parse(task.expires_at);\n"
        "  const evaluated = Date.parse(at);\n"
        "  const ack = [...task.loss_ack.split('|')].sort();\n"
        "  const checks = {\n"
        "    authorization_id_match: authId === task.authorization_id,\n"
        "    nonce_match: nonce === task.nonce,\n"
        "    loss_ack_exact: JSON.stringify(ack) === JSON.stringify(expectedLoss),\n"
        "    authority_match: task.authority === 'fixture_owner',\n"
        "    scope_exact: task.scope === 'exact_loss_manifest',\n"
        "    artifact_bound: task.artifact_digest === expectedDigest,\n"
        "    provenance_bound: task.provenance === 'fixture_authority_record',\n"
        "    time_valid: issued <= evaluated && evaluated < expires,\n"
        "    revocation_epoch_current: Number(task.revocation_epoch) === Number(state.current_revocation_epoch),\n"
        "    not_revoked: !state.revoked_authorization_ids.includes(authId),\n"
        "    authorization_id_unused: !state.used_authorization_ids.includes(authId),\n"
        "    nonce_unused: !state.used_nonces.includes(nonce),\n"
        "    single_use: task.usage === 'single_use',\n"
        "  };\n"
        "  const allowed = Object.values(checks).every(Boolean);\n"
        "  const before = clone(state);\n"
        "  if (allowed) {\n"
        "    state.used_authorization_ids = [...state.used_authorization_ids, authId].sort();\n"
        "    state.used_nonces = [...state.used_nonces, nonce].sort();\n"
        "  }\n"
        "  const after = clone(state);\n"
        "  return {\n"
        "    checks,\n"
        "    decision: allowed ? 'authorized_once' : 'deny',\n"
        "    execution_allowed: allowed,\n"
        "    evaluate_at: at,\n"
        "    presented_authorization_id: authId,\n"
        "    presented_nonce: nonce,\n"
        "    state_before: before,\n"
        "    state_after: after,\n"
        "  };\n"
        "}\n\n"
        "const replayState = freshState();\n"
        "const firstUse = attempt(replayState);\n"
        "const replay = attempt(replayState);\n"
        "const revoked = attempt(freshState(expectedEpoch, [task.authorization_id]));\n"
        "const stale = attempt(freshState(expectedEpoch + 1));\n"
        "const tampered = attempt(freshState(), { nonce: 'nonce-tampered-0001' });\n"
        "const expired = attempt(freshState(), { evaluate_at: task.expires_at });\n"
        "const result = {\n"
        "  policy: {\n"
        "    usage: 'single_use',\n"
        "    revocation: 'deny_if_revoked',\n"
        "    freshness: 'revocation_epoch_must_match',\n"
        "    replay: 'consume_authorization_id_and_nonce',\n"
        "    default: 'deny',\n"
        "  },\n"
        "  scenarios: {\n"
        "    first_use: firstUse,\n"
        "    replay_same_token: replay,\n"
        "    revoked_before_use: revoked,\n"
        "    stale_revocation_epoch: stale,\n"
        "    tampered_nonce: tampered,\n"
        "    expired_token: expired,\n"
        "  },\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_unsafe_stateless_node(doc: dict[str, Any]) -> str:
    """Negative control: ignores revocation, nonce consumption and epoch freshness."""
    task = auth_task(doc)
    task_json = json.dumps(task, sort_keys=True, separators=(",", ":"))
    return (
        "// UNSAFE NEGATIVE CONTROL: stateless reusable authorization.\n"
        f"const task = {task_json};\n"
        "function unsafe(overrides = {}) {\n"
        "  const at = overrides.evaluate_at ?? task.evaluate_at;\n"
        "  const authId = overrides.authorization_id ?? task.authorization_id;\n"
        "  const nonce = overrides.nonce ?? task.nonce;\n"
        "  const allowed = task.authority === 'fixture_owner' && Date.parse(at) < Date.parse(task.expires_at);\n"
        "  return {\n"
        "    checks: { authority_match: task.authority === 'fixture_owner', time_valid: Date.parse(at) < Date.parse(task.expires_at) },\n"
        "    decision: allowed ? 'authorized_once' : 'deny',\n"
        "    execution_allowed: allowed,\n"
        "    evaluate_at: at,\n"
        "    presented_authorization_id: authId,\n"
        "    presented_nonce: nonce,\n"
        "    state_before: {},\n"
        "    state_after: {},\n"
        "  };\n"
        "}\n"
        "const result = {\n"
        "  policy: { usage: 'single_use', revocation: 'deny_if_revoked', freshness: 'revocation_epoch_must_match', replay: 'consume_authorization_id_and_nonce', default: 'deny' },\n"
        "  scenarios: {\n"
        "    first_use: unsafe(),\n"
        "    replay_same_token: unsafe(),\n"
        "    revoked_before_use: unsafe(),\n"
        "    stale_revocation_epoch: unsafe(),\n"
        "    tampered_nonce: unsafe({ nonce: 'nonce-tampered-0001' }),\n"
        "    expired_token: unsafe({ evaluate_at: task.expires_at }),\n"
        "  },\n"
        "};\n"
        "process.stdout.write(JSON.stringify(result) + '\\n');\n"
    )


def compile_target(doc: dict[str, Any], target: str) -> str:
    if target == "python312":
        return compile_python(doc)
    if target == "node20":
        return compile_node(doc)
    raise BridgeReplayCompileError(f"unsupported target: {target}")
