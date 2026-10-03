# Bridge-0 Validator Rules v0.2

> Status: Experimental hard-rule set for the restricted grammar.  
> A validator checks semantic integrity after parsing. It does not decide real-world truth.

## V001 — Unique IDs

Every first-class semantic object must have a unique ID.

Reject:

```text
■ [C1] a = true
△ [C1] b = true
```

## V002 — One epistemic state per proposition

Reject mixed forms such as:

```text
■ [C1] delivery_date = ?
```

Require one of:

```text
■ [C1] delivery_date = 2026-10-15
△ [C1] delivery_date = estimated_date
? [C1] delivery_date
```

## V003 — Unknown carries no value

An UNKNOWN object must not contain a value.

## V004 — Evidence target must exist

```text
◆ [V1] source supports [C1]
```

requires `[C1]` to exist.

## V005 — Evidence does not promote claim state

Evidence attachment alone never changes:

```text
△ → ■
? → ■
```

Promotion requires a separate explicit verification/state transition process.

## V006 — Meta-claim separation

```text
■ [C2] agent_A asserted [C1]
```

must not alter the epistemic state of `[C1]`.

## V007 — Conflicting evidence remains unresolved

If:

```text
◆ E1 supports C1
◆ E2 opposes C1
```

the validator must record conflict.

It must not choose a winner unless an explicit reconciliation rule is supplied.

## V008 — Relation class is fixed

Examples:

```text
associated_with → descriptive
causes → causal
supports → evidential
requires → normative
supersedes → temporal
```

A parser/renderer may not silently substitute a relation from another class.

## V009 — Association cannot promote to causation

A descriptive relation cannot become causal solely by restatement.

## V010 — Tool failure is not negative world-state evidence

If:

```text
■ lookup_tool.call_status = failed
```

the validator must reject any derived fact equivalent to:

```text
■ target.exists = false
```

unless separate evidence supports that claim.

## V011 — Superseded is not erased

A source marked superseded remains addressable for historical provenance.

## V012 — Verification is scoped

```text
✓ [K1] [C1] verified_by source_check
```

verifies only the referenced object under the recorded method/scope.

It does not verify sibling claims automatically.

## V013 — Permissions do not expand

Permission must be evaluated as:

```text
(actor, action, resource, scope, conditions, time)
```

No dimension may be broadened by implication.

## V014 — Irreversible actions require explicit guards

If an action is declared:

```text
■ action_X.reversible = false
```

then consequential execution must have at least one explicit guard before a runtime can consider execution.

The validator does not decide whether the guard is sufficient.

## V015 — Handoff preserves state and provenance

A handoff may transform presentation, but it may not silently alter:

- source claim ID;
- epistemic state;
- evidence links;
- scope;
- timestamp;
- authority.

## V016 — Canonical identity is label-independent

Localized labels may change.

Semantic IDs and relation identities may not.

## V017 — Parse leftovers are errors

If any non-comment token remains after a grammar rule matches, parsing fails.

No best-effort interpretation.

## V018 — Unknown relation is error

Relations outside the registry must be rejected in the restricted parser.

Future versions may add extensible namespaces, but v0.2 does not.

---

## Validator output shape

Recommended:

```json
{
  "valid": false,
  "errors": [
    {
      "rule": "V010",
      "statement_id": "C7",
      "message": "Tool failure cannot establish target absence."
    }
  ],
  "warnings": [],
  "conflicts": []
}
```

The validator should be deterministic for the same IR input.
