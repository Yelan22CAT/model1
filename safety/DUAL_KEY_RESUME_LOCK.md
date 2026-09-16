# Dual-Key Resume Lock

> A second lock for systems that have already entered a frozen state.

## Why add a second lock?

A stop mechanism is weaker if the same agent that was stopped can immediately resume itself, if a single accidental approval can restart execution, or if the system resumes before its control state is restored.

The Dual-Key Resume Lock separates **stopping** from **permission to continue**.

## Rule

After a Human Catch-up Gate freeze, consequential execution may resume only when two independent conditions are satisfied:

```text
KEY 1 — Authorized human decision
AND
KEY 2 — External control-plane invariant check
```

Neither key alone is sufficient.

## Key 1 — Human authorization

An accountable human explicitly chooses one of:

```text
RESUME
MODIFY_AND_RESUME
ROLLBACK
REJECT
KEEP_FROZEN
```

Silence, timeout, model recommendation, or prior approval does not count as a new resume authorization.

## Key 2 — External invariant check

A control layer outside the stopped agent confirms the minimum restart conditions relevant to the system, for example:

- the current state snapshot exists and is readable;
- the execution trace is preserved;
- tool, credential, network, and external-action permissions are in the intended state;
- critical validators have completed or unresolved failures are explicitly surfaced;
- version and configuration boundaries are known;
- rollback or containment remains available where required;
- the requested resume path matches the human-approved scope.

The same stopped model must not be the sole authority that declares these invariants satisfied.

## Minimal state transition

```text
FROZEN
  |
  v
WAITING_HUMAN
  |
  +--> Human approval? -------- no --> remain frozen
  |
 yes
  |
  +--> External invariants? --- no --> remain frozen / repair / rollback
  |
 yes
  v
RESUME_READY
  |
  v
RESUME within approved scope
```

## Hard invariants

1. `MODEL_REQUEST_RESUME` is not `RESUME_AUTHORIZED`.
2. Prior authorization does not silently survive a material state change.
3. Human approval without control-plane readiness does not restart the system.
4. Control-plane readiness without human approval does not restart the system.
5. Resume scope must not exceed the scope explicitly approved.
6. If the system cannot prove which state it is resuming from, it remains frozen.
7. A new material change after approval invalidates the stale resume decision and requires reassessment.

## Why this matters

The first lock answers:

```text
When should continuation stop?
```

The second lock answers:

```text
What must be true before continuation is allowed again?
```

Together they create a minimal two-stage brake:

```text
PRE-STOP / FREEZE
        +
DUAL-KEY RESUME
```

This remains a design pattern, not a production-certified safety mechanism.
