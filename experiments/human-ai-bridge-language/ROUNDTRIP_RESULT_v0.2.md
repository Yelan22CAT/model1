# Bridge-0 v0.2 — Semantic Round-Trip Test Result

> Experimental branch result. This is not a production-safety claim.

## Test objective

Check:

```text
Bridge
→ Parser
→ Canonical IR
→ Renderer
→ Bridge
→ Parser
→ Canonical IR
```

for semantic-state preservation.

Also check that malformed or ambiguous syntax is rejected rather than guessed.

## Verified CI result

The first round-trip-enabled CI run completed successfully.

### Passed

- parser syntax and unit tests;
- validator tests;
- semantic round-trip tests;
- negative / malformed-input tests;
- end-to-end parse + validate demo.

### Test count

Initial round-trip run:

```text
31 tests
31 passed
0 failed
```

Extended semantic-mutation run:

```text
39 tests
39 passed
0 failed
```

The extended suite additionally checks:
- hypothesis → fact mutation remains detectable;
- association → causation mutation remains detectable;
- evidence-target mutation remains detectable;
- missing references are rejected;
- localized labels do not change canonical surface semantics;
- conflict state survives round-trip;
- meta-claims do not promote embedded claims;
- a deterministic 100-claim batch survives parse → render → parse without semantic change.

The tested invariants include:

- fact / hypothesis / unknown preservation;
- meta-claim preservation;
- conflicting evidence preservation;
- action / guard / verification / time round-trip;
- numeric value + unit preservation;
- tool-failure vs world-unknown separation;
- association vs causation distinction;
- malformed syntax rejection.

## What this result means

It supports a narrow statement:

> Within the current restricted v0.2 grammar and tested corpus, deterministic representation changes did not alter the tested semantic states.

It does NOT establish:

- complete language correctness;
- hallucination elimination;
- cross-model equivalence;
- broad human readability;
- safe production execution;
- complete permission semantics.

## Next test layer

Add semantic mutation tests:

```text
hypothesis → fact
association → causation
evidence target A → B
localized label change
conflict preservation
meta-claim preservation
100-claim deterministic batch
```

The purpose is to verify that meaning-changing mutations remain visible while presentation-only changes do not.


## Current interpretation

The current evidence supports only a bounded claim:

> The restricted v0.2 implementation preserves the tested semantic distinctions under deterministic parse/render cycles and detects the tested meaning-changing mutations.

This is stronger than the initial syntax-only result, but it is still not evidence of complete language correctness or general hallucination elimination.

Next test layer should target structured scope, permissions, handoff records, and state-transition semantics.
