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

```text
31 tests
31 passed
0 failed
```

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
