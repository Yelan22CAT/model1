# Start Here

This is the beginner entry point for **Model 1 v1.0**.

Model 1 is a public-safe judgment support scaffold. It helps a person pause before taking a consequential next step, especially when the situation involves uncertainty, rising cost, unclear sources, or reduced reversibility.

It is not an autonomous system.  
It is not a private engine.  
It is not personal advice.  
It is not a replacement for human judgment.

The purpose of this guide is simple:

> Slow down before action.  
> Separate fact, inference, and unknown.  
> Check the boundary and reversibility.  
> Keep the final decision human.

---

## 1. What Model 1 is

Model 1 v1.0 is a minimal stop-loss guardrail for judgment.

It helps with questions like:

- Should I pause before acting?
- Is the next step reversible?
- Do I have enough verified information?
- What is fact, inference, and unknown?
- Does the present evidence support, oppose, or fail to resolve the proposed path?
- Am I crossing a boundary?
- Is the cost rising faster than the clarity?
- Am I asking an AI system to decide something that I should decide myself?

Model 1 does not give a command. It gives bounded review outputs.

The final decision stays with the human user.

---

## 2. What Model 1 is not

Model 1 is not:

- a prediction tool for other people;
- a profiling system;
- a persuasion or manipulation guide;
- an automated decision engine;
- therapy, counseling, medical advice, legal advice, financial advice, or investment advice;
- a replacement for professional judgment;
- a system for outsourcing responsibility to AI.

It should not be used to label, pressure, diagnose, rank, or control another person.

---

## 3. The basic idea

Before taking a consequential action, ask:

1. **What is the next action?**  
   Write the action in plain language.

2. **What is fact, inference, and unknown?**  
   Do not let a confident explanation replace verification.

3. **What could go wrong if I continue?**  
   Look for cost, boundary crossing, missing evidence, or loss of reversibility.

4. **Can I still stop or roll back?**  
   If the answer is unclear, slow down before continuing.

The goal is not to find a perfect answer. The goal is to prevent avoidable escalation and false certainty.

---

## 4. Evidence direction: `+ / 0 / -`

Use a bounded direction for the proposed action:

- `+` — current evidence supports the path;
- `0` — evidence is insufficient, mixed, or unresolved;
- `-` — current evidence opposes the path.

`0` is a valid result. Unknown is not failure and should not be disguised as approval or rejection.

A direction describes the evidence. It does not authorize action.

---

## 5. The three risk signals

### 🟢 Green

No stop-loss trigger is currently visible from the stated input.

This does not guarantee that the action is correct.

### 🟡 Yellow

Risk, ambiguity, cost, or uncertainty is rising.

Slow down, check sources, clarify the boundary, and preserve options.

### 🔴 Red

A hard boundary, irreversible cost, or serious validation gap is present.

Freezing or exiting may be reasonable. The human user makes the final decision.

A signal is a review prompt, not a command or authorization.

---

## 6. Direction and signal are different

The two outputs answer different questions:

- `+ / 0 / -` asks what the evidence currently says about the path;
- Green / Yellow / Red asks how strongly the person should pause before acting.

A path may be supported by some evidence but still receive Yellow because it is difficult to reverse. Evidence may remain unresolved while a mandatory validation gap requires Red.

---

## 7. Human Final Gate

AI may help organize information, identify possible risk signals, and ask better questions.

AI must not become the final decision-maker.

> If the action has real-world consequences, the final decision cannot be outsourced to AI.

---

## 8. Source discipline

Before acting, check:

- What do I actually know?
- What is inferred?
- What is assumed?
- What has been verified from a real source?
- What is still unclear?
- What would change my decision?

Do not treat fluency, confidence, repetition, or formatting as verified evidence.

---

## 9. Gray analysis and hard boundaries

Use nuance when the evidence is partial or mixed. Do not turn one defect into a total judgment or one successful result into proof of repeatable operation.

But nuance stops where a hard rule controls, such as:

- safety;
- authorization;
- contract or specification facts;
- privacy or consent;
- required validation;
- a non-negotiable personal limit.

Complexity must not be used to wash away responsibility.

---

## 10. A simple beginner workflow

1. Write the proposed next action.
2. Check whether it has real-world consequences.
3. Separate fact, inference, and unknown.
4. Assign an evidence direction: `+ / 0 / -`.
5. Check consequence, boundary, and reversibility.
6. Assign a Green, Yellow, or Red risk signal.
7. State what evidence would reverse the conclusion.
8. Apply the Human Final Gate.
9. Proceed, slow down, freeze, or exit through human judgment.

For the detailed public language interface, see [`docs/02-judgment-language.md`](02-judgment-language.md).

---

## 11. Practice with public examples

After learning the basic workflow, review the public-safe composite cases:

1. [`examples/01-source-drift-procurement.md`](../examples/01-source-drift-procurement.md)  
   Unresolved evidence direction, source conflict, master-data risk, and reversible approval design.

2. [`examples/02-unverified-change-release.md`](../examples/02-unverified-change-release.md)  
   Evidence opposing release, validation gaps, escalation, and the Human Final Gate.

These examples are composite and anonymized. They demonstrate the public method without reproducing private records or complete private-engine logic.

---

## 12. Public/private boundary

This public repository contains only the beginner-safe scaffold.

It may include:

- beginner guides;
- public-safe definitions;
- composite examples;
- boundary notes;
- decision gates;
- evidence-direction and signal vocabulary.

It does not include:

- private cases;
- identifiable personal material;
- private calibration chains or thresholds;
- observer packs, market-extraction maps, or anti-poisoning implementation internals;
- sensitive judgment records;
- relationship, family, medical, workplace, or financial details;
- complete private-engine logic;
- hidden runtime packs or executable decision systems.

The public layer demonstrates the method without transferring the private core.

---

## 13. How to read this repository

A beginner may read the repository in this order:

1. [`README.md`](../README.md)
2. [`docs/00-start-here.md`](00-start-here.md)
3. [`docs/01-basic-principles.md`](01-basic-principles.md)
4. [`docs/02-judgment-language.md`](02-judgment-language.md)
5. [`examples/README.md`](../examples/README.md)
6. [`ARCHITECTURE.md`](../ARCHITECTURE.md)
7. [`SAFETY.md`](../SAFETY.md)
8. [`GLOSSARY.md`](../GLOSSARY.md)

---

## 14. Core rule

Model 1 is not here to make the decision for you.

It is here to help you notice when the next step deserves a pause.

> Check the action.  
> Separate fact, inference, and unknown.  
> Check the boundary and reversibility.  
> Keep the final gate human.
