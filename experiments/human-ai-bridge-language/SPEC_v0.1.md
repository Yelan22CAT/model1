# Bridge-0 Semantic Specification v0.1

> Status: **Experimental Draft**  
> Scope: semantic core only. No claim of production safety or completeness.

## 1. Design target

Bridge-0 defines a small, machine-parseable and human-readable semantic layer for human–AI communication.

The v0.1 target is not general computation. It is **semantic-state preservation**.

The parser/runtime should be able to distinguish:

```text
entity
claim
epistemic state
evidence
constraint
action
authority
verification
time
```

without requiring a language model to guess the intended category.

---

## 2. Canonical primitives

### 2.1 Entity — `○`

Represents a referent that can participate in state or relationships.

```text
○ user
○ model
○ document
○ tool
```

An entity declaration does not imply any property beyond existence in the current semantic frame.

### 2.2 State — `=`

Associates an entity or claim with a value.

```text
○ task
task.status = pending
```

### 2.3 Goal — `⊙`

Declares the intended target state or outcome.

```text
⊙ produce_verified_summary
```

A goal is not evidence and is not a fact about the world.

### 2.4 Fact claim — `■`

A proposition presented as factual within the current scope.

```text
■ contract.amount = 30000 CAD
```

A fact claim should carry provenance or a verification path when material.

### 2.5 Hypothesis — `△`

A proposition that may be useful for reasoning but is not asserted as fact.

```text
△ delay.cause = supplier_failure
```

### 2.6 Unknown — `?`

Represents a proposition or field whose value is missing, unresolved, or unavailable.

```text
? delivery_date
```

Round-1 rule: **one proposition carries one epistemic marker**. Avoid forms such as `■ delivery_date = ?`, because they mix a fact marker with an unknown value.

If an estimate exists, represent it as a hypothesis instead:

```text
△ delivery_date ≈ 2026-10-15
```

Unknown is not an error state.

### 2.7 Evidence — `◆`

Represents a source, observation, measurement, or artifact used to support or oppose a claim.

```text
◆ invoice.pdf
◆ sensor_reading_17
```

Evidence is not automatically true merely because it is evidence.

### 2.8 Constraint — `!`

Defines a rule that must not be silently violated.

```text
! budget <= 30000 CAD
! no_external_side_effect_without_approval
```

### 2.9 Action / transition — `→`

Represents change, execution, or transition.

```text
○ agent → generate_report
```

### 2.10 Verified — `✓`

Marks that a claim or transition has passed a defined verification condition.

```text
✓ invoice_total
```

Verification must identify what was verified and under which rule.

### 2.11 Forbidden / rejected — `×`

Marks an invalid, disallowed, or rejected transition.

```text
× deploy_without_approval
```

### 2.12 Time — `⏱`

Binds a claim, state, or action to a time context.

```text
⏱ observed_at = 2026-10-01T22:00-04:00
```

---

## 3. Mandatory epistemic rules

### R1 — No silent promotion

```text
△  ≠  ■
?  ≠  ■
```

A hypothesis or unknown may become a fact claim only through an explicit state transition.

### R2 — Unknown remains explicit

```text
? claim
+ no sufficient ◆
→ × promote_to_fact
```

The runtime must not silently fill an unknown field merely because a probable completion exists. A transition from `?` or `△` to `■` must be explicit and auditable.

### R3 — Evidence and claim are distinct objects

```text
◆ evidence
→ supports / opposes
■ or △ claim
```

Evidence may be incomplete, stale, contradictory, or misinterpreted.

### R4 — Verification is scoped

```text
✓ claim_X
```

does not imply:

```text
✓ all_related_claims
```

### R5 — Action and authority are separate

```text
can_describe(action)
≠
can_execute(action)
```

### R6 — Rendering is not semantics

The following may render differently for different users:

- Chinese labels;
- English labels;
- graphical layouts;
- accessibility text;
- machine serialization.

The underlying semantic graph must remain invariant.

---

## 4. Provisional relation vocabulary

Symbols identify primitive categories. Relations remain textual in v0.1.

Initial relations:

```text
supports
opposes
requires
allows
forbids
derived_from
observed_at
owned_by
verified_by
supersedes
```

This is intentional. v0.1 should not prematurely invent a symbol for every relation.

---

## 5. Provisional grammar sketch

This is a design sketch, not a frozen grammar.

```text
<statement> ::= <marker> <subject> [<relation> <object>]

<marker> ::= ○ | ■ | △ | ? | ◆ | ! | ✓ | × | ⊙ | ⏱

<transition> ::= <subject> → <action>

<assignment> ::= <subject> "." <field> = <value>
```

A future parser should serialize the same meaning into a canonical IR.

---

## 6. Canonical IR sketch

Example Bridge surface form:

```text
△ cause = network_failure
◆ log_17 supports △ cause
```

Possible machine representation:

```json
{
  "claims": [
    {
      "id": "cause",
      "epistemic_state": "hypothesis",
      "value": "network_failure"
    }
  ],
  "evidence": [
    {
      "id": "log_17",
      "relation": "supports",
      "target": "cause"
    }
  ]
}
```

The JSON form is an implementation representation, not the language itself.

---

## 7. Hallucination-control objective

Bridge-0 does not claim to eliminate all model error.

It targets several controllable failure modes:

```text
ambiguity
→ unintended interpretation

missing data
→ silent completion

hypothesis
→ context drift
→ false fact

recommendation
→ accidental authority

evidence mention
→ unsupported certainty
```

Desired containment behavior:

```text
missing → ?
guess → △
source → ◆
fact → ■
verification → ✓
constraint breach → ×
```

---

## 8. Compatibility principle

Bridge-0 should compile *to* existing technologies rather than replacing them immediately.

Targets may include:

```text
GitHub Actions
Python
Rust
JSON Schema
MCP
REST / RPC
agent policies
validation engines
```

---

## 9. Open questions for v0.2

1. Should confidence be a primitive or an attribute?
2. How should conflicting evidence be represented?
3. How should temporal expiry / stale evidence be encoded?
4. Should authority have its own primitive marker?
5. How should negation differ from prohibition?
6. Can spatial / 2D layout carry formal semantics without harming parser determinism?
7. What is the smallest teachable symbol set?
8. Can multiple AI models round-trip the same Bridge expression without state loss?


---

## 10. Round-1 refinement note

Ten public-safe repository patterns were encoded with the current primitives.

Round 1 found that the current alphabet is sufficient at the category level, but the grammar/IR needs:

- stable claim IDs;
- exactly one epistemic marker per proposition;
- typed relation semantics;
- explicit scope/time binding;
- guarded state transitions.

No new glyph is added by Round 1.

See:

- [ROUND1_10_CASES.md](ROUND1_10_CASES.md)
- [ROUND1_GAP_LEDGER.md](ROUND1_GAP_LEDGER.md)
- [corpus/round1_cases.json](corpus/round1_cases.json)


---

## 11. Round-2 mandatory invariants

Round 2 stress tests make the following rules mandatory for the next grammar revision.

### R7 — Attributed claim is not adopted truth

```text
■ [C2] actor asserted [C1]
≠
■ [C1]
```

A claim about another claim does not inherit the embedded claim's truth status.

### R8 — Conflicting evidence remains unresolved

```text
◆ [E1] supports [C1]
◆ [E2] opposes [C1]
```

does not authorize automatic promotion or rejection of `[C1]`.

A reconciliation rule must be explicit and auditable.

### R9 — Numerical uncertainty, confidence, and epistemic state are distinct

```text
measurement uncertainty
≠ confidence
≠ ■ / △ / ?
```

These belong in typed attributes or distributions, not in the epistemic marker itself.

### R10 — Handoff preserves provenance

A handoff must preserve at least:

```text
source_agent
target_agent
claim_or_artifact_id
scope
time
allowed_transform
```

Restatement does not reset uncertainty.

### R11 — Permission is scoped

Permission must be interpreted as a tuple:

```text
(actor, action, resource, scope, conditions, time)
```

Permission for one tuple does not imply permission for another.

### R12 — Tool failure is not a negative world-state fact

```text
tool_failed
or
no_result
≠
target_absent
```

The world state remains `?` unless supported by separate evidence.

### R13 — Superseded is not erased

A superseded source may remain historically valid while losing current authority.

### R14 — Irreversible actions require explicit guards

Guard conditions must be first-class for consequential transitions.

### R15 — Association is not causation

A descriptive association relation must not be promoted into a causal relation without additional evidence and an explicit transition.

### R16 — Semantic identity is independent of localized label

```text
semantic_id = invariant
localized_label = renderable
```

Chinese, English, or other labels may differ without changing the underlying object.

---

## 12. Provisional reference syntax after Round 2

This syntax is experimental and not frozen.

```text
■ [C1] subject.field = value
△ [C2] subject relation object
? [C3] subject.field

◆ [E1] source supports [C1]
! [G1] action requires condition
⏱ [T1] valid_from = timestamp
```

Bracketed identifiers are language-neutral references for claims, evidence, guards, goals, and time bindings.

Round 2 still does not justify any new glyph.

See:

- [ROUND2_STRESS_TESTS.md](ROUND2_STRESS_TESTS.md)
- [ROUND2_GAP_LEDGER.md](ROUND2_GAP_LEDGER.md)
- [corpus/round2_cases.json](corpus/round2_cases.json)
