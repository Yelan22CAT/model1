# Bridge-0 Specification — v1.0-rc1 Candidate

> **Release Candidate / Experimental / Not Production Ready**

## Scope

Bridge-0 is a shared semantic and assurance layer for human–AI workflows. It does not replace execution languages, operating systems, cryptographic libraries, organizational governance, or human judgment.


## Surface-language contract

The Bridge surface language MUST be designed for three simultaneous properties:

- human readability;
- AI generatability;
- deterministic machine verifiability.

A surface construct is not mature solely because it parses or executes. Correctness-affecting semantics MUST be explicit at the Bridge layer; implementation-only detail SHOULD remain in lowering/backend layers unless it changes semantic validity.

This rule is applied incrementally: compatible existing constructs are retained, and incompatible constructs require explicit revision, migration, or deprecation rather than an unconditional from-scratch rewrite.

Automated verification MAY establish machine properties and declared AI-generation behavior, but MUST NOT be described as proof of human comprehension. Human-comprehension claims require separate human evidence.

## Normative rule

**Each layer proves only the claim it owns.**

No successful gate may silently substitute for a different claim domain.

## End-to-end validity

A candidate executable decision requires, as applicable:

1. strict transport and canonical semantics;
2. current integrity/authenticity/trust state;
3. typed evidence with well-founded provenance;
4. explicit truth/conflict state;
5. qualified evidence independence where required;
6. calibrated confidence only where quantitative policy consumes it;
7. trusted risk/decision policy;
8. current scoped human review where required;
9. current authorization/delegation/quorum state;
10. one coherent Assurance Context and exact dependency graph;
11. valid ordered plan and current state binding;
12. semantically eligible attested runtime;
13. declared and mediated effect surface with behaviorally conformant broker where required;
14. replay/freshness/atomic-commit checks;
15. durable effect/recovery/restore state;
16. no active terminal trust state.

## Assurance Context

Decision-critical artifacts bind one coherent subject/resource, operation, state/epoch/generation vector, or carry an explicit trusted context-transition proof.

Compatibility is non-transitive by default. Transition chains are bounded by a cumulative Compatibility Budget anchored to an original trusted root.

Budget reset requires a separately authorized Fresh Root Revalidation event.

## Truth state

Bridge preserves:
- `SUPPORTED`
- `UNSUPPORTED / UNVERIFIABLE`
- `REFUTED`
- `CONFLICT`

`CONFLICT` is not silently coerced into support or refutation.

## Human review

Human approval is typed, scoped, current, and bound to the actual review material. A signature/approval event does not prove comprehension, attention, voluntariness, or sound judgment.

## Planning and recovery

Plans are first-class ordered semantic objects. Partial execution survives restart. Retry, Resume, Replan, Compensate, Rollback, and Abort are distinct operations.

## Effect surface

Authorization covers declared effects, not arbitrary implementation side effects. High-assurance execution may require deny-by-default complete mediation within a declared runtime/TCB boundary. Claims of completeness remain bounded to that mediation surface.

## Trust recovery

Normal trust-root loss may be recoverable through an independently provisioned emergency recovery authority. Emergency recovery authority is distinct from normal execution authority.

If all independent trust anchors are unavailable, Bridge enters:

`EXTERNAL_TRUST_BOOTSTRAP_REQUIRED`

In that state automatic root creation and normal execution are forbidden. External bootstrap creates a new trust era; it must not be described as uninterrupted trust continuity.

## Compatibility

Default behavior:
- mixed unsupported schema/spec generations fail closed;
- cross-tenant/cluster/environment artifacts do not compose implicitly;
- context compatibility is explicit and scoped;
- transition proofs are non-transitive by default;
- same display label does not imply same resource or assurance identity.

## Verification boundary

Finite-domain exhaustive tests, randomized adversarial tests, cross-runtime equality, formal proofs, attestation, and reproducible builds are scoped evidence. None is a universal security proof beyond its declared domain.

## Maturity

This RC candidate follows five consecutive orthogonal convergence passes with no new structural revision, a cumulative assurance regression, exact Python/Node/Ruby RC-corpus reproduction, and a machine-readable freeze audit.

It remains **Experimental / Not Production Ready** until implementation, deployment, governance, and external review criteria are separately satisfied.