# Candidate Pre-stop Triggers

This document lists candidate trigger classes for a Human Catch-up Gate. These are categories for engineering review, not validated universal thresholds.

## Trigger classes

A pre-stop MAY be triggered when one or more of the following conditions appear:

### 1. Human comprehension lag

- unverified claims accumulate faster than humans can review them;
- new decisions depend on conclusions that remain poorly understood by accountable humans;
- operators report that they can no longer reconstruct the system's current reasoning, dependencies, or action state;
- explanation or trace quality falls below the level required for safe review.

### 2. Permission expansion

- the agent requests broader tool access;
- new credentials, data sources, network paths, or external systems are added;
- a task shifts from analysis to consequential execution;
- the agent attempts to modify its own permission boundary.

### 3. Recursive or accelerating behavior

- the system begins modifying its own workflow, graph, prompts, policies, or execution structure;
- recursive experiment loops exceed expected depth, rate, or duration;
- repeated self-generated dependencies make the current operating state difficult to independently verify.

### 4. Validator or evidence conflict

- independent validators materially disagree;
- critical evidence is missing, stale, unsupported, or contradictory;
- expected system state differs from observed system state;
- unresolved `UNKNOWN` states are being treated as if they were verified.

### 5. Irreversibility or high consequence

- money, identity, credentials, production systems, safety-critical systems, or external users are affected;
- an irreversible or difficult-to-reverse action is imminent;
- rollback is unavailable, untested, or uncertain;
- the cost of a mistaken continuation materially exceeds the cost of pausing.

### 6. Boundary deviation

- behavior departs from the accepted operating envelope;
- unauthorized architecture, policy, schema, or version changes appear;
- hidden or unexpected execution paths are detected;
- the system attempts to bypass a prior stop or retry limit.

## Human-trigger rule

A human operator's explicit statement that the system is moving too quickly to understand or supervise is itself a valid trigger candidate.

The purpose is not to prove that the AI is wrong. The purpose is to preserve time for human re-entry before continued execution creates additional uncertainty or irreversible consequences.

## Escalation pattern

```text
Low concern      -> Continue + monitor
Moderate concern -> Slow + explain + verify
High concern     -> Pre-stop + snapshot + human review
Critical concern -> Freeze + revoke consequential permissions + rollback/containment review
```

## Threshold policy

No fixed numerical threshold is claimed here. Production thresholds should be calibrated to task consequence, reversibility, autonomy, external reach, observability, and the reliability of the surrounding control plane.