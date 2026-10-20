# Bridge-0 Grammar Draft v0.2

> Status: **Experimental Draft / Restricted 1D Grammar**  
> This document defines the first grammar intended for deterministic parsing.  
> It is deliberately small. Anything outside this grammar must be rejected rather than guessed.

## 1. Design goal

Bridge-0 v0.2 is not a general-purpose programming language.

Its first parser target is a **shared semantic contract** for:

- entities;
- claims;
- unknowns;
- evidence;
- goals;
- actions;
- constraints;
- verification;
- prohibition;
- time;
- typed relations;
- scoped authority.

The parser must prefer explicit failure over semantic guessing.

```text
ambiguous input
→ parse error

not:

ambiguous input
→ model guesses intended meaning
```

---

## 2. Core lexical rules

### 2.1 Statement markers

```text
○ entity
■ fact claim
△ hypothesis
? unknown
◆ evidence
! constraint / guard
⊙ goal
→ action / transition
✓ verification
× forbidden / rejected action
⏱ time binding
```

### 2.2 Stable IDs

Every first-class statement in v0.2 SHOULD have a stable ID:

```text
[E1] entity
[C1] claim
[V1] evidence
[G1] guard / constraint
[O1] goal
[A1] action
[K1] verification
[F1] prohibition
[T1] time binding
```

The prefix is a readability convention, not the semantic source of truth.

The parser treats the bracketed ID as an opaque identifier.

Valid examples:

```text
[C1]
[C_001]
[claim-7]
[abc]
```

Invalid:

```text
[]
[C 1]
```

### 2.3 Canonical identifiers

Machine-facing subjects, fields, predicates, and actions use ASCII identifiers in the restricted grammar:

```text
agent
human_owner
invoice.total
vendor.status
production.deploy
```

Localized display labels belong in rendering metadata, not in canonical identity.

---

## 3. One proposition, one epistemic state

A proposition may be:

```text
■ fact
△ hypothesis
? unknown
```

but never more than one at the same time.

Preferred forms:

```text
■ [C1] invoice.total = 4280 CAD
△ [C2] delay.cause = supplier_failure
? [C3] delivery_date
```

Rejected form:

```text
■ [C4] delivery_date = ?
```

Reason: it mixes FACT and UNKNOWN in one proposition.

---

## 4. Statement forms

### 4.1 Entity declaration

```text
○ [E1] agent
○ [E2] human_owner
```

Grammar:

```text
ENTITY := "○" ID IDENTIFIER
```

### 4.2 Fact / hypothesis assignment

```text
■ [C1] agent.can_prepare = true
△ [C2] delay.cause = supplier_failure
```

Grammar:

```text
CLAIM_ASSIGN := ("■" | "△") ID PATH "=" VALUE [UNIT]
```

### 4.3 Fact / hypothesis relation

```text
■ [C3] source_v2 supersedes source_v1
△ [C4] X causes Y
```

Grammar:

```text
CLAIM_REL := ("■" | "△") ID TERM RELATION TERM
```

### 4.4 Unknown

```text
? [C5] target_record.exists
? [C6] current_vendor_status
```

Grammar:

```text
UNKNOWN := "?" ID PATH
```

Unknown carries no invented value.

### 4.5 Evidence relation

```text
◆ [V1] invoice.pdf supports [C1]
◆ [V2] sensor_B_reading opposes [C7]
```

Grammar:

```text
EVIDENCE := "◆" ID TERM EVIDENTIAL_REL ID
```

where:

```text
EVIDENTIAL_REL := supports | opposes | derived_from
```

### 4.6 Constraint / guard

```text
! [G1] merge requires human_owner.approval
! [G2] write requires target.in(agent.write_scope)
```

Grammar:

```text
GUARD := "!" ID ACTION_EXPR NORMATIVE_REL CONDITION
```

where:

```text
NORMATIVE_REL := requires | allows | forbids
```

### 4.7 Goal

```text
⊙ [O1] produce_validated_result
```

Grammar:

```text
GOAL := "⊙" ID ACTION_EXPR
```

### 4.8 Action / transition

```text
→ [A1] agent prepare_change
→ [A2] control_plane preempt run
```

Grammar:

```text
ACTION := "→" ID ACTOR ACTION_NAME [OBJECT]
```

### 4.9 Verification

```text
✓ [K1] [C1] verified_by arithmetic_check
```

Grammar:

```text
VERIFY := "✓" ID ID verified_by TERM
```

Verification is scoped to the referenced semantic object.

### 4.10 Prohibition / rejection

```text
× [F1] agent self_merge
× [F2] deploy_without_approval
```

Grammar:

```text
FORBID := "×" ID ACTION_EXPR
```

The `×` marker is reserved for forbidden/rejected transitions, not ordinary factual negation.

Use:

```text
■ [C8] agent.merge_permission = false
```

for a factual negative value.

### 4.11 Time binding

```text
⏱ [T1] source_v2.valid_from = 2026-10-01T00:00:00Z
⏱ [T2] source_v1.valid_until = 2026-09-30T23:59:59Z
```

Grammar:

```text
TIME := "⏱" ID PATH "=" TIMESTAMP
```

---

## 5. Typed relation registry

Relations MUST belong to a semantic class.

### 5.1 Evidential

```text
supports
opposes
derived_from
```

### 5.2 Temporal

```text
supersedes
precedes
follows
```

### 5.3 Causal

```text
causes
contributes_to
prevents
```

### 5.4 Descriptive

```text
associated_with
contains
depends_on
```

### 5.5 Authority / normative

```text
requires
allows
forbids
owned_by
approval_by
```

The parser records relation class explicitly in IR.

A validator must prevent class drift such as:

```text
associated_with
→ silently rewritten as
causes
```

---

## 6. Meta-claims

Bridge must distinguish:

```text
A asserted X
```

from:

```text
X is true
```

Example:

```text
△ [C1] component.safe = true
■ [C2] agent_A asserted [C1]
```

Required invariant:

```text
■ [C2]
does not promote
△ [C1] → ■ [C1]
```

A claim reference is a TERM when written as an ID.

---

## 7. Scoped permission model

Permissions are not general capabilities.

Canonical permission tuple:

```text
(actor, action, resource, scope, conditions, valid_time)
```

Example facts:

```text
■ [C10] agent.read_scope = /docs/**
■ [C11] agent.write_scope = /drafts/**
■ [C12] agent.merge_permission = false
```

A validator must reject any inference that expands one tuple into another.

---

## 8. Guarded transition model

A transition becomes executable only if its guards are satisfied.

Example:

```text
→ [A10] agent transfer_funds payment_17
! [G10] transfer_funds requires human_owner.approval
! [G11] transfer_funds requires verification.complete
```

The grammar only represents the guard.

The runtime decides whether conditions are satisfied.

Bridge itself does not execute the action.

---

## 9. Tool-result semantics

Tool execution state and world state are different namespaces.

Valid:

```text
■ [C20] lookup_tool.call_status = failed
? [C21] target_record.exists
```

Invalid inference:

```text
lookup_tool.call_status = failed
→ target_record.exists = false
```

This is a hard semantic rule.

---

## 10. Value types

Restricted v0.2 values:

```text
STRING
NUMBER
BOOLEAN
IDENTIFIER
TIMESTAMP
PATH_LITERAL
REFERENCE_ID
```

Examples:

```text
"ready"
4280
0.72
true
false
supplier_failure
2026-10-01T22:00:00-04:00
/docs/**
[C1]
```

Units are parsed separately from numeric values where present.

---

## 11. Comments

Line comments begin with `#`.

```text
# this line is ignored by the parser
■ [C1] invoice.total = 4280 CAD
```

Inline comments are not supported in v0.2.

Reason: keep parsing deterministic.

---

## 12. Error behavior

The parser MUST reject rather than guess when:

- marker is unknown;
- ID is missing where required;
- assignment has no value;
- unknown has a value;
- relation is not registered;
- syntax can match more than one statement form;
- reference ID is malformed;
- timestamp field uses invalid timestamp syntax;
- trailing unparsed tokens remain.

Example:

```text
■ [C1] delivery_date = ?
```

Expected:

```text
ParseError:
mixed epistemic state:
FACT assignment cannot use UNKNOWN marker as a value.
Use:
? [C1] delivery_date
```

---

## 13. Minimal EBNF sketch

```ebnf
statement      = entity | claim_assign | claim_rel | unknown
               | evidence | guard | goal | action | verify
               | forbid | time ;

entity         = "○", id, identifier ;

claim_assign   = ("■" | "△"), id, path, "=", value, [unit] ;

claim_rel      = ("■" | "△"), id, term, relation, term ;

unknown        = "?", id, path ;

evidence       = "◆", id, term, evidential_relation, id ;

guard          = "!", id, action_expr, normative_relation, condition ;

goal           = "⊙", id, action_expr ;

action         = "→", id, actor, action_name, [object] ;

verify         = "✓", id, id, "verified_by", term ;

forbid         = "×", id, action_expr ;

time           = "⏱", id, path, "=", timestamp ;

id             = "[", id_char, { id_char }, "]" ;

path           = identifier, { ".", identifier } ;

identifier     = letter_or_underscore, { letter_or_digit_or_underscore_or_dash } ;

term           = identifier | path | id | string | number ;

relation       = evidential_relation
               | temporal_relation
               | causal_relation
               | descriptive_relation
               | authority_relation ;

evidential_relation = "supports" | "opposes" | "derived_from" ;

temporal_relation   = "supersedes" | "precedes" | "follows" ;

causal_relation     = "causes" | "contributes_to" | "prevents" ;

descriptive_relation = "associated_with" | "contains" | "depends_on"
                     | "asserted" ;

authority_relation = "requires" | "allows" | "forbids"
                   | "owned_by" | "approval_by" ;
```

This EBNF is intentionally incomplete around expressions and path literals.

The executable parser prototype defines the actually accepted subset.

---

## 14. v0.2 boundary

The following remain deferred:

- 2D spatial syntax;
- user-defined operators;
- macros;
- loops;
- general arithmetic;
- implicit type coercion;
- natural-language parsing;
- automatic synonym resolution;
- autonomous action execution.

v0.2 exists to establish **semantic discipline**, not expressive completeness.
