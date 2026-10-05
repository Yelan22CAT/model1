# Bridge-0 Surface Language Design Principles

> Status: Experimental / v0.x / Not Production Ready

## Purpose

The Bridge surface language is designed for a three-party contract:

1. **Human-readable** — a competent human should be able to inspect the surface form and recover the intended meaning without reconstructing backend implementation details.
2. **AI-generatable** — an AI system should be able to produce valid Bridge expressions reliably from natural-language intent without depending on hidden prompt conventions.
3. **Machine-verifiable** — deterministic tooling should be able to parse, type-check, validate, and reject malformed or semantically incomplete expressions.

A surface feature is not mature merely because one of these properties holds.

```text
Human-readable
× AI-generatable
× Machine-verifiable
= viable Bridge surface
```

## Design rule

**Expose what affects correctness; hide what only affects implementation.**

Correctness-affecting state belongs in explicit Bridge semantics when it can materially change interpretation, authority, validity, safety, or externally observable effect.

Examples include:

- epistemic state;
- authority and scope;
- evidence and provenance;
- time validity;
- dependency identity;
- reversibility and side-effect class;
- target capability requirements;
- execution-state identity when it affects semantic validity.

Backend-only implementation detail should remain below the surface unless it changes one of those properties.

Examples normally kept below the Bridge surface:

- target-language syntax;
- SDK boilerplate;
- transport formatting;
- concrete HTTP headers;
- device-specific instruction syntax;
- incidental filesystem or process details.

## Surface / IR separation

The human-facing surface is not the canonical truth object.

```text
Human / AI surface
        ↓ parse
Canonical Bridge IR
        ↓ validate
Semantic obligations
        ↓ lower
Backend-specific execution
```

The surface may evolve for readability or generation quality without silently changing canonical semantics.

## No from-scratch rewrite requirement

This principle applies as a **continuous compatibility constraint**, not as an instruction to discard the existing language.

Existing constructs are retained when they satisfy the triad. Constructs that fail should be revised locally, migrated explicitly, or deprecated with compatibility evidence.

```text
new principle
!= rewrite everything

new principle
= audit existing surface
+ preserve valid constructs
+ revise failing constructs
+ require future constructs to satisfy the same gate
```

## Verification boundary

Automated tests can directly measure:

- parse success/failure;
- canonical IR equality;
- ambiguity under machine parsing;
- deterministic validation;
- round-trip preservation;
- generation conformance under a declared model/test harness;
- rejection of unsupported syntax.

Automated tests **cannot by themselves prove human comprehensibility**.

Human readability therefore remains a separate evidence class requiring human review or user-study evidence when a release makes a human-comprehension claim.

```text
Machine parse success
!= Human understanding

AI generation success
!= Human readability

Human readability claim
→ human evidence required
```

## Acceptance gate for new surface syntax

A new or changed surface construct should not become canonical unless:

1. it maps to one unambiguous canonical semantic structure;
2. invalid or incomplete forms fail closed;
3. its semantics survive render → parse → canonicalize round trips;
4. at least one declared AI-generation test can produce it reliably;
5. a human-facing explanation exists;
6. no backend-specific detail leaks into the semantic layer without a correctness reason;
7. compatibility or migration behavior is explicit.

## Relation to lower layers

This design principle complements, rather than replaces:

- capability contracts;
- semantic lowering;
- runtime identity binding;
- effect verification;
- recovery and replay controls.

The surface contract governs how intent and semantic state are expressed. Lower layers govern whether that meaning survives execution.
