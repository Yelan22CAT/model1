# Basic Principles

This document explains the public principles behind **Model 1 v1.0**.

Model 1 is a human-controlled judgment guardrail for AI-assisted work. It helps a person pause before a consequential next step, especially when evidence is incomplete, cost is rising, or reversibility is shrinking.

It is a decision-support scaffold, not an autonomous decision-maker.

---

## 1. Define the next action

Start with the action that is about to happen.

Examples:

- send a message;
- approve a change;
- continue a task;
- place an order;
- release a system;
- escalate an issue;
- stop and review;
- request another source.

A concrete action can be checked. A vague situation cannot.

---

## 2. Separate fact, inference, assumption, and unknown

Before acting, identify:

- what is directly observed;
- what has been verified;
- what is a bounded inference;
- what is assumed;
- what remains unknown;
- what evidence would change the decision.

A confident explanation is not the same as a verified source.

---

## 3. Preserve an unresolved state

Do not force incomplete evidence into a binary answer.

Use a bounded evidence direction:

- `+` — present evidence supports the proposed path;
- `0` — evidence is insufficient, mixed, or unresolved;
- `-` — present evidence opposes the proposed path.

`0` is not concealed approval, concealed rejection, or failure. It preserves judgment until the evidence improves.

---

## 4. Keep evidence direction separate from action risk

Model 1 uses two public axes:

1. evidence direction: `+ / 0 / -`;
2. action-risk signal: Green / Yellow / Red.

Evidence direction describes the current case for or against the path. The risk signal describes how strongly the person should pause before acting.

A supported path can still deserve Yellow when reversibility is low. An unresolved path can require Red when a hard validation or authorization requirement is missing.

---

## 5. Check consequence and reversibility

Ask:

- What could this action change?
- What cost could accumulate?
- Can the action be reversed?
- Can a smaller test be used first?
- Are options being preserved or closed?
- Who will own exceptions, maintenance, correction, and rollback?

The less reversible the action, the stronger the review should be.

---

## 6. Keep boundaries explicit

A boundary should be visible before execution.

Public examples include:

- insufficient evidence;
- unclear responsibility;
- rising irreversible cost;
- AI output being treated as authority;
- pressure to act before verification;
- loss of a safe stop or rollback path;
- a missing authorization or required validation step;
- a privacy or consent limit.

Nuance must not be used to wash away a hard boundary.

---

## 7. Use gray where evidence is gray

Do not compress:

- partial support into complete approval;
- caution into opposition;
- one flaw into a total judgment;
- a local success into proof of repeatable operation;
- current evidence into permanent certainty;
- minor and fatal risk into one label.

A conclusion should be no more precise than its evidence.

---

## 8. Use risk signals as prompts, not commands

Model 1 uses three public risk signals:

- 🟢 **Green:** no stop-loss trigger is currently identified;
- 🟡 **Yellow:** slow down, verify, and preserve options;
- 🔴 **Red:** freeze or exit may be reasonable.

A signal does not authorize action. It prompts human review.

---

## 9. Preserve the Human Final Gate

AI may organize information, surface uncertainty, compare options, and support documentation.

AI must not absorb final accountability for consequential action.

The final decision remains human-controlled.

---

## 10. Prefer compact, auditable output

A useful decision-support response should normally state:

1. the bounded conclusion;
2. decisive evidence;
3. unresolved unknowns;
4. what would reverse the conclusion;
5. one safe and reversible next action.

Length, repetition, confidence, or hidden scratch work do not prove correctness.

---

## 11. Maintain public/private separation

The public repository contains only a beginner-safe scaffold.

It excludes:

- private cases and identifiable narratives;
- workplace, relationship, family, medical, or financial details;
- private calibration chains and thresholds;
- observer packs and detailed market or interaction models;
- anti-poisoning implementation internals;
- hidden runtime packs;
- complete private-engine logic;
- executable decision systems.

The public layer demonstrates the method without transferring the private core.

---

## Minimal review sequence

1. Define the next action.
2. Separate fact, inference, assumption, and unknown.
3. Assign an evidence direction: `+ / 0 / -`.
4. Identify consequence, responsibility, and reversibility.
5. Check explicit and hard boundaries.
6. Assign a Green, Yellow, or Red risk signal.
7. State what evidence would reverse the conclusion.
8. Apply the Human Final Gate.
9. Proceed, slow down, freeze, or exit through human judgment.

For the public language interface and canonical states, see [`docs/02-judgment-language.md`](02-judgment-language.md).

---

## Practice with public examples

Use the public-safe composite cases to see the sequence applied:

1. [`Source Drift in a Procurement Decision`](../examples/01-source-drift-procurement.md)  
   Demonstrates unresolved evidence direction, source reconciliation, master-data risk, consequence analysis, and reversible approval design.

2. [`Unverified Change Before Release`](../examples/02-unverified-change-release.md)  
   Demonstrates evidence opposing release, validation gaps, escalation, rollback analysis, release control, and the Human Final Gate.

The cases are composite, anonymized, and generalized. They are demonstrations of the public method, not reproductions of private records.
