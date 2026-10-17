# RFC | Bridge-0 Stage11 Witness Attestation Boundary (Experimental)

**Date:** 2026-10-17  
**Status:** Draft RFC / Candidate / Not Production Ready / Training Hold  
**Audience:** human reviewers and implementers of *advisory-only* effect verification.  
**Relation:** follows the Stage9 declared-conflict RFC as a separate independent verification concern.

## Problem and scope

A structured claim that a side effect occurred is not evidence that it actually occurred. In particular, a mutable application-local effect receipt is insufficient to warrant an externally observable success assertion. Stage11 proposes a narrow semantic interface for verifying a *separately witnessed* effect **without giving an agent any capability to execute, authorize, or claim success**.

This document specifies a candidate interface and its limitations. It is not an implementation, a production cryptographic protocol, or a proof of trust-root separation.

## Candidate interfaces

The witness assessment contract describes:

| Field | Meaning |
| --- | --- |
| `operation_id` | Stable identity of the attempted, explicitly authorized operation |
| `request_digest` | Digest of the exact candidate request/scope |
| `effect_claim_digest` | Digest of the observed effect claim (not effect proof) |
| `witness_identity` and `attestation_epoch` | Identity and revocation epoch in an independently controlled trust domain |
| `witness_sequence` and `previous_checkpoint` | Monotonic ordering, history binding, and rollback review |
| `consumption_binding` | Persistent, integrity-bound record of whether a witness has already been consumed |
| `validity_interval` | Time bounds under an independently trusted clock |
| `verification_evidence_ref` | Opaque reference to externally verifiable effect evidence, not untrusted message text |

Candidate outcomes:

- `HOLD_MISSING_OR_UNTRUSTED_WITNESS`
- `HOLD_SCOPE_OR_DIGEST_MISMATCH`
- `HOLD_REVOKED_OR_EXPIRED`
- `HOLD_REPLAY_OR_ROLLBACK`
- `HOLD_EFFECT_NOT_INDEPENDENTLY_PROVEN`
- `SIMULATED_WITNESS_MATCH_ONLY` (local demonstration; explicitly **not** a success claim)

All candidate Stage11 assessments maintain `can_execute=false` and `can_claim_success=false`. Nothing in this RFC elevates a simulation label to `VERIFIED_EFFECT` or creates permission to act.

## Gates for any future trustworthy implementation

1. **Independently authorized attestation:** a signer must not blindly sign caller-supplied effect claims; independently validate the granted operation and the actual observable effect.
2. **Independent trust domain:** protect the signer, journal, key custody, revocations, and trusted clock from the execution actor's capabilities.
3. **Rollback-resistant history:** independently maintained, monotonic, append-only high-water, verified restore history, and durable consumption/replay state.
4. **Crash and recovery:** model partial writes, reconciliation, revocation epochs, drift, and human authorization for recovery without replaying durable side effects.
5. **Conformance and adversarial review:** preserve negative test cases; passing an intentionally insecure assertion is a passed *test*, not a passed *security property*.
6. **Human Final:** only independently verified real evidence and a fresh authorized policy decision can change production gates.

## Explicit non-claims

- No verified remote model A/B, independent witness infrastructure, real effect attestation, or production release.
- No claim that the previously reported mutable receipt flaw is repaired within the original Stage3 broker.
- No promotion of Bridge-0 remote verified `v0.147` or local synthetic `v0.272` high-water.
- No change to existing Frozen / Sealed / Deprecated / Training Hold or official grammar/IR.

**Private implementation and negative-case reproduction artifacts are deliberately excluded from this public RFC.**
