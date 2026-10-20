# Bridge-0 Cross-Language Compiler Semantics v0.11

> Status: Experimental / first true cross-language target layer

## Purpose

v0.10 showed that one Bridge program could preserve a typed semantic result
across Ubuntu, Windows, and macOS while still using Python 3.12.

v0.11 changes the implementation language itself.

The tested path is:

```text
same Bridge source
├→ Python 3.12 source
└→ Node.js 20 source
          ↓
typed JSON observable
          ↓
semantic equivalence / drift
```

## Language-neutral source

The Bridge source does not name a Python module or JavaScript command.

```text
⊙ [P1] program
  name=bridge0_v011_cross_language
  targets=python312,node20

→ [C1] compute
  op=stats
  values=2,3,5,7,11,13
  observe=json_value
```

The semantic task is:

```text
stats(integer sequence)
→ {
    count,
    max,
    min,
    sum
  }
```

This operation is defined above the backend implementation language.

## Python compiler target

The compiler generates:

```text
generated/generated_v0_11.py
```

using Python-specific implementation details.

## Node.js compiler target

The same Bridge IR generates:

```text
generated/generated_v0_11.mjs
```

using JavaScript / Node-specific implementation details.

The source files are structurally different.

Their declared semantic observable must remain equal.

## Real runtime verification

The generated GitHub workflow runs both compiled artifacts:

```text
python_backend  → Python 3.12
node_backend    → Node.js 20
compare_backends
```

Both outputs are parsed with the existing typed JSON comparator.

Verified canonical digest:

```text
d4198466737cdf57b1f75243ea8d6200b4bd3e8c3e05cf8b79ac53673ca12e8a
```

## Negative control

The test suite deliberately mutates only the Node backend result:

```text
sum = expected
→
sum = expected + 1
```

The comparator reports semantic drift.

Therefore:

```text
same Bridge source + correct compilers
→ equivalent typed observable

mutated backend
→ drift
```

## Compiler artifact gate

CI recompiles both generated sources from the Bridge source and requires exact
equality with the checked-in generated Python and Node files.

So the generated backend sources cannot silently drift away from the canonical
Bridge source.

## Input restrictions

v0.11 deliberately exposes only one language-neutral operation:

```text
op=stats
```

Input is a bounded integer sequence.

The validator rejects:

- missing target language;
- unknown target language;
- unknown operation;
- non-integer input;
- more than 256 input values;
- backend-specific fields in the semantic task.

This keeps the first cross-language semantic core small enough to audit.

## New validator rules

```text
V075 program / executable subset integrity
V076 exact cross-language target set
V077 semantic operation / observable binding
V078 bounded language-neutral input
```

## Main architectural consequence

v0.11 demonstrates a stronger form of Bridge-as-source-language:

```text
Bridge source
≠ Python source
≠ JavaScript source
```

Instead:

```text
Bridge source
        ↓
Canonical semantic operation
   ┌────┴────┐
   ↓         ↓
Python      Node
backend     backend
```

The implementation language is now a compiler target rather than part of the
canonical source semantics.

## Important boundary

The current cross-language result covers one small deterministic integer
operation.

It does not establish general semantic equivalence between Python and
JavaScript for:

- floating-point edge cases;
- filesystem semantics;
- concurrency;
- network I/O;
- date/time behavior;
- Unicode edge cases;
- error/exception semantics;
- nondeterminism.

Those require dedicated semantic contracts rather than assuming the languages
behave the same.

## Next frontier

The next higher-value round should attack semantic differences that are known to
vary across implementation languages:

```text
integer overflow
floating-point special cases
Unicode normalization
ordering
null / missing
exception behavior
time semantics
```

The goal should be to discover which semantics Bridge must define explicitly
instead of inheriting accidentally from Python or JavaScript.
