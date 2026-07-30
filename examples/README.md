# Public Showcase Cases

These cases demonstrate how Model 1 structures operational uncertainty without publishing private records or proprietary reasoning assets.

They are public-safe composites. They are not transcripts of single real events.

## Cases

1. [`01-source-drift-procurement.md`](01-source-drift-procurement.md) — conflicting source records, unresolved evidence direction, procurement risk, evidence reconciliation, and reversible approval design.
2. [`02-unverified-change-release.md`](02-unverified-change-release.md) — incomplete technical validation, evidence opposing release, escalation, rollback, and the Human Final Gate.
3. [`03-near-miss-escalation.md`](03-near-miss-escalation.md) — operational-risk escalation, evidence preservation, containment, restart governance, and closure conditions.
4. [`04-vendor-onboarding-control-gap.md`](04-vendor-onboarding-control-gap.md) — proportional third-party risk intake, evidence-state review, conditional approval, exception control, and ongoing monitoring.
5. [`05-ai-generated-summary-before-approval.md`](05-ai-generated-summary-before-approval.md) — AI claim drift, source hierarchy, traceability, consequential-use gating, and accountable human approval.

## Domain coverage

| Case | Domain | Main control question |
| --- | --- | --- |
| 1 | procurement / master data | Is the current source of truth reliable enough to approve the order? |
| 2 | technical operations / change control | Has the full operating condition been validated before release? |
| 3 | operational risk / safety governance | Is the process safe and controlled enough to restart? |
| 4 | vendor / third-party risk | Is the evidence sufficient for the proposed dependency and access? |
| 5 | AI governance / decision support | Can the AI-generated brief be traced and trusted for consequential use? |

## What to look for

Each case follows the same visible structure:

- situation;
- proposed next action;
- known facts;
- assumptions and unknowns;
- risk and control decomposition;
- consequence and reversibility;
- evidence direction: `+ / 0 / -`;
- Green / Yellow / Red risk signal;
- compact decision-support output;
- recommended control response;
- reversal and closure conditions;
- Human Final Gate;
- public boundary.

Evidence direction and risk signal are intentionally separate:

```text
Direction = what the current evidence says about the proposed path
Signal = how strongly the person should pause before acting
```

## Supporting methods and templates

- [`../methods/01-operational-risk-review.md`](../methods/01-operational-risk-review.md)
- [`../methods/02-third-party-risk-intake.md`](../methods/02-third-party-risk-intake.md)
- [`../methods/03-ai-assisted-evidence-review.md`](../methods/03-ai-assisted-evidence-review.md)
- [`../templates/RISK_REVIEW_TEMPLATE.md`](../templates/RISK_REVIEW_TEMPLATE.md)
- [`../templates/CONTROL_GAP_LOG.md`](../templates/CONTROL_GAP_LOG.md)
- [`../templates/ESCALATION_BRIEF_TEMPLATE.md`](../templates/ESCALATION_BRIEF_TEMPLATE.md)

The examples demonstrate the interface and reasoning discipline. They do not disclose complete private calibration logic, real identities, organizations, internal records, observer packs, anti-poisoning internals, or proprietary technical details.

For the full employer-facing work-sample path, see [`../WORK_SAMPLES.md`](../WORK_SAMPLES.md).