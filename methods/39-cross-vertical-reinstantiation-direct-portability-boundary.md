# 39 — Cross-Vertical Reinstantiation & Direct-Portability Boundary
**Status:** User-authorized method-level Full-Push / Not Frozen (2026-11-25). Public-safe method. It does **not** claim a universal cross-domain executor, automatic industrial expertise, production deployment, or foundation-model weight update.

## Boundary statement

A vertical execution module should **not** be assumed to port directly into another vertical domain.

`Vertical_A != Vertical_B`

`Shared abstraction != shared execution semantics`

`Judgment transfer != execution transfer`

The transferable object is usually the **rebuild method**, not the finished vertical module.

This is an operational AI boundary: a system may recognize structural similarity across domains while still lacking the target domain's local state variables, tools, tolerances, failure modes and acceptance criteria. Cross-domain reasoning can therefore be useful before cross-domain execution is safe.

## Two questions that must not be conflated

### 1. Direct vertical portability
Can a domain-A execution module be reused in domain B without reconstructing the target domain?

**Default: reject.**

A vertical module contains more than code shape, vocabulary or high-level intent. It embeds a local coordinate system:

- **STATE** — what variables describe reality;
- **ACTION** — what actions are actually possible;
- **CONSTRAINT** — safety, authorization, geometry, timing, capacity, regulation;
- **TOOL** — fixtures, instruments, APIs, machines, operators;
- **TOLERANCE** — acceptable variation and measurement error;
- **FAILURE** — how things fail and how failure appears;
- **FEEDBACK** — what signals reveal success, drift or damage;
- **ACCEPTANCE** — what counts as a qualified outcome.

A similar problem shape does not establish equivalent execution semantics.

### 2. Meta-transfer / reinstantiation
Can a horizontal system reuse decomposition, diagnostics and verification logic to construct a new domain-B adapter faster than rebuilding blindly from zero?

**Candidate: yes, but only through target-domain reinstantiation and reality verification.**

Canonical rule:

`Cross-domain success = reusable meta-structure + target-domain reinstantiation + reality verification`

## Reinstantiation protocol

When a domain jump is detected, enter `REINSTANTIATE` rather than immediately issuing confident execution steps.

### A. Detect the domain jump
Trigger when critical state variables, tools, material/physical constraints, failure modes or acceptance criteria are unknown or only inferred by analogy.

### B. Rebuild the target coordinate system
Explicitly reconstruct:

`STATE / ACTION / CONSTRAINT / TOOL / TOLERANCE / FAILURE / FEEDBACK / ACCEPTANCE`

Critical unknowns remain `UNKNOWN`; do not silently inherit them from the source domain.

### C. Retrieve target-domain anchors
Prefer authoritative manufacturer instructions, standards/specifications, measured drawings, qualified expert input, prior test data and instrumented observations.

Analogy may generate hypotheses. It does not certify execution.

### D. Compile to reusable primitives
Generic primitives may transfer:

`ALIGN -> CONSTRAIN -> GUIDE -> ACT -> COMMIT/SEAT -> MEASURE -> VERIFY -> STOP/REWORK`

Their parameters, tools, thresholds and pass/fail criteria are target-domain-specific.

### E. Generate bounded candidate adapters
Each candidate should identify:
- required inputs;
- tools/interfaces;
- expected failure modes;
- observable success signals;
- stop conditions;
- falsifying evidence.

### F. Build a Reality Harness
The target domain needs its own equivalent of compiler/tests/logs.

Examples:
- physical: gauges, force/displacement traces, leakage/retention tests, inspection;
- software: compiler, tests, logs, sandbox, rollback;
- business/process: receipts, reconciliation, approvals, exception outcomes.

### G. Promote only after target-domain evidence
`Candidate -> controlled trial -> qualified/independent verification -> repeatable outcome -> reusable vertical adapter`

A successful history in the source domain does not skip this chain.

## Negative-transfer gate

Cross-domain reuse can make performance worse.

Warning signs:
- source heuristics increase target failures;
- similar words hide different semantics;
- assumed tools do not exist in the new environment;
- familiar thresholds lack target-domain provenance;
- model confidence remains high while observed outcomes worsen.

On warning:

`STOP -> mark analogy non-binding -> rebuild local coordinates -> retrieve decisive evidence`

A system should be rewarded for detecting non-transferability, not for preserving a universal-expert narrative.

## What may transfer horizontally

Useful cross-domain priors include:
1. problem decomposition;
2. hidden-constraint discovery;
3. discriminating-question selection;
4. evidence grading;
5. failure-mode search;
6. permission/authority separation;
7. rollback and safe-stop design;
8. observability requirements;
9. acceptance-test structure;
10. Reality Gate discipline.

These can reduce search cost. They do not establish target-domain correctness.

## AI boundary clarified

The objective is **not zero-shot omniscience** and not “one vertical module jumps into another.”

The objective is:

> make the *rebuild process* reusable, faster and more explicit.

A capable horizontal system should know:
- what it can carry across;
- what must be relearned;
- which evidence is missing;
- when to stop;
- how to construct a temporary local expert layer;
- when that layer has earned promotion through reality evidence.

This preserves domain experts and target-domain evidence as necessary inputs where consequence requires them.

## Evidence boundary

Agreement from experienced practitioners can be useful corroboration, but practitioner agreement alone is not independent proof that the method works across domains. Universal cross-domain competence requires target-domain experiments and repeatable evidence.

## Integration

`Horizontal–Vertical Complementarity -> LCR-G / MISA-G -> CVR-G -> ANASG -> PERV-G / Reality Gate -> Human Final`

Cross-Model Structural Synthesis supplies candidate abstractions; CVR-G prevents those abstractions from being mistaken for executable target-domain knowledge.

## Non-negotiable boundaries

- Direct vertical portability: **DEFAULT REJECT**.
- Meta-transfer: **allowed only as a reinstantiation candidate**.
- No claim that every domain can be learned cheaply, rapidly or without experts.
- No self-authored synthetic test can establish industrial cross-domain competence by itself.
- Existing Bridge Stage3/Stage11/HER blockers, Training Hold and Production FAIL remain unchanged.
- No production runtime, formal Bridge grammar, external actuation, or foundation-model weight change.

**End state:** `METHOD FULL-PUSH / DIRECT PORTABILITY DEFAULT REJECT / META-TRANSFER VIA TARGET-DOMAIN REINSTANTIATION / REALITY VERIFICATION REQUIRED`.
