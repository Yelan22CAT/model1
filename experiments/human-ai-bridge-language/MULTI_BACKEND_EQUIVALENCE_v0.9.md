# Bridge-0 Multi-Backend Equivalence v0.9

> Status: Experimental / backend-drift verification layer  
> v0.9 adds no new glyphs.

## Purpose

v0.8 proved that Bridge source can compile to a real GitHub Actions workflow.

v0.9 asks a harder question:

> If the same Bridge source is executed through two backend paths, do the
> observable results remain the same?

Tested path:

```text
same Bridge source
├→ GitHub Actions backend
└→ local deterministic backend
          ↓
canonical observable comparison
```

## Observable

v0.9 adds an optional compiler-facing field:

```text
observe=stdout
```

Example:

```text
→ [T3] task
  kind=python_module
  module=bridge_probe_v0_9
  cwd=experiments/human-ai-bridge-language/prototype
  observe=stdout
```

Both backends capture the same task's stdout and compare normalized bytes.

## Current backends

### GitHub Actions path

The compiler emits a native GitHub Actions task and captures stdout:

```text
python -m bridge_probe_v0_9 > .bridge-github-T3.stdout
```

### Local deterministic path

```text
local_runner_v0_9.py
```

parses and validates the same Bridge source, then executes the allowlisted task
locally and captures:

```text
.bridge-local-T3.stdout
```

## Equivalence gate

```text
compare_observables_v0_9.py
```

normalizes line endings and compares observable bytes.

Matching result:

```text
BRIDGE_BACKEND_EQUIVALENT sha256=...
```

Mismatch:

```text
BACKEND_DRIFT left=<hash> right=<hash>
```

and returns failure.

## Verified positive control

The real generated GitHub workflow executed both backend paths and returned:

```text
BRIDGE_BACKEND_EQUIVALENT
sha256=53b7aef77cb78d64ca2518d7651b97aba18cf2d94790e3e548ef3da667f67657
```

## Verified negative control

CI deliberately compared two different backend outputs.

The comparator returned:

```text
BACKEND_DRIFT
```

and the enclosing negative-control test passed only because the mismatch was
correctly detected.

So both directions are tested:

```text
same observable → equivalence
different observable → drift
```

## Compiler/runtime restrictions

The v0.9 execution subset remains intentionally narrow:

- checkout;
- setup_python;
- python_module;
- stdout observation.

No raw shell task is introduced.

The validator rejects unsupported observable kinds and unknown compiler fields.

## Important boundary

The two backend implementations are different execution paths, but in the
current end-to-end test they run on the same GitHub-hosted Ubuntu environment
and Python 3.12 runtime.

Therefore the current evidence supports:

```text
implementation-path equivalence
```

more strongly than:

```text
cross-platform equivalence
```

The latter remains untested.

## New validator rules

```text
V068 observable-kind binding
V069 compiler-field allowlist
V070 no-observable warning
```

## Next frontier

The next high-value layer is heterogeneous-runtime equivalence:

```text
same Bridge source
├→ Ubuntu / CPython
├→ another OS/runtime
└→ possibly another compiler target
          ↓
typed observable comparison
```

Plain stdout equality will also become insufficient for many real programs.

A later layer should define typed observables such as:

- exit state;
- JSON value;
- file content hash;
- state transition;
- structured API result;
- side-effect manifest.

That would let Bridge compare semantics rather than incidental text formatting.
