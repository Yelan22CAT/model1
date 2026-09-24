# 13 — Cross-Model Evidence Reconciliation and Explanation Audit

## Purpose

Use multiple AI models as independent analytical probes without mistaking agreement for independent evidence or disagreement for failure.

## Blind-first sequence

```text
User hypothesis / problem
→ shared evidence boundary
→ independent model passes
→ delta extraction
→ source adjudication
→ adversarial recheck
→ Human Final
```

Each pass should separate observed fact, inference, alternative explanation, missing evidence, and conclusion boundary.

## Agreement rule

```text
Two models agree
≠ two independent factual confirmations
```

Agreement may support structural robustness, but factual promotion still requires source and reality checks.

## Disagreement rule

Classify the disagreement before choosing a side: fact, definition, scope, model/version/tool, policy/safety, inference, or value framing.

## Explanation-layer audit

```text
Observation
≠ Interpretation
≠ Causal Story
```

Conclusion convergence does not imply explanation convergence. When primary documentation conflicts, preserve the inconsistency rather than inventing a harmonizing story.

## Boundary

This method does not rank providers or treat model consensus as truth.
