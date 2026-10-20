# Bridge-0 Round 10 — Heterogeneous Runtime / Typed Observable Result

> Status: Experimental v0.10

## Latest verified prototype result

```text
161 tests
161 passed
0 failed
```

All earlier end-to-end gates remained green.

## Real heterogeneous workflow

The generated workflow:

```text
bridge0_v010_typed_equivalence
```

executed on three real GitHub-hosted operating-system runners.

Results:

```text
backend_ubuntu_latest   ✓
backend_windows_latest  ✓
backend_macos_latest    ✓
compare_backends        ✓
```

## Typed semantic comparison

All three runners produced the same canonical JSON semantic value.

Verified digest:

```text
d2bd73193dfdf95314fb1b2c53e53690ec14d97aef21b9e8f671b94e063159d5
```

## Negative control

A deliberate semantic change:

```text
result=42
→
result=43
```

was detected as:

```text
HETEROGENEOUS_BACKEND_DRIFT
```

## New tested behaviors

Round 10 covers:

- three-OS target declaration;
- target uniqueness and allowlisting;
- typed JSON observables;
- key-order independence;
- whitespace independence;
- CRLF/LF irrelevance through JSON parsing;
- whole-float/integer normalization;
- non-finite JSON rejection;
- semantic-drift detection;
- deterministic heterogeneous compiler output;
- generated artifact equality;
- real Ubuntu / Windows / macOS execution.

## Main result

The tested Bridge source now has verified semantic equivalence across three
different operating systems for the declared typed observable.

This is stronger than the v0.9 same-environment implementation-path test.

## Bounded conclusion

The evidence supports:

> For the tested Bridge v0.10 program, Ubuntu, Windows, and macOS runners using
> Python 3.12 produced the same canonical JSON semantic observable.

It does not establish:

- universal cross-language equivalence;
- equivalence of hidden side effects;
- nondeterministic-program equivalence;
- equivalence across all Python implementations;
- general-purpose program semantics.

## Next frontier

The next high-value test is a true cross-language compiler target:

```text
same Bridge source
├→ Python backend
└→ another implementation language/runtime
          ↓
typed semantic observable
          ↓
equivalence / drift
```

That would test whether Bridge semantics survive not only OS variation, but
compiler-target language variation.
