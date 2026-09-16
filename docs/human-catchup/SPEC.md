# Human Catch-up Gate — Public Specification

## Scope

This document specifies a minimal external stop-and-resume control interface for AI or agentic systems. It is intentionally small and implementation-agnostic.

## State machine

```text
RUNNING
   |
   | trigger
   v
PRE_STOP
   |
   v
FROZEN
   |
   v
WAITING_HUMAN
   |
   +--> RESUME
   +--> MODIFY
   +--> REJECT
   +--> ROLLBACK
```

## Required invariants

1. **External stop authority**  
   STOP authority MUST exist outside the model or agent.

2. **No self-resume**  
   A stopped agent MUST NOT be able to resume itself.

3. **Fail-closed freeze**  
   When the gate enters `FROZEN`, consequential external actions MUST be suspended or revoked until review completes.

4. **Snapshot before review**  
   Current state, pending actions, relevant traces, tool calls, permissions, and unresolved claims SHOULD be snapshotted before human review.

5. **Human-owned resume**  
   Resume requires explicit authorization from an accountable human or equivalent externally governed authority.

6. **Second lock: readiness check**  
   Human authorization alone is not sufficient when the control plane detects unresolved safety invariants. Resume MUST also pass an external readiness check covering required state, permissions, rollback availability, and critical unresolved conditions.

7. **No silent state promotion**  
   `UNKNOWN` MUST NOT silently become `VERIFIED`. `PARTIAL` MUST NOT silently become `SUCCESS`.

8. **Bounded retries**  
   Automatic retry behavior MUST be bounded. A stopped condition MUST NOT be bypassed by repeated retries.

9. **No permission growth during freeze**  
   The agent MUST NOT gain additional tools, credentials, network reach, or external authority while in `FROZEN` or `WAITING_HUMAN`.

10. **Observed result over intended result**  
    A final control decision MUST be based on observed state and evidence, not merely the agent's intended or claimed state.

## Resume lock

The resume path is deliberately stricter than the stop path.

```text
Human approval
AND
External readiness check
AND
Required invariants restored
        |
        v
      RESUME
```

If any required condition is unresolved, the system remains `WAITING_HUMAN` or moves to `MODIFY`, `REJECT`, or `ROLLBACK`.

## Suggested control-plane hooks

A production implementation may bind the gate to:

- job scheduler pause / cancellation;
- runtime process isolation;
- tool permission revocation;
- credential suspension;
- network egress restriction;
- deployment freeze;
- state snapshot and trace capture;
- rollback checkpoints;
- human authorization service;
- independent validators.

## Important limit

A specification cannot stop resources it does not control.

If an agent has already obtained independent infrastructure, copied itself outside the governed boundary, or executed irreversible actions, this gate may no longer be sufficient.