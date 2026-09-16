# Design Principles

These principles are intentionally small. They describe public control logic, not a complete private engine.

## 1. Correctness ≠ Comprehension

A result can be correct while humans do not yet understand, verify, or integrate it well enough to supervise consequential continuation.

## 2. Capability ≠ Authority

A system becoming more capable does not grant it more permission.

## 3. Agency ≠ Sovereignty

An agent may gain broader ability to plan or act while final stop, resume, and irreversible-action authority remain external.

## 4. Stop authority must be external

The stopped model must not be the sole authority that decides whether the stop still applies.

## 5. Resume is a new decision

A prior approval does not automatically survive a material state change.

```text
Prior approval + material change ≠ current approval
```

## 6. Freeze before irreversible escalation

The best time to preserve control is before the system obtains a state that is difficult or impossible to revoke.

## 7. Unknown remains unknown

A workflow must not fill missing control state with optimistic inference merely to keep moving.

## 8. Trace before restart

A human reviewer needs a recoverable snapshot, visible trace, and known control boundary before deciding whether to continue.

## 9. Minimum sufficient intervention

Not every low-risk AI output requires a stop.

Use the smallest intervention that preserves control:

```text
continue
→ slow
→ explain / compress
→ review
→ freeze
→ rollback / exit
```

## 10. Human time sovereignty

> Humans do not need to be faster than AI at every step; they need to retain the authority to decide when the system may continue.

## 11. Two locks are stronger than one

```text
Lock 1: Human Catch-up Gate
        stops consequential continuation.

Lock 2: Dual-Key Resume Lock
        prevents restart until both human authorization
        and external control-plane readiness are present.
```

## 12. Small control primitives can still matter

A safety primitive does not need to understand the whole system to be useful. Circuit breakers, watchdogs, interlocks, and emergency stops are valuable because they preserve a control boundary at the point where continued operation would increase risk.

The same principle motivates these public notes: add a small, auditable brake rather than claim a universal solution.
