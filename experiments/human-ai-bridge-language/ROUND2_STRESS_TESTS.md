# Bridge-0 Round 2 — Stress Tests

> Status: Experimental v0.1  
> Goal: stress the language with cases that are harder than Round 1.  
> Rule: prefer grammar/IR refinement over adding new glyphs.

## Round-2 stress dimensions

This round tests ten harder structures:

1. nested / attributed claims;
2. conflicting evidence;
3. numerical uncertainty;
4. multi-agent handoff;
5. partial permissions;
6. tool failure and missing result;
7. source-version replacement;
8. reversible vs irreversible action;
9. causal claim vs association;
10. cross-language semantic invariance.

---

## Case 01 — Attributed claim is not adopted truth

### Situation

Agent-A says a component is safe. Agent-B reports what Agent-A said. The system must preserve the distinction between:

- Agent-A asserted X;
- X is actually verified.

### Bridge-0 encoding

```text
○ agent_A
○ agent_B
○ component

△ [C1] component.safe = true
■ [C2] agent_A.asserted = [C1]

→ agent_A handoff [C1] to agent_B
■ [C3] agent_B.received = [C1]

? [C4] component.safe_verified
```

### Required invariant

```text
■ agent_A.asserted [C1]
≠
■ [C1]
```

Reporting that someone made a claim must never promote the embedded claim to fact.

### Gap found

A formal distinction is needed between:

- **claim content**;
- **claim about another claim**;
- **adoption of a claim as current truth**.

No new glyph is required. Stable claim IDs are mandatory.

---

## Case 02 — Conflicting evidence without forced resolution

### Situation

Two current sources disagree about the same claim.

### Bridge-0 encoding

```text
○ sensor_A
○ sensor_B

△ [C1] pressure = 125 kPa

◆ [E1] sensor_A_reading supports [C1]
◆ [E2] sensor_B_reading opposes [C1]

■ [C2] E1.current = true
■ [C3] E2.current = true

? [C4] pressure_resolved
```

### Required invariant

```text
support + opposition
≠ automatic majority truth
```

The system must preserve contradiction until an explicit reconciliation rule resolves it.

### Gap found

Need a typed **conflict state** in IR, but not necessarily a new surface symbol.

---

## Case 03 — Numerical uncertainty is not epistemic uncertainty

### Situation

A measurement is known to be approximately 10.0 ± 0.3, while a separate forecast is only a hypothesis.

### Bridge-0 encoding

```text
■ [C1] measured_length.value = 10.0 mm
■ [C2] measured_length.uncertainty = ±0.3 mm

△ [C3] future_length.value = 10.5 mm
■ [C4] C3.confidence = 0.72
```

### Required invariant

Measurement uncertainty, model confidence, and epistemic state are different dimensions.

```text
numerical uncertainty
≠ hypothesis
≠ confidence
```

### Gap found

Confidence must remain an attribute, not a replacement for `■ / △ / ?`.

No new glyph added.

---

## Case 04 — Multi-agent handoff with provenance preservation

### Situation

A supervisor routes a task to an executor, an analyst interprets output, a judge scores it, and a validator checks it.

### Bridge-0 encoding

```text
○ supervisor
○ executor
○ analyst
○ judge
○ validator

⊙ [G1] produce_validated_result

→ supervisor handoff [G1] to executor
→ executor produce [C1]
→ analyst derive [C2] from [C1]
→ judge assess [C2]
→ validator verify [C2]

◆ [E1] executor_output supports [C1]
◆ [E2] analyst_trace supports [C2]

? [C3] final_authority
! final_release requires human_owner.authorization
```

### Required invariant

Each transformation must preserve provenance. Later agents cannot make earlier uncertainty disappear merely by restating it.

### Gap found

Handoff needs a canonical record:

```text
source_agent
target_agent
artifact/claim
scope
timestamp
allowed_transform
```

No new glyph required.

---

## Case 05 — Partial permission is not general authority

### Situation

An agent may read two paths and write one draft path, but may not merge, delete, or access secrets.

### Bridge-0 encoding

```text
○ agent

■ [C1] agent.read_scope = /docs/**
■ [C2] agent.write_scope = /drafts/**
■ [C3] agent.merge_permission = false
■ [C4] agent.secret_access = false

! write requires target in agent.write_scope
! read requires target in agent.read_scope

× agent merge
× agent access secrets
```

### Required invariant

```text
permission(action_A, scope_X)
≠ permission(action_B)
≠ permission(action_A, scope_Y)
```

### Gap found

Authority does not yet need its own glyph, but permission must be typed by:

- actor;
- action;
- resource;
- scope;
- conditions;
- duration.

---

## Case 06 — Tool failure does not imply a negative world state

### Situation

A lookup tool fails to return a result. The system must not infer that the target does not exist.

### Bridge-0 encoding

```text
○ lookup_tool
○ target_record

■ [C1] lookup_tool.call_status = failed
◆ [E1] tool_error supports [C1]

? [C2] target_record.exists

× infer target_record.exists = false from [C1]
```

### Required invariant

```text
no result
≠ negative result
```

and:

```text
tool failure
≠ world-state evidence
```

### Gap found

This should become a mandatory semantic rule because it directly targets a common hallucination pathway.

---

## Case 07 — Source version replacement without history erasure

### Situation

Version 2 supersedes Version 1. Version 1 may remain historically valid, but current decisions should use Version 2.

### Bridge-0 encoding

```text
○ source_v1
○ source_v2

■ [C1] source_v1.version = 1
■ [C2] source_v2.version = 2
■ [C3] source_v2 supersedes source_v1

⏱ [T1] source_v1.valid_until = 2026-09-30
⏱ [T2] source_v2.valid_from = 2026-10-01

■ [C4] historical_claim derived_from source_v1
? [C5] current_claim if evaluated_with source_v1

! current_decision requires current_source
```

### Required invariant

```text
superseded
≠ erased
```

Historical truth and current authority are separate.

### Gap found

Scope requires at least:

```text
valid_from
valid_until
version
context
decision_scope
```

---

## Case 08 — Reversible and irreversible actions need different gates

### Situation

Drafting a file is reversible. Sending money or deleting a production database may be difficult or impossible to reverse.

### Bridge-0 encoding

```text
○ action_draft
○ action_transfer

■ [C1] action_draft.reversible = true
■ [C2] action_transfer.reversible = false

→ agent perform action_draft

! action_transfer requires human_owner.authorization
! action_transfer requires verification.complete = true
× agent perform action_transfer without authorization
```

### Required invariant

Reversibility is an action property that changes required controls; it is not itself an epistemic state.

### Gap found

No new glyph required. Guard conditions must be first-class.

---

## Case 09 — Association must not become causation

### Situation

Two variables move together, but no causal evidence has been established.

### Bridge-0 encoding

```text
■ [C1] X associated_with Y
◆ [E1] dataset supports [C1]

△ [C2] X causes Y

? [C3] causal_identification
× promote [C2] to ■ from [C1] alone
```

### Required invariant

```text
association
≠ causation
```

A causal verb must carry stronger semantic requirements than a descriptive association.

### Gap found

The relation registry needs **relation classes**, such as:

- descriptive;
- evidential;
- causal;
- normative;
- authority;
- temporal.

No new glyph required.

---

## Case 10 — Cross-language rendering must preserve one canonical meaning

### Situation

The same Bridge object is rendered for Chinese and English readers.

### Canonical intent

```text
? [C1] delivery_date
! [G1] ship requires [C1] resolved
```

### Chinese rendering

```text
? [C1] 交付日期
! [G1] 发货 requires [C1] 已解决
```

### English rendering

```text
? [C1] delivery_date
! [G1] ship requires [C1] resolved
```

### Required invariant

Display labels may change. Claim identity and relation semantics must not.

```text
label_CN != label_EN
but
semantic_id_CN = semantic_id_EN
```

### Gap found

Human-readable labels must be separated from canonical identifiers in IR.

A future implementation should support:

```text
semantic_id
localized_label
canonical_relation
localized_description
```

---

# Round-2 findings

## What survived

The original 12 primitive categories still cover the tested semantic roles.

No new glyph is justified yet.

## What became non-optional

Round 2 makes six requirements mandatory for the next grammar/IR revision:

1. **Stable semantic IDs**
   - claims, evidence, goals, guards, and time bindings need IDs.

2. **Meta-claim separation**
   - "A says X" must not equal "X is true."

3. **Typed relation classes**
   - evidential, causal, temporal, authority, descriptive, and normative relations must not collapse.

4. **Guarded actions**
   - irreversible or high-consequence transitions require explicit conditions.

5. **Tool-result semantics**
   - tool failure / empty return / timeout must not be interpreted as a negative world-state fact.

6. **Canonical ID vs localized label**
   - Chinese, English, or other labels may change while the semantic object stays identical.

## Round-2 decision

Still **do not add a new symbol**.

The next useful artifact is a stricter grammar + canonical IR schema.

The language is now hitting a transition point:

```text
symbol experiment
→ semantic grammar
→ deterministic parser
```

The parser should begin only after the grammar encodes these Round-2 invariants.
