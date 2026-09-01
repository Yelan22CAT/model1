# Case 11 — Metric / Decision-Objective Mismatch in an AI-Assisted Workflow

## Situation

An AI-assisted triage workflow ranks items using a score that was originally designed to improve speed and throughput.

A later use case asks the same score to support a higher-consequence prioritization decision where severity, downstream impact, and reversibility also matter.

The score may be technically consistent and still be misaligned with the new decision objective.

## Proposed consequential action

Use the existing score as the primary basis for high-consequence prioritization without validating whether the metric preserves the decision priorities that now matter.

## Known facts

- the score has an established relationship with the original operational objective;
- the proposed use changes the decision being made;
- the new decision includes consequences not represented explicitly in the original score;
- no current evidence shows that score ordering preserves the same ordering for severity or downstream impact;
- the workflow still has a human review point available.

## Inferences and unknowns

### Inference

The existing score may remain useful as one input.

### Unknowns

- whether high-severity items can receive a low operational score;
- whether optimizing the score creates systematic blind spots;
- whether the ranking remains stable under changed conditions;
- whether users understand what the score does and does not measure;
- whether exceptions are surfaced before action.

## Key distinction

```text
Predictive or operational metric
≠ decision objective
```

A metric can be accurate for what it measures and still be insufficient for the decision being made.

The question is not only:

> Is the score predictive?

It is also:

> Does the score rank outcomes in a way that matches the consequence-sensitive decision objective?

## Risk and control decomposition

| Element | Review |
| --- | --- |
| Original metric objective | known |
| New decision objective | broader and more consequential |
| Metric-to-decision alignment | not established |
| Exception handling | requires explicit review |
| Human override | available |
| Consequence | important items may be deprioritized for the wrong reason |
| Reversibility | depends on how quickly a missed priority can be detected and corrected |

## Evidence direction

**`0` — unresolved.**

The metric may be useful, but current evidence does not support treating it as a complete decision rule for the new use case.

## Risk signal

**Yellow — preserve the score as an input, but validate decision alignment before expanding authority.**

If the workflow would remove human review or automatically execute high-consequence actions, the signal should be escalated.

## Control response

1. define the actual decision objective in operational language;
2. identify what the existing score measures;
3. identify important consequences not represented by the score;
4. test whether ranking by the score preserves decision-relevant ordering;
5. define exception conditions and human review;
6. monitor for cases where metric success conflicts with decision quality;
7. keep model output advisory until alignment is demonstrated.

## Compact decision-support output

**Decision required:** Can the existing AI score become the primary prioritization rule for the new use case?

**Conclusion:** Not yet. Metric usefulness is established for the old objective, not for the expanded decision objective.

**Decisive evidence:** The use case changed while the metric definition did not.

**Unknowns:** Decision-ordering quality, severity blind spots, and exception behavior.

**Evidence direction:** `0`

**Risk signal:** Yellow

**Control gap:** No demonstrated alignment between the score and the new consequence-sensitive decision objective.

**Reversal condition:** Evaluation shows that the score, together with explicit exceptions, reliably preserves the ordering required by the new decision.

**Safe next action:** Run a bounded retrospective or shadow review comparing metric ranking with human-owned decision criteria.

**Human Final Gate:** The accountable process or risk owner approves any expansion of model authority.

## Employer-facing capability demonstrated

- AI evaluation beyond headline accuracy;
- metric-goal alignment review;
- model-risk and decision-risk separation;
- exception and override design;
- consequential-use gating;
- human-in-the-loop control.

## Public boundary

This is a generalized composite case. It does not publish private model objectives, thresholds, training data, scoring formulas, or internal evaluation records.