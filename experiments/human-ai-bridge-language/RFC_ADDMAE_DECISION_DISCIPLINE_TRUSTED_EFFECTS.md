# RFC — ADD-MAE Decision Discipline & Trustworthy Effect Recovery

**Status:** Experimental / Candidate / Public-safe / **Not Production Ready**  
**Date:** 2026-10-08  
**Project:** Human–AI Bridge (Bridge-0) — public interface discussion; not a canonical grammar amendment.

## Motivation

An agent can choose an apparently reasonable action yet still lack current authorization, attempt redundant external actions, or mistake a database row for a trustworthy execution receipt. Agent quality therefore includes *when not to act* and *how to prove an external effect*.

## Proposal: composable decision checks

For a proposed action, distinguish three separate claims:

- **CanAct:** the chosen runtime has the required capability.
- **MayAct:** a current scoped authority permits the exact operation and effect surface.
- **ShouldAct:** the action is necessary and proportionate under the current goal, risk and evidence.

These do not imply each other. An action candidate must also preserve plan identity, resource/state version, current policy/authorization epoch, and relevant provenance. This is a **candidate** decision interface, not a grant of execution power.

### Recovery states are not interchangeable

- An invalid tool argument calls for contract correction, not an identical retry loop.
- A transient error may justify a bounded, policy-authorized retry only when replay is safe.
- A revoked permission blocks the affected operation even if a previous plan allowed it.
- An unknown external effect calls for **RECONCILE** against independent trustworthy evidence, not blind replay.
- An already confirmed external effect must not be repeated merely because another diagnostic reports an error.
- An unsuccessful mandatory step cannot be silently dropped and reported as completed.
- Safe **ABSTAIN**, **ASK**, **ABORT** and **ESCALATE** are distinct from success and must be auditable. Unwarranted abstention is also an error.

### Minimal sufficient action

Evaluation should combine completion correctness and risk with unneeded tool calls, duplicate side effects, unnecessary complexity, and false abstention. Define denominators and severity before using any aggregate score. No single blanket retry count is normative.

## Stage 3 local simulation: scoped observations

A local prototype coupled a proposal/decision interface to a separate mock execution broker and two SQLite databases, one for authorization/intents and one for a mock receiver's effect records.

Observed *within a single-host synthetic harness*:

| Evidence | Local result | Interpretation limit |
| --- | --- | --- |
| Unit/integration | 41/41 pass | Author-generated assertions and scenarios |
| Seeded scenarios | 1,200 / 3,083 assertions; zero observed failures | Not representative of all runtime states |
| Child-process crash after mock effect, before journal receipt | Recovered by reconciliation without duplicate effect | Local mock receiver; not distributed exactly-once |
| 72 concurrent duplicate callers | One mock effect row | Local uniqueness and serialization only |
| 25 revoke-vs-write races | Serialized outcomes | Single-host locks, not network trust |
| Pinned earlier decision regression | No observed drift in tested inputs | Not independent model-generation A/B |

**Blocking red-team finding:** a privileged change to the unsigned mock receiver database could inject a fabricated, matching receipt; reconciliation **accepted the forgery** (`forgery_accepted: true`). No authenticated witness or independently protected evidence root was present. This is a **known trust-boundary failure**, not a passed security gate.

## Required next gates

1. Separate, independently governed witness identity and authenticated receipt semantics; adversarial tests for forged, missing, revoked, stale and replayed attestations.
2. Versioned compatibility/migration review for any candidate ADD-MAE surface and canonical Bridge IR; unknown or mixed generations must fail closed.
3. Multi-host crash/partition experiments and real effect-broker assumptions, with explicit limits on exactly-once claims.
4. External-generated corpus and human comprehension evidence before treating the surface as an accepted shared language.
5. Human governance review before merge or any deployment.

## Non-claims and publication boundary

This RFC does **not** claim production safety, a formal Bridge-0 version advancement, trusted authorization, authenticated receipts, real external effects, independent human comprehension, or GPT-5.6/GPT-6 model-generation equivalence. The protected/private implementation, full tests, hidden calibration and raw source materials are not part of this publication. **Executable capability is not execution authority.**

Related documents: [Bridge-0 introduction](README.md), [state-bound planning](RFC_STATE_BOUND_PLANNING_REPLAN.md), [surface-language principles](SURFACE_LANGUAGE_PRINCIPLES.md), [RC candidate specification](SPEC_v1.0-rc1.md).
