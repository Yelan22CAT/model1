# Bridge-0 Round 1 — Gap Ledger

> Purpose: record failures before changing the language.

| Gap ID | Observed problem | Frequency in Round 1 | Proposed response | New glyph? |
|---|---|---:|---|---|
| G01 | Claims cannot yet be referenced by stable IDs | high | Add explicit claim identifiers in grammar/IR | No |
| G02 | `■ field = ?` mixes fact marker with unknown value | high | Require one epistemic marker per proposition | No |
| G03 | Relation words are informal | high | Define typed relation registry | No |
| G04 | Verification scope is underspecified | medium | Bind verification to claim + field + scope + method | No |
| G05 | Stale/current validity needs explicit time rules | medium | Add validity/expiry attributes and temporal validator | No |
| G06 | Claim validity may depend on objective/context | medium | Add scope/context binding in IR | No |
| G07 | Authority is repeatedly needed | medium | Standardize `requires approval_by` / `allows` / `forbids` first | Not yet |
| G08 | State transitions are common | high | Formalize guarded transitions | No |
| G09 | Negation and prohibition can look similar | low | Reserve `×` for invalid/forbidden transitions; use explicit negative values for facts | No |
| G10 | 2D visual syntax not needed for current tests | none | Defer until 1D semantics stabilize | No |

## Key correction from Round 1

The initial example:

```text
■ person.age = ?
```

is too ambiguous.

Preferred v0.1 direction:

```text
? person.age
```

If a hypothesis exists:

```text
△ person.age ≈ 35
◆ source_X supports △ person.age
```

If verified:

```text
■ person.age = 35
◆ source_Y supports ■ person.age
✓ person.age verified_by source_check
```

This gives every proposition one explicit epistemic state.

## Why no new symbols were added

A symbol should exist only if it carries a semantic category that cannot be represented cleanly through:

- an existing primitive;
- a typed relation;
- an attribute;
- a guarded transition.

Round 1 showed that the current problem is mostly **formalization**, not missing pictograms.

## Next test target

Round 2 should test:

- nested claims;
- conflicting evidence;
- numerical uncertainty;
- multi-agent handoff;
- partial permissions;
- tool failure;
- source version replacement;
- reversible vs irreversible action;
- causal claims;
- cross-language rendering.

Only after those tests should the primitive alphabet be reconsidered.
