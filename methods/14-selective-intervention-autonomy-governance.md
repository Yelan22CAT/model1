# 14 — Selective Intervention and Autonomy Governance

## Purpose

Preserve high-throughput autonomous execution without turning safety and governance into a per-step latency tax.

The method separates the **execution plane** from a **shadow control plane**. Low-risk, reversible work may continue. Observation, evidence capture and recovery state can remain active in parallel. Intervention becomes synchronous only when a material boundary is crossed.

## Three operating states

```text
FREE RUN
  low-risk + reversible + inside authority boundary

SHADOW
  observe + score + log + checkpoint
  no behavior change unless a trigger matures

PREEMPT
  freeze / contain / reroute / rollback / escalate
  when a material boundary is crossed
```

## What the control plane watches

The primary question is not whether every local action is perfect. It is whether the overall trajectory remains acceptable and recoverable.

Useful trigger classes include:

- authority or permission escalation;
- irreversible external side effects;
- explicit constraint violation;
- state corruption or provenance loss;
- repeated dead ends or unrecoverable drift;
- runaway resource, cost or time consumption;
- loss of a credible checkpoint, rollback or alternative path;
- safety, privacy, legal or release boundaries that require accountable review.

## Trajectory recoverability

```text
local mistake
+ preserved state
+ bounded consequence
+ credible recovery path
= may continue

local mistake
+ irreversible consequence
or lost recovery path
= intervention candidate
```

This allows cheap mistakes while protecting against expensive or irreversible ones.

## Human-on-the-boundary

Human Final means the accountable human retains authority over consequential boundaries. It does not require a human approval click for every reversible step.

```text
human-in-every-step  ≠ required
human authority at consequential boundaries = required
```

## Bounded judges are sensors, not sovereigns

A fast classifier, judge, scoring model or deterministic rule can supply local signals. Those signals may help determine drift, risk, completion, relevance or recovery state. They do not independently gain permission to expand authority, waive hard rules or authorize irreversible action.

## Public acceptance tests

A future implementation should be able to demonstrate that:

1. low-risk reversible steps are not unnecessarily blocked;
2. shadow judgments can be inspected without changing behavior;
3. material intervention triggers create an auditable event;
4. a preempted run preserves enough state for review and recovery;
5. human authority is invoked at defined consequential boundaries rather than indiscriminately;
6. failure of the judgment layer does not silently grant broader authority.

## Boundary

This document is a public-safe architecture method. It does not publish private thresholds, credentials, hidden runtime packs, unrestricted permissions, production enforcement logic or a claim that these controls are already deployed.
