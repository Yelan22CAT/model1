# Threat Model

## Purpose

This file states the limits of the Human Catch-up Gate and Dual-Key Resume Lock.

A useful stop mechanism must be honest about the boundary it actually controls.

## Protects against some forms of

- accidental continued execution after human understanding has fallen behind;
- self-resume by an agent after an externally imposed freeze;
- stale approval silently carrying across material state changes;
- continuation while required state, trace, permissions, or validators are unknown;
- irreversible action proceeding before an accountable human has a chance to review;
- recursive workflows continuing indefinitely without an external pacing boundary.

## Does not by itself protect against

- independent AI systems outside this control plane;
- a compromised host operating system or privileged infrastructure layer;
- copied or distributed model instances outside the stop boundary;
- a model or operator that already obtained uncontrolled external infrastructure;
- hidden execution paths not governed by the gate;
- malicious human operators with higher privileges;
- physical or digital actions that have already become irreversible;
- credential theft outside the controlled environment;
- model-weight theft, supply-chain compromise, or broader cyberattack;
- failures of the external validator itself;
- unsafe organizational incentives that intentionally bypass the control;
- global catastrophic or existential risk as a whole.

## Control-boundary principle

> The effectiveness of a stop mechanism is bounded by the resources it can actually revoke, isolate, or hold.

A UI button that says STOP but cannot affect compute, credentials, tools, network access, or external-action permissions is not equivalent to a real control-plane stop.

## Bypass questions

Before relying on the mechanism, ask:

1. What resources can the stopped system still access?
2. Does another process, copy, agent, or credential path remain active?
3. Can the agent modify or disable the stop mechanism?
4. Can it create work that continues after the visible process is frozen?
5. Who can override the freeze?
6. Is that override auditable?
7. Can the system resume from an unknown or stale state?
8. Does a material change invalidate prior approval?

## Failure posture

If control state cannot be established, the safe interpretation is not "probably okay."

```text
Unknown control state
→ remain frozen
→ restore observability
→ verify boundary
→ reassess
```

## Tail-risk note

This repository does not assign a numerical probability to catastrophic or existential AI risk.

The design rationale is narrower: when a risk has very high consequence and uncertain probability, preserving external pause, trace, rollback, and human re-entry can be valuable even when the exact probability is unknown.
