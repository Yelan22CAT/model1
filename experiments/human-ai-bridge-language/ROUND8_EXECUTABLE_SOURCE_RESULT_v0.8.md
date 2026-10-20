# Bridge-0 Round 8 — Executable Source / Compiler Result

> Status: Experimental v0.8

## Latest verified results

Main prototype CI:

```text
136 tests
136 passed
0 failed
```

Compiler verification:

```text
Bridge source
→ parse
→ validate
→ compile
→ generated GitHub Actions YAML
→ byte-for-byte artifact comparison
✓ passed
```

Actual generated workflow:

```text
bridge0_v08_generated
checkout       ✓
setup Python   ✓
python module  ✓
workflow       ✓
```

## First true backend execution

This round is materially different from previous rounds.

The generated artifact was placed in:

```text
.github/workflows/bridge0-generated-v08.yml
```

GitHub recognized it as a workflow and actually executed the generated steps.

That is the first tested path where Bridge source produced a backend program
that ran on the target platform.

## Failure discovered and corrected

The first compiler output was not valid for the real GitHub Actions parser.

It emitted an invalid shell/YAML command representation.

This failure was not hidden.

The compiler was corrected, the artifact regenerated, and the real generated
workflow then passed.

This creates an important engineering rule:

```text
compiler unit tests
≠ backend acceptance
```

Therefore backend execution remains a mandatory verification gate.

## Compiler safety tests

The v0.8 suite now tests rejection of:

- raw shell tasks;
- shell metacharacter injection;
- relative path traversal;
- unsupported runners;
- push workflows without branch scope;
- arbitrary action fields.

The compiler target is intentionally narrower than GitHub Actions itself.

## Bounded conclusion

The current evidence supports:

> Bridge-0 can already function as a restricted source language for a real
> executable workflow backend.

It does not support the stronger claim that Bridge is already a complete
general-purpose programming language.

## Architectural consequence

The target architecture is now empirically demonstrated in miniature:

```text
Bridge source
      ↓
Canonical IR
      ↓
Validation
      ↓
Compiler
      ↓
Backend program
      ↓
Runtime
```

A human-language explanation is no longer required inside this execution path.

## Next test

The next valuable test is multi-backend semantic equivalence:

```text
same Bridge source
→ GitHub Actions backend
→ local deterministic backend
→ compare observable outputs
```

That will test whether Bridge semantics remain stable when the execution target changes.
