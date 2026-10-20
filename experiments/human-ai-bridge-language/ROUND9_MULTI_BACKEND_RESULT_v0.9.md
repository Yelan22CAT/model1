# Bridge-0 Round 9 — Multi-Backend Semantic Equivalence Result

> Status: Experimental v0.9

## Latest verified prototype result

```text
148 tests
148 passed
0 failed
```

All previous end-to-end gates remained green.

## Real generated workflow result

The generated workflow:

```text
bridge0_v09_backend_equivalence
```

executed successfully.

Steps:

```text
checkout                         ✓
setup Python                     ✓
GitHub backend probe             ✓
local backend runner             ✓
observable comparison            ✓
```

The comparison produced:

```text
BRIDGE_BACKEND_EQUIVALENT
sha256=53b7aef77cb78d64ca2518d7651b97aba18cf2d94790e3e548ef3da667f67657
```

## Negative control

A deliberate mismatch was also executed:

```text
backend-A
!=
backend-B
```

The comparator emitted:

```text
BACKEND_DRIFT
```

and the CI negative-control gate passed because the drift was correctly
detected.

## New tested behaviors

Round 9 covers:

- same Bridge source compiled/executed through two backend paths;
- deterministic Bridge rendering with observable fields;
- deterministic compiler output;
- observable capture;
- CRLF/LF normalization;
- positive equivalence;
- negative drift detection;
- unsupported observable rejection;
- unknown compiler-field rejection;
- checked-in generated workflow equality;
- real local backend execution;
- 20-observable-task compiler stress.

## Core result

The project now has an empirical pipeline:

```text
Bridge source
→ canonical semantics
→ backend A
→ observable A

Bridge source
→ canonical semantics
→ backend B
→ observable B

observable A == observable B
→ tested equivalence for that observable
```

This is the first round that tests backend semantic drift explicitly.

## Bounded conclusion

The current evidence supports:

> For the tested v0.9 program and stdout observable, the GitHub Actions path
> and the local deterministic runner produced identical normalized output.

It does not establish:

- universal backend equivalence;
- cross-OS equivalence;
- cross-language equivalence;
- equivalence of hidden side effects;
- equivalence for nondeterministic programs.

## Important design consequence

Compiler target differences are now treated as a first-class verification
problem rather than assumed away.

```text
same source
≠ automatically same behavior
```

Backend equivalence must be measured.

## Next test frontier

Move from text observables to typed semantic observables and execute across
genuinely heterogeneous runtimes.
