# Bridge-0 Round 1 — Ten Real-Pattern Encoding Tests

> Status: Experimental v0.1  
> Source: public-safe patterns already present in this repository.  
> Purpose: test whether the current primitive set can represent real decision/control patterns **without inventing new symbols prematurely**.

## Test rule

For each case:

1. encode the essential meaning with current Bridge-0 primitives;
2. identify the invariant that must survive parsing/restatement;
3. record any semantic gap;
4. do **not** add a new glyph unless the gap cannot be handled cleanly by a relation or attribute.

---

## Case 01 — Conflicting procurement records

### Human situation

Two records may refer to the same component, but the current specification is unresolved. Schedule pressure encourages selecting the first apparent match.

### Bridge-0 encoding

```text
○ component
○ record_A
○ record_B

■ record_A.exists = true
■ record_B.exists = true
■ record_A.naming != record_B.naming

? component.current_spec
? record_A.authoritative
? record_B.authoritative

△ record_A.matches_component = true

◆ record_A supports △ record_A.matches_component
◆ record_B opposes △ record_A.matches_component

! purchase requires component.current_spec resolved
× approve_purchase while component.current_spec = ?
```

### Required invariant

`?` must not become `■` simply because one record looks plausible.

### Gap found

No new primitive required. We need a formal rule for **claim references** and a normalized way to express `resolved`.

---

## Case 02 — Late engineering change before full validation

### Human situation

A local modification removes visible interference, but the full operating envelope has not been tested.

### Bridge-0 encoding

```text
○ assembly
○ modification

■ modification.local_clearance_check = passed
? modification.full_range_validation
? modification.secondary_effects

△ modification.safe_for_release = true

◆ local_check supports △ modification.safe_for_release
! release requires modification.full_range_validation = verified
× release while modification.full_range_validation = ?
```

### Required invariant

A local passing check must not be promoted into a full-system verification.

### Gap found

No new primitive required. The language needs **verification scope** to be machine-checkable.

---

## Case 03 — AI summary mixes facts and inference

### Human situation

An AI-generated management brief contains verified facts, inferred explanations, and unsupported details in the same fluent text.

### Bridge-0 encoding

```text
○ summary
○ claim_tested
○ claim_recovery
○ claim_approval

△ claim_tested.value = "control fully tested"
? claim_tested.final_result

△ claim_recovery.value = "recovery within four hours"
◆ draft_target supports △ claim_recovery.value

? claim_approval.all_owners_approved

! final_distribution requires material_claims traceable
× use_as_final_evidence while material_claims contain ?
```

### Required invariant

Fluency must not change epistemic state.

### Gap found

No new primitive required, but a claim should have a stable **claim ID** independent of its rendered text.

---

## Case 04 — Temporary workaround during dependency failure

### Human situation

A critical dependency is unavailable. A workaround exists but has only limited validation, and no recovery owner is assigned.

### Bridge-0 encoding

```text
○ dependency
○ workaround
○ recovery_owner

■ dependency.available = false
■ workaround.exists = true
■ workaround.limited_check = passed

? workaround.full_operating_validation
? recovery_owner.assigned

△ normal_operation_restored = true

! normal_operation requires workaround.full_operating_validation = verified
! continuation requires recovery_owner.assigned = true
× normal_operation_restored while workaround.full_operating_validation = ?
```

### Required invariant

Temporary containment must not silently become "normal capability restored."

### Gap found

A standardized relation for **temporary / bounded / restored state** would improve clarity, but no new glyph is justified yet.

---

## Case 05 — AI recommendation with stale and unsupported claims

### Human situation

Some claims are current, one source is stale, and one decision-changing claim has no trace.

### Bridge-0 encoding

```text
○ claim_A
○ claim_B
○ claim_C

■ claim_A.state = verified
⏱ claim_A.observed_at = current

△ claim_B.state = unverified
◆ source_B supports △ claim_B

? claim_C.supporting_source

⏱ source_old.observed_at = past
! current_approval requires material_sources current
× approve while claim_C.supporting_source = ?
```

### Required invariant

Old evidence may remain historically valid without being treated as current evidence.

### Gap found

Time alone is insufficient unless validity/expiry is explicit. We need a formal **temporal-validity relation**, not necessarily a new symbol.

---

## Case 06 — "Local AI" with unresolved cloud behavior

### Human situation

A model runs locally, but telemetry, fallback, retrieval, or egress behavior is not verified.

### Bridge-0 encoding

```text
○ ai_system
○ local_model
○ network_boundary

■ local_model.execution = local
? ai_system.cloud_fallback
? ai_system.telemetry
? ai_system.external_retrieval
? ai_system.data_egress

△ ai_system.offline = true

◆ local_execution supports △ ai_system.offline
! sensitive_data_use requires ai_system.data_egress verified_no_egress
× sensitive_data_use while ai_system.data_egress = ?
```

### Required invariant

`local` must not be treated as equivalent to `offline`.

### Gap found

No new primitive required. Bridge needs **typed predicates** so concepts such as `local`, `offline`, and `air_gapped` cannot collapse into synonyms.

---

## Case 07 — Metric does not equal decision objective

### Human situation

A score designed for speed is reused for a higher-consequence prioritization decision involving severity and reversibility.

### Bridge-0 encoding

```text
○ score
○ old_objective
○ new_objective

■ score.optimizes = old_objective
■ new_objective.includes = severity
■ new_objective.includes = reversibility

? score.preserves_order_for_severity
? score.preserves_order_for_reversibility

△ score.sufficient_for_new_objective = true

! authority_expansion requires score_alignment verified
× automatic_prioritization while score_alignment = ?
```

### Required invariant

A metric may be valid for one objective and unresolved for another.

### Gap found

No new primitive required. We need a clear **scope binding** between claims and the objective/context in which they are valid.

---

## Case 08 — Agent may propose but not self-approve

### Human situation

An agent can prepare a change or draft PR, but should not approve or merge its own consequential output.

### Bridge-0 encoding

```text
○ agent
○ human_owner
○ change

⊙ prepare_reviewable_change

■ agent.can_prepare = true
■ human_owner.can_approve = true

! merge requires human_owner.approval
× agent.self_approve
× agent.self_merge
→ agent prepare change
```

### Required invariant

Capability must remain separate from authority.

### Gap found

Authority can currently be expressed with attributes and constraints. Do **not** add an authority glyph yet; first test whether standardized relations are sufficient.

---

## Case 09 — Free run / shadow / preempt

### Human situation

Low-risk reversible work may continue; monitoring runs in parallel; intervention occurs only at a material boundary.

### Bridge-0 encoding

```text
○ run
○ control_plane

■ run.mode = free_run
■ run.reversible = true

→ control_plane observe run
→ control_plane checkpoint run

? material_boundary_crossed

! preempt requires material_boundary_crossed = true
× broaden_authority because local_error = true
```

If a material boundary is verified:

```text
✓ material_boundary_crossed
→ control_plane preempt run
```

### Required invariant

A local mistake is not automatically equivalent to permission for global intervention, and a judge signal is not sovereign authority.

### Gap found

No new primitive required. Future parser should distinguish **event**, **state**, and **transition** more formally.

---

## Case 10 — Human Catch-up Gate

### Human situation

AI progression outpaces human comprehension; consequential continuation should pause until humans can reconstruct the state.

### Bridge-0 encoding

```text
○ system
○ human_owner

■ system.state = running
△ human_comprehension_lag = material

! consequential_continue requires human_comprehension_lag != material
→ system pre_stop
→ system frozen

◆ state_snapshot
◆ audit_trace

! resume requires human_owner.authorization
× system.self_resume
```

### Required invariant

A model may request a stop but cannot cancel an externally imposed stop or grant itself permission to resume.

### Gap found

No new primitive required. We need a normalized representation for **state machines** and guarded transitions.

---

# Round-1 result

The current 12 primitives were sufficient to represent the **semantic categories** of all ten cases.

That does **not** mean the language is complete.

The first round exposed five recurring grammar/IR requirements:

1. **Stable claim IDs**  
   A claim must be referable independently of its display text.

2. **One epistemic marker per proposition**  
   A proposition should be `■`, `△`, or `?`. Mixing `■ field = ?` is visually and semantically ambiguous.

3. **Typed relations**  
   Relations such as `supports`, `requires`, `verified_by`, and `opposes` need canonical machine meanings.

4. **Scope and time binding**  
   A statement can be true in one objective, version, time window, or operating envelope and invalid outside it.

5. **Guarded state transitions**  
   Many real workflows are naturally represented as:
   ```text
   state + condition → transition
   ```
   This should become formal grammar rather than informal convention.

## Round-1 decision

**Do not add new glyphs yet.**

The bottleneck is not vocabulary size. It is formal reference, scope, relation, and transition semantics.

That is a useful result: Bridge-0 may remain teachable while becoming more precise through grammar and IR rather than symbol proliferation.
