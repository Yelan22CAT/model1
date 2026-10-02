# Bridge-0 Round 2 — Gap Ledger

| Gap ID | Problem | Severity | Round-2 decision |
|---|---|---:|---|
| G11 | Attributed claim can be confused with adopted truth | Critical | Add meta-claim rule and stable claim references |
| G12 | Conflicting evidence lacks explicit unresolved-conflict state | High | Represent conflict in IR; do not auto-resolve |
| G13 | Numerical uncertainty and confidence may be confused with epistemic state | High | Keep as typed attributes |
| G14 | Multi-agent handoff can lose provenance | Critical | Define handoff record with source/target/artifact/scope/time |
| G15 | Partial permission can expand accidentally | Critical | Permission tuple must include actor/action/resource/scope/condition/time |
| G16 | Tool failure can be hallucinated into "not found" | Critical | Add mandatory no-result ≠ negative-result rule |
| G17 | Superseded source can be mistaken for false or erased | High | Separate historical validity from current authority |
| G18 | Irreversible action lacks formal guard semantics | Critical | Make guards first-class in grammar/IR |
| G19 | Association may drift into causation | Critical | Add typed relation classes and causal promotion rule |
| G20 | Localized labels may become canonical semantics | High | Separate semantic IDs from localized labels |

## Cross-round synthesis

Round 1 found:

- claim IDs;
- one epistemic state per proposition;
- typed relations;
- scope/time binding;
- guarded transitions.

Round 2 confirms all five and strengthens them.

The most important new discovery is **meta-claim separation**:

```text
■ [C2] agent_A asserted [C1]
```

does not establish:

```text
■ [C1]
```

This must become a hard validator rule.

## Candidate grammar additions

These are syntax proposals, not new semantic primitives:

```text
■ [C1] subject.field = value
△ [C2] subject relation object
? [C3] subject.field

◆ [E1] source supports [C1]
! [G1] action requires condition
⏱ [T1] valid_from = timestamp
```

Identifiers in brackets are language-neutral references.

## Deferred decisions

Still deferred:

- new authority glyph;
- confidence glyph;
- contradiction glyph;
- causality glyph;
- 2D spatial syntax.

All can still be represented through typed relations or attributes.

A new glyph should be introduced only if repeated tests show that a semantic category is both:
1. irreducible to existing structures; and
2. materially clearer to humans when visually distinguished.
