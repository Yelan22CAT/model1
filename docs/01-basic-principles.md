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
- escalate an issue;
- stop and review;
- request another source.

A concrete action can be checked. A vague situation cannot.

---

## 2. Separate evidence from assumption

Before acting, identify:

- what is known;
- what is assumed;
- what has been verified;
- what remains uncertain;
- what evidence would change the decision.

A confident explanation is not the same as a verified source.

---

## 3. Check consequence and reversibility

Ask:

- What could this action change?
- What cost could accumulate?
- Can the action be reversed?
- Can a smaller test be used first?
- Are options being preserved or closed?

The less reversible the action, the stronger the review should be.

---

## 4. Keep boundaries explicit

A boundary should be visible before execution.

Public examples include:

- insufficient evidence;
- unclear responsibility;
- rising irreversible cost;
- AI output being treated as authority;
- pressure to act before verification;
- loss of a safe stop or rollback path.

---

## 5. Use signals as prompts, not commands

Model 1 uses three public signals:

- 🟢 **Green:** no stop-loss trigger is currently identified;
- 🟡 **Yellow:** slow down, verify, and preserve options;
- 🔴 **Red:** freeze or exit may be reasonable.

A signal does not authorize action. It prompts human review.

---

## 6. Preserve the Human Final Gate

AI may organize information, surface uncertainty, compare options, and support documentation.

AI must not absorb final accountability for consequential action.

The final decision remains human-controlled.

---

## 7. Maintain public/private separation

The public repository contains only a beginner-safe scaffold.

It excludes:

- private cases and identifiable narratives;
- workplace, relationship, family, medical, or financial details;
- private calibration chains and thresholds;
- hidden runtime packs;
- complete private engine logic;
- executable decision systems.

The public layer demonstrates the method without transferring the private core.

---

## Minimal review sequence

1. Define the next action.
2. Verify the important facts.
3. Identify consequence and reversibility.
4. Check explicit boundaries.
5. Assign a Green, Yellow, or Red review signal.
6. Apply the Human Final Gate.
7. Proceed, slow down, freeze, or exit through human judgment.

---

## Practice with public examples

Use the public-safe composite cases to see the sequence applied:

1. [`Source Drift in a Procurement Decision`](../examples/01-source-drift-procurement.md)  
   Demonstrates source reconciliation, master-data risk, consequence analysis, and reversible approval design.

2. [`Unverified Change Before Release`](../examples/02-unverified-change-release.md)  
   Demonstrates validation gaps, escalation, rollback analysis, release control, and the Human Final Gate.

The cases are composite, anonymized, and generalized. They are demonstrations of the public method, not reproductions of private records.
