# Bridge-0 Semantic Round-Trip Test Plan v0.2

> Goal: test whether a Bridge statement can travel through the machine representation and return without semantic drift.

## Core invariant

```text
Bridge source
→ deterministic parser
→ canonical IR
→ deterministic renderer
→ Bridge source'
→ deterministic parser
→ canonical IR'

Expected:

semantic(IR) = semantic(IR')
```

Textual formatting does not need to be identical.

Semantic identity must be identical.

## Why this matters

The project exists partly to reduce a common failure mode:

```text
human meaning
→ model interpretation
→ restatement
→ subtle state change
→ later false certainty
```

A canonical round-trip test asks a stricter question:

> Can the system transform representation without changing fact/hypothesis/unknown state, references, relation class, evidence links, guards, or time bindings?

## Fields that MUST survive

- semantic IDs;
- entity identity;
- epistemic state;
- claim path / subject / predicate / object;
- relation class;
- evidence target;
- guard relation;
- action actor/action/object;
- verification target/method;
- prohibition expression;
- time binding;
- numerical value and unit.

## Presentation fields that MAY differ

- whitespace;
- line spacing;
- localized display labels;
- comments;
- ordering only if a later version explicitly defines order as non-semantic.

v0.2 preserves statement order.

## Hard failure condition

If the renderer cannot produce unambiguous restricted syntax from IR, it must error.

It must not ask a language model to invent a surface form.

## Round-trip categories

1. fact / hypothesis / unknown;
2. meta-claim;
3. conflicting evidence;
4. action + guard + verification;
5. time validity;
6. numerical values + units;
7. tool failure + unknown world state;
8. descriptive vs causal relation.

## Negative corpus

The same CI also checks that malformed inputs are rejected:

```text
■ [C1] delivery_date = ?
? [C1] delivery_date = 2026-10-10
■ delivery_date = tomorrow
■ [C1] X probably_means Y
→ [A1] agent deploy target extra
★ [C1] a = true
```

The desired behavior is:

```text
unsupported / ambiguous
→ ParseError
```

not:

```text
unsupported / ambiguous
→ best guess
```
