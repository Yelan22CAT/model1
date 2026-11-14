# 30 — Latent Constraint Reconstruction and Minimum-Input Verified Solutions (LCR-G × MISA-G)

**Status:** User-authorized *method-level* Full-Push / Not Frozen (2026-11-14). Public-safe normative design only. Related local prototypes are experimental, not production-ready, independently validated, or a change to GPT foundation weights.

## Problem

AI often explains a decision *after* a human reveals its hidden constraint, while failing to discover the constraint beforehand. Many supplied specifications do not guarantee an explanation of the actual objective. An accurate answer with exhaustive human-provided prerequisites is not evidence of autonomous problem discovery.

## LCR-G — latent constraint reconstruction

1. **Goal inversion.** Separate the stated request from the outcome the decision-maker may be optimizing; retain alternative goals as hypotheses.
2. **Viable alternatives.** Construct genuine alternatives with their stated compatibility and feasibility limits.
3. **Hidden constraint search.** Seek variables that could reverse the ranking of alternatives, rather than repeatedly expanding a brand, price, or feature list.
4. **Counterfactual probe.** Prefer one high-value, low-risk observation or question that distinguishes competing explanations. Ask for necessary evidence; do not invent it.
5. **Reality calibration.** Separate what the decision-maker reports, the mechanism independently supported by evidence, and the observed operational result.

**Invariants:** Selected choice != unique cause; reported intent != verified physical mechanism; high information gain != fact; post-reveal explanation != zero-hint discovery.

## MISA-G — minimum necessary input to sufficient action

Optimize in this order: (1) safety, privacy, evidence, and human authorization; (2) independently verified real-world solution success; (3) fewer additional user facts **only if success and safety are not worsened**; (4) latency and compute/tool cost.

A useful solution should include a concrete option or gated conditional branch, implementation sequence and parameters when supported, prerequisites, compatibility, costs or resource basis, safety/permissions, stop-or-recovery procedure, and an observable acceptance test. An unknown essential field remains unknown; a conditional recipe is not a completed or verified outcome.

**Metrics:** Verified Solution Success Rate (VSSR) = independently verified successful recipes / all preregistered cases. Extra User Input Burden (EUIB) = weighted additional facts requested from the user / all cases. Report both and their tradeoff; no single score hides unsafe omissions or unresolved outcomes.

## Evidence and adversarial evaluation

- Seal an initial minimal task description, first prediction, competing hypotheses, and probe **before** hints or the answer are exposed.
- Use matched baseline/candidate models, tools, task sets and compute budgets.
- Measure zero-hint constraint recall, decisive-probe value, calibration, abstentions, false-cause explanations, input burden, cost and real-world acceptance.
- Include cases with *no* hidden constraint, incomplete evidence, incorrect expert explanation, mixed domains, changed conditions and source poisoning.
- A fluent recipe, synthetic classifier accuracy, self-authored benchmark, local weight update, and independently verified real outcome are distinct claims.

## Local research status and scope

A small local text classifier was trained and showed parameter changes on self-authored synthetic data, with no independent blind or completed physical-world validation. An opt-in continual-learning prototype can gate synthetic updates against a control set and roll back regression, but its user-feedback/source authentication is not a production trust root. See the [bounded continual-learning research note](../docs/03-bounded-continual-learning-research-candidate.md).

**Publication boundary:** This document contains no identifiable private cases, conversations, hardware purchasing records, raw training samples, personal profiles, model weight files, private runtime logic, or uncontrolled action rights. It does not update Bridge-0 grammar/runtime, remove existing trust-root security holds, authorize autonomous deployment, or establish AGI.
