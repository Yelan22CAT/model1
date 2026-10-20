# Bridge-0 Assurance Architecture — v0.50 Consolidation

> **Experimental / v0.x / Not Production Ready**
>
> Public-safe consolidation of adversarial verification findings from v0.20–v0.50.

## Purpose

Bridge-0 began as a shared semantic layer for humans and AI systems. Later verification showed that semantic clarity alone is insufficient for consequential action. A usable bridge must also preserve identity, scope, currentness, provenance, authority, review state, execution context, and recovery history.

Public assurance stack:

```text
transport
→ canonical semantics
→ integrity / authenticity
→ trust anchor
→ authorization
→ evidence / provenance
→ confidence / calibration
→ decision / risk policy
→ human review
→ plan composition
→ runtime eligibility
→ execution / recovery
→ durable restore state
```

## Normative principle

> **Each layer proves only the claim it owns.**

```text
signature valid != key currently trusted
runtime attested != behavior correct
behavior correct != action authorized
probability high != permission
human approved != informed understanding
all steps locally safe != plan globally safe
all layers individually valid != end-to-end valid
```

## Claim states

Bridge-0 preserves at least:

- `SUPPORTED`
- `UNSUPPORTED / UNVERIFIABLE`
- `REFUTED`
- `CONFLICT`

`CONFLICT` is not silently coerced into support or refutation.

## Typed evidence and inference

Authentic evidence is not interchangeable across claim domains. Every assurance artifact is scoped by evidence/claim type, subject, issuer/authority, context, schema/profile, freshness where relevant, and exact upstream dependency identity.

Cross-layer inference is allowed only by trusted explicit rules. Circular support cannot manufacture truth without an independently trusted root.

## Dynamic truth maintenance

A derived claim is not permanent. Evidence, rules, policy, time, revocation, or context changes may invalidate prior support. Losing one proof path does not refute a claim if another valid rooted path remains.

```text
Past PASS != Current PASS
Revoked support != Refuted claim
Proof path stale != Claim necessarily false
```

## Evidence independence

Raw artifact count, signer count, organization labels, or copied reports do not automatically establish independent evidence. Independence is evaluated against a trusted provenance threat model, potentially including control root, observation/data root, measurement system, calibration/model lineage, and upstream-source lineage.

```text
Distinct signer ID != Independent source
No known shared dependency != Proven independence
Independent sources != Correct sources
```

## Confidence and decision policy

Quantitative confidence is separate from claim state and requires a calibration contract. Decision thresholds are action- and consequence-specific. Risk/loss policy is trusted policy state, not request-controlled metadata.

```text
Confidence != Truth state
High probability != Fact
High probability != Permission
Probability != Action
```

## Human review

Human approval is a scoped, current event. It binds the exact action, resource, material parameters/state, decision context, review material shown, reviewer identity/role/current eligibility, review policy, and validity context.

```text
Signed approval != Informed understanding
Approval of X != Approval of materially changed X
Human review != Authorization
Human review != Execution
```

## Plan composition and recovery

Plans are first-class ordered semantic objects. Per-step validity is necessary but insufficient. Plan validation includes cumulative risk/budget, ordering, state evolution, capability accumulation, irreversibility, and plan-level review.

Partial-plan state survives restart. Retry, resume, replan, compensate, rollback, and abort remain distinct.

```text
Local safe != Globally safe
Individual step approvals != Plan approval
Completed flag != Durable effect evidence
Compensation != Rollback
Process restart != Plan state reset
```

## Long-lived restore state

Disaster recovery is security-sensitive state reconstruction. A valid backup can still be stale, incomplete, forked, or composed from incompatible stores.

Durable security state includes policy/auth epochs, replay ledger, revocations, effect/idempotency receipts, plan/recovery state, approval lifecycle state, and trusted high-water anchors.

```text
Backup authentic != Fresh enough to restore
Backup integrity != Backup completeness
Same epoch != Same recovered history
```

## Assurance Context

v0.50 introduces a first-class **Assurance Context / Assurance Transaction identity**.

End-to-end artifacts must refer to one coherent reality or carry an explicit trusted transition proof. A context may bind subject/resource, operation ID, state version, authorization/policy/evidence/review/plan/runtime/replay epochs, restore generation, and schema/semantic-profile identity.

Exact dependency edges remain required:

```text
Evidence A
→ Confidence(A)
→ Decision(A)
→ Review(Decision A)
→ Authorization(Decision A, Review A)
→ Plan(Authorization A)
→ Execution(Plan A)
```

```text
All layers individually valid != End-to-end valid
All green checks != Same reality
```

## Verification boundary

The v0.20–v0.50 campaign covers canonical semantics, trust separation, authorization/state/TOCTOU, crash recovery, trusted time, transparency, delegation, quorum, policy composition, receipts, selective disclosure, schema evolution, mixed-version fleets, runtime/build provenance, typed assurance composition, circular-proof rejection, truth maintenance, conflict states, source independence, calibrated confidence, risk policy, human review, multi-step planning, recovery, disaster restore, and full-stack compositional regression.

These are results for tested models and corpora, not a proof that all implementations or deployments are secure.

## Public / private boundary

Public material may expose interface-level semantics, invariants, public-safe examples, high-level test outcomes, failure classes, and reproducibility guidance. It does not need to expose private thresholds, confidential cases, unrestricted execution logic, hidden runtime/control-plane internals, sensitive attack corpora, proprietary benchmarks, or private calibration chains.

## Maturity

```text
Bridge-0
Experimental
v0.x
Not Production Ready
Post-v0.50 convergence testing in progress
```

A future v1.0 release candidate should require core-layer coverage plus several orthogonal adversarial test families producing no new structural specification revisions, followed by full regression, cross-runtime/cross-version verification, and documentation freeze.