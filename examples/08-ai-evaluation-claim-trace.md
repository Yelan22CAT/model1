# Showcase Case 8 — AI Recommendation With Broken Claim Trace

> Public-safe composite case. This is not a transcript of a single model, company, dataset, or production decision.

## Situation

An AI-assisted review produces a concise recommendation for management. The summary appears coherent and cites several source documents. During review, one important statement cannot be traced to the cited material, one source is outdated, and a generated comparison blends facts with inferred conclusions.

## Proposed consequential action

Use the AI-generated recommendation as the basis for approval without reopening the supporting claims.

## Known facts

- the recommendation was generated from multiple sources;
- some claims are traceable to current evidence;
- one decision-changing claim lacks direct support;
- one cited source is outdated;
- fact and inference are mixed in at least one comparison;
- the proposed decision has operational consequences.

## Claim-state table

| Claim | Source state | Current status |
| --- | --- | --- |
| Current process has documented approval | current authoritative source | verified |
| Proposed change reduces operating risk | mixed source and inference | unverified |
| Vendor evidence satisfies the new requirement | outdated source | stale |
| No material exception remains | no supporting source located | unsupported |

## Control gaps

- no claim-level trace for decision-changing statements;
- stale evidence not distinguished from current evidence;
- generated inference presented with factual wording;
- no explicit unknown state;
- no reversal condition;
- management-ready fluency treated as evidence quality.

## Evidence direction

**Direction: `0` — unresolved**

Some supporting evidence is valid, but the recommendation as a whole is not sufficiently grounded for approval.

## Risk signal

**Signal: 🔴 Red**

A consequential decision would rely on unsupported and stale claims.

## Recommended control response

1. freeze approval;
2. break the recommendation into atomic claims;
3. label each claim as verified, inferred, stale, unsupported, or unknown;
4. replace stale sources or state the limitation;
5. remove or qualify unsupported conclusions;
6. identify which claims are decision-changing;
7. define what evidence would reverse the current conclusion;
8. return the corrected brief to the accountable human owner.

## Reversal condition

The conclusion may change when:

- every decision-changing claim has a current and relevant source;
- inference is clearly labeled;
- stale evidence is replaced or formally accepted as a limitation;
- unsupported claims are removed;
- the final owner reviews consequence, uncertainty, and rollback.

## Compact management output

```text
Decision required: approve the recommendation
Current state: partially grounded, not approval-ready
Primary issue: broken claim trace on decision-changing statements
Immediate control: atomic claim review and source refresh
Residual uncertainty: expected impact remains partly inferred
Human Final Gate: accountable management owner
```

## Capability demonstrated

- AI output evaluation;
- claim-level source trace;
- stale-source detection;
- fact/inference separation;
- uncertainty preservation;
- Human Final Gate design.

## Public boundary

This case omits real models, prompts, datasets, organizations, management decisions, and internal documents. It demonstrates an evaluation pattern rather than a production AI system.