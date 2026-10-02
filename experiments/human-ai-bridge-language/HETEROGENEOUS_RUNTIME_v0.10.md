# Bridge-0 Heterogeneous Runtime Equivalence v0.10

> Status: Experimental / typed semantic observable layer

## Purpose

v0.9 compared two execution paths on the same Ubuntu/CPython environment.

v0.10 asks a harder question:

> Can the same Bridge source produce the same typed semantic result across
> genuinely different operating-system backends?

The tested targets are:

```text
ubuntu-latest
windows-latest
macos-latest
```

All use Python 3.12, but the operating systems and runner implementations differ.

## Typed observable

v0.10 moves from text equality to:

```text
observe=json_value
```

Example:

```text
→ [T3] task
  kind=python_module
  module=bridge_probe_v0_10
  cwd=experiments/human-ai-bridge-language/prototype
  observe=json_value
```

The probe may render JSON with different key order, whitespace, line endings,
or integer/whole-float notation and still be semantically equal.

## Canonicalization

The comparator:

```text
compare_typed_observables_v0_10.py
```

performs:

- UTF-8 JSON parsing;
- rejection of NaN / Infinity;
- recursive key normalization;
- whole-float → integer normalization;
- canonical JSON serialization;
- semantic value comparison;
- canonical SHA-256 reporting.

Therefore:

```text
{"a":1,"b":2}
```

and:

```text
{
  "b": 2.0,
  "a": 1.0
}
```

are treated as the same declared JSON value.

## Heterogeneous compiler

The same Bridge source declares:

```text
targets=ubuntu-latest,windows-latest,macos-latest
```

The compiler generates:

```text
backend_ubuntu_latest
backend_windows_latest
backend_macos_latest
        ↓
artifact upload
        ↓
compare_backends
```

Each backend runs the same canonical Bridge task and emits a typed JSON
observable artifact.

## Verified real run

All three backend jobs passed:

```text
Ubuntu   ✓
Windows  ✓
macOS    ✓
```

The comparison job passed and produced:

```text
BRIDGE_TYPED_EQUIVALENT
sha256=d2bd73193dfdf95314fb1b2c53e53690ec14d97aef21b9e8f671b94e063159d5
```

## Negative control

CI also compares two deliberately different typed JSON values.

The comparator emits:

```text
HETEROGENEOUS_BACKEND_DRIFT
```

and the negative-control test passes only when that mismatch is detected.

## New validator rules

```text
V071 heterogeneous target-set validity
V072 typed observable binding
V073 compiler-field allowlist
V074 at least one typed observable required
```

## Important boundary

This round proves more than v0.9 because the operating systems differ.

It still does not prove universal cross-runtime equivalence.

All three paths use:

```text
Python 3.12
same probe implementation
same compiler-generated semantic task
```

So the next stronger test would change both runtime and backend language, for
example:

```text
same Bridge source
├→ CPython
├→ another Python implementation
└→ a non-Python backend
```

with the same typed semantic observable contract.

## Core principle

```text
format equality
≠ semantic equality
```

and:

```text
same source
≠ automatically same result
```

The declared observable is what must remain invariant.
