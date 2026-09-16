# Human Catch-up Gate

> A minimal external pacing and stop-control primitive for AI and agentic systems.

## Purpose

AI systems may generate conclusions, execute workflows, or recursively iterate faster than humans can understand, verify, and safely supervise them.

The Human Catch-up Gate is a small public control pattern for that mismatch.

```text
AI / Agent Runtime
        |
        v
   PRE-STOP GATE
        |
        +----> CONTINUE
        |
        +----> FREEZE
                 |
                 v
          Snapshot + Trace
                 |
                 v
           Human Review
                 |
        +--------+---------+----------+
        |        |         |          |
      Resume   Modify    Reject    Rollback
```

## Core idea

The mechanism is not intended to make humans faster than AI.

It is intended to preserve a higher-level human right:

> Humans do not need to be faster than AI at every step; they need to retain the authority to decide when the system may continue.

The stop authority must exist outside the model or agent.

A model may recommend stopping. A model must not own the authority to override the stop.

## Two locks

This public extension uses two distinct locks:

1. **Pre-stop lock** — an external control plane can freeze execution when risk, uncertainty, permission expansion, or human comprehension debt crosses an accepted boundary.
2. **Resume lock** — after a stop, the agent cannot resume itself. Resume requires both authorized human approval and an external readiness check confirming that state, permissions, and required invariants are restored.

This makes the gate fail-closed rather than relying on the agent's own judgment.

## What this is

- a pacing-control mechanism;
- a human re-entry mechanism;
- an external stop primitive;
- a way to limit comprehension debt;
- a building block for safer agent runtimes.

## What this is not

- a complete AI alignment solution;
- a claim that it can prevent existential catastrophe;
- a replacement for interpretability, evaluations, sandboxing, access control, or governance;
- a requirement that humans understand every low-risk AI output;
- a validated quantitative risk model.

## Public documents

- [`SPEC.md`](SPEC.md) — state machine and invariants;
- [`TRIGGERS.md`](TRIGGERS.md) — candidate pre-stop triggers;
- [`COMPREHENSION_DEBT.md`](COMPREHENSION_DEBT.md) — qualitative model of human understanding lag;
- [`THREAT_MODEL.md`](THREAT_MODEL.md) — what the mechanism can and cannot stop;
- [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) — compact design rules;
- [`TEST_PLAN.md`](TEST_PLAN.md) — minimum control tests.

## Integration boundary

This public material defines a control interface, not a full autonomous execution engine. Implementers should bind it to infrastructure they actually control: runtime permissions, credentials, network access, tool invocation, job execution, state snapshots, and human authorization.

The effectiveness of any stop mechanism is bounded by the resources it can actually revoke.