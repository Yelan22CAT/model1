# 42 — Horizontal Decision Core + Vertical Expertise Packs

**Status:** User-authorized method-level Full-Push / Not Frozen (2026-11-28). Public-safe architecture method only; not a claim of foundation-weight training, production readiness, universal domain expertise, or automatic authority.

## Purpose

Build a general-purpose decision chassis that does not need to be the strongest expert in every domain. The horizontal core supplies routing, constraint handling, conflict detection, verification planning and authority boundaries. Domain depth is attached through modular vertical expertise packs.

**Core distinction:**

`Horizontal = how to judge across domains`  
`Vertical = what a domain knows, where it fails, and how to verify it`

## Layered architecture

### Layer 0 — General/Foundation capability

General language, reasoning, representation and tool-use substrate.

### Layer 1 — Horizontal Decision Core (HDC)

The core should:

- decompose the task;
- detect decision-critical unknowns and hidden constraints;
- select the minimum sufficient set of vertical modules;
- normalize outputs into a shared decision representation;
- preserve provenance and uncertainty;
- detect incompatible assumptions or constraints;
- synthesize feasible intersections across domains;
- define verification and stop conditions;
- route consequential continuation through authorization and Human Final.

The core does **not** need to pretend to be the deepest domain expert.

### Layer 2 — Vertical Expertise Packs (VEPs)

A vertical pack does not have to be a neural model. It may include:

- domain ontology and state definitions;
- decision rules and exceptions;
- hidden constraints;
- failure cases and anti-patterns;
- case libraries;
- SOPs and playbooks;
- thresholds and tolerances;
- tools and evaluators;
- provenance and evidence grades;
- uncertainty and applicability boundaries;
- version / validity windows;
- escalation conditions.

Expert experience is treated as scoped evidence, not universal truth.

### Layer 3 — Reality & Action

External data, deterministic checks, tools, real-world execution, safety/authorization gates, independent verification and Human Final.

## Vertical Module Interface

Each pack should expose a stable contract such as:

```text
MODULE_ID
DOMAIN
VERSION
OWNER_OR_SOURCE
SCOPE
OUT_OF_SCOPE
INPUT_SCHEMA
DOMAIN_STATE
CONSTRAINTS
KNOWN_FAILURES
DECISION_RULES
EXCEPTIONS
OUTPUT_SCHEMA
EVIDENCE
PROVENANCE
UNCERTAINTY
CONFIDENCE
VERIFICATION_METHOD
STOP_CONDITIONS
ESCALATION_CONDITIONS
```

## Shared decision representation

Cross-domain outputs should be translated into a common skeleton:

```text
OBJECTIVE
STATE
OBSERVATIONS
CONSTRAINTS
UNKNOWN
HYPOTHESES
CANDIDATE_ACTIONS
EXPECTED_EFFECT
FAILURE_MODES
EVIDENCE
CONFIDENCE
VERIFICATION
STOP_CONDITION
```

This common structure enables modules with different internal implementations to participate in one decision process.

## Multi-module synthesis

When a problem spans multiple domains:

```text
task
-> minimum sufficient VEP set
-> independent domain outputs
-> shared representation
-> conflict / assumption check
-> feasible constraint intersection
-> candidate plan
-> verification / risk / authority gate
-> Human Final
```

Do not average conflicting experts by default. First test whether the disagreement comes from different scope, context, assumptions, time period or objective.

## Minimum sufficient modules

More modules do not automatically produce better judgment.

**Rule:** `Task Need -> Minimum Sufficient VEP Set -> Synthesis`.

Unnecessary modules can add noise, latency and irrelevant conflicts.

## Expert-experience compression

High-value expertise is often conditional rather than encyclopedic:

- normally do A;
- unless B and C are both present;
- if D appears, inspect E before F;
- if F fails, do not repeat it until G is ruled out.

Therefore experience compression should prioritize:

**state + constraint + exception + failure + diagnostic order + verification**

rather than accumulating prose alone.

## Lifecycle and evidence

Each VEP should support:

- provenance;
- evidence grade;
- applicability scope;
- versioning;
- validity window;
- conflict history;
- rollback / deprecation;
- reality-verification updates.

A pack's inclusion in the architecture does not promote all of its internal claims to Verified.

## Authority boundary

A VEP produces a **candidate domain judgment**, not unconditional execution authority.

Default path:

```text
VEP recommendation
-> HDC constraint/conflict gate
-> verification
-> authorized system / accountable human
-> observed effect
```

High-risk domains must not bypass independent authorization merely because a module is confident.

## Relationship to JEPA

HDC+VEP is not equivalent to JEPA. JEPA-like representation or world-prediction methods may be used inside one layer, but this method is a modular decision-system architecture centered on routing, constraints, expert composition, verification and authority.

## Non-claims

- A larger number of packs does not imply better performance.
- Human experts can be biased, local, stale or wrong.
- Module compatibility must be demonstrated.
- Cross-domain synthesis must preserve provenance and uncertainty.
- No foundation-model weight update is implied.
- No production deployment is implied.
- No module automatically inherits Full-Push or Verified status.
- Human Final remains required for consequential action.

## Design target

The target is not "one model that knows everything."

The target is:

> A generalist decision core that can correctly attach, combine, challenge, verify, update and retire specialized expertise modules.
