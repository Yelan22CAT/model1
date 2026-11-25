# 38 — Bidirectional Human–Automation Authority & Layered Assurance
**Status:** User-authorized method-level Full-Push / Not Frozen (2026-11-25). Public-safe augmentation of Method 33 (AITR-G), **not** a deployed flight-control policy, aviation brand ranking, production Bridge change, or foundation-weight update.

## Problem
Safety-critical automation can fail in two directions:

- a human can issue an unsafe command, misunderstand state, or react too slowly;
- an automated controller can act on wrong sensors, wrong state estimates, flawed logic, stale evidence, or a degraded mode.

A safe design therefore cannot reduce the problem to either “human always wins” or “automation always wins.”

## Core invariants
`Human Final != Manual Everything`

`Human-in-the-loop != Meaningful Human Control`

`Design Safe != Built Safe != Operated Safe != Organization Safe`

Human Final can coexist with pre-authorized automatic protection when the automated response is bounded, independently validated, observable, and faster than a human could safely orient and act.

## 1. Bidirectional error containment
### Machine catches predictable human error
Use deterministic limits, validation, interlocks, bounded envelopes, or safe-state responses where the hazard is well modeled and the protection itself is tested.

### Human or independent assurance catches machine error
Expose current mode, relevant evidence, sensor disagreement, action history and remaining authority. Preserve a tested path to pause, reject, degrade, isolate, roll back, escalate, or enter a safe state when automation is wrong or uncertain.

Neither side may be its own sole proof of correctness.

## 2. Authority is state-dependent
Authority should vary with operating state rather than with a permanent slogan.

- **Routine state:** automation may carry repetitive, high-frequency control.
- **Known bounded hazard:** pre-validated automatic protection may act faster than a person.
- **Degraded state:** protection loss, sensor conflict and mode changes must be visible.
- **Unknown or contested state:** require independent evidence, expert review, or a safe stop.
- **Time-to-harm < time-to-orient-and-act:** nominal human review is not meaningful control.

## 3. Protection must be observable and degradable
A safety mechanism is itself a system that can fail.

Require:
1. clear current operating mode;
2. visible loss or downgrade of protections;
3. auditable action/effect history;
4. analysis of shared dependencies and common-mode failure;
5. rehearsed recovery and authority-transfer paths;
6. evidence that the human has enough time, skill and state understanding to intervene.

An override control alone is not evidence of safe takeover.

## 4. Layered assurance
Do not infer end-to-end safety from a correct architecture diagram.

Review separately:
1. architecture and control philosophy;
2. detailed implementation;
3. verification/certification;
4. build/manufacturing conformance;
5. maintenance and change control;
6. operations and training;
7. organizational incentives and governance;
8. real-world outcomes, incidents and near-misses.

A PASS in one layer cannot erase a FAIL in another.

## 5. AI / agent mapping
For AI-assisted systems:

- AI may catch omissions, conflicts, schema errors and obvious out-of-policy actions.
- Deterministic workflows should remain preferred where they are sufficient.
- People must be able to inspect what the AI did, why, from which evidence, and what external effects already occurred.
- High-risk, irreversible, disputed or unknown states require fresh authorization, independent evidence or safe stop/escalation.
- Model output must not serve as the sole evidence that its own action succeeded.

This extends AITR-G rather than creating a competing governance stack.

## Acceptance questions
Before consequential use, answer:

1. Who currently owns control authority, and why?
2. Which human actions are constrained automatically, and how were those constraints validated?
3. Can a human actually override the system within the available time?
4. Is degradation clearly visible?
5. Which data/sensors/models are single points or common dependencies?
6. How is build/deployment conformance checked after design approval?
7. Can maintenance or version drift invalidate prior assurance?
8. Which incidents or near-misses feed back into redesign?
9. Can schedule/cost incentives bypass safety checks?
10. What independent evidence proves the external effect?

Unknown critical answers must hold rather than default to “safe.”

## Boundaries
- No claim that Boeing-, Airbus-, human-first-, or automation-first philosophies are inherently safer.
- Aviation examples are structural analogies; domain certification remains domain-specific.
- Existing Bridge witness-forgery, signer-independence, provenance and timeout blockers remain OPEN / Production HOLD.
- No external actuation, production deployment, formal Bridge grammar release, operator certification, or foundation-model weight change.

**Integration:** Method 33 AITR-G, Human Final, ANASG/minimal sufficient autonomy, evidence/effect separation, PERV-G / Reality Gate, and existing Bridge authority gates.
