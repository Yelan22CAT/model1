# Human Catch-up Gate

> A minimal external pacing-control primitive for AI and agentic systems.

## Problem

AI systems may generate conclusions, code, plans, experiments, or actions faster than humans can understand, verify, and safely supervise them.

That creates a control problem even when individual outputs appear correct:

```text
AI generation / execution pace
>
human comprehension / verification pace
```

Correctness does not imply comprehension, and nominal human oversight can become ineffective if humans cannot reconstruct the current state before the system moves again.

## Core idea

The Human Catch-up Gate adds a simple external control pattern:

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
  +--> snapshot state
  +--> preserve trace
  +--> suspend consequential external action
  |
  v
WAITING_HUMAN
  |
  v
review / explain / verify / integrate
  |
  v
Dual-Key Resume Lock
```

The objective is not to make humans faster than AI. The objective is to preserve enough time and authority for humans to re-enter the loop before consequential continuation.

## Authority rule

```text
Human / external governance authority
>
control plane
>
agent / model
```

A model may request or recommend a stop.

A model must not be able to cancel, bypass, or self-release an externally imposed stop.

## Candidate triggers

A pre-stop may be appropriate when one or more of the following occurs:

- unverified claims or dependencies accumulate faster than they can be reviewed;
- new decisions materially depend on AI-generated conclusions not yet understood by accountable humans;
- independent validators materially disagree;
- the agent requests broader permissions, credentials, tools, network reach, or execution scope;
- the agent proposes changing its own workflow, graph, policy, or control boundary;
- an irreversible or difficult-to-reverse action is imminent;
- money, identity, production systems, credentials, external users, or other high-consequence resources are affected;
- recursive or long-running loops exceed an accepted operating envelope;
- operators cannot reliably explain the current system state or why the next action is justified;
- the system departs from its accepted operating envelope;
- an accountable human explicitly invokes STOP.

These are categories, not validated quantitative thresholds.

## Minimal invariants

1. Stop authority exists outside the agent/model.
2. A stopped agent cannot resume itself.
3. Consequential external actions are suspended or revoked during freeze.
4. A recoverable state snapshot and audit trace are preserved.
5. Critical unknowns remain unknown; they are not silently promoted to verified facts.
6. Resume requires an external authorization path.
7. A freeze is not treated as failure, punishment, or proof that the model was wrong.
8. Human review may end in resume, modification, rejection, rollback, or continued hold.

## Human time sovereignty

The design principle is:

> Humans do not need to be faster than AI at every step; they need to retain the authority to decide when the system may continue.

The gate therefore protects a form of **human time sovereignty**: enough time to understand, verify, challenge, or refuse continuation before the system creates further irreversible dependency.

## Not a complete safety solution

This mechanism does not by itself solve alignment, interpretability, cybersecurity, model-weight security, distributed-system control, misuse, or catastrophic-risk governance.

Its value is narrower: it is a small control primitive that can be composed with evaluation, sandboxing, permissions, monitoring, rollback, incident response, and human governance.
