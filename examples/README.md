# Public Showcase Cases

These public-safe composite cases demonstrate how Model 1 structures operational uncertainty without publishing private records or proprietary reasoning assets.

## Cases

1. [`01-source-drift-procurement.md`](01-source-drift-procurement.md) — source-of-truth conflict, procurement risk, and reversible approval.
2. [`02-unverified-change-release.md`](02-unverified-change-release.md) — incomplete validation, release control, escalation, and rollback.
3. [`03-near-miss-escalation.md`](03-near-miss-escalation.md) — evidence preservation, containment, restart governance, and closure.
4. [`04-vendor-onboarding-control-gap.md`](04-vendor-onboarding-control-gap.md) — proportional vendor intake, conditions, exceptions, and initial monitoring.
5. [`05-ai-generated-summary-before-approval.md`](05-ai-generated-summary-before-approval.md) — AI claim drift, source traceability, and human approval.
6. [`06-critical-dependency-recovery.md`](06-critical-dependency-recovery.md) — critical dependency failure, temporary containment, fallback, recovery ownership, and restart criteria.
7. [`07-vendor-monitoring-trigger.md`](07-vendor-monitoring-trigger.md) — material-change detection, stale onboarding evidence, access expansion, and triggered reassessment.
8. [`08-ai-evaluation-claim-trace.md`](08-ai-evaluation-claim-trace.md) — atomic claim review, stale-source detection, broken traceability, and consequential-use gating.
9. [`09-control-effectiveness-drift.md`](09-control-effectiveness-drift.md) — prior assurance after process change, evidence currency, and targeted control reassessment.
10. [`10-local-ai-hidden-cloud-dependency.md`](10-local-ai-hidden-cloud-dependency.md) — local-vs-offline distinction, unverified data egress, cloud dependency, and deployment approval.
11. [`11-metric-decision-objective-mismatch.md`](11-metric-decision-objective-mismatch.md) — metric usefulness vs decision-objective alignment, exceptions, and model-authority limits.

## Domain coverage

| Case | Domain | Main control question |
| --- | --- | --- |
| 1 | procurement / master data | Is the source of truth reliable enough to approve the order? |
| 2 | technical operations / change control | Has the full operating condition been validated before release? |
| 3 | operational risk / safety governance | Is the process sufficiently contained and controlled to restart? |
| 4 | vendor / third-party risk | Is evidence sufficient for the proposed dependency and access? |
| 5 | AI governance / decision support | Can the generated brief be traced and trusted for consequential use? |
| 6 | operational resilience | Is this restored capability or only temporary containment? |
| 7 | continuous third-party monitoring | Has a material change invalidated the original assessment? |
| 8 | AI evaluation | Are decision-changing claims current, supported, and clearly separated from inference? |
| 9 | risk & controls / GRC | Does the prior control assessment still describe the current process state? |
| 10 | AI / technology risk | Does “local” actually describe the full approved data and network boundary? |
| 11 | AI / model risk | Does the metric rank outcomes in a way that matches the actual decision objective? |

## Common review structure

Each case uses:

- proposed consequential action;
- known facts;
- assumptions, inferences, stale evidence, and unknowns;
- control gaps and ownership;
- consequence and reversibility;
- evidence direction: `+ / 0 / -`;
- Green / Yellow / Red risk signal;
- compact management output;
- reversal and closure conditions;
- Human Final Gate;
- public boundary.

```text
Direction = what the current evidence says about the proposed path
Signal = how strongly action should pause before proceeding
```

The newer cases also demonstrate two public extensions around the stable core:

```text
Material change → refresh affected evidence
Deployment or model label → verify the actual operating boundary
Metric performance → verify alignment with the real decision objective
```

## Supporting portfolio material

- [`../ROLE_EVIDENCE_MATRIX.md`](../ROLE_EVIDENCE_MATRIX.md)
- [`../WORK_SAMPLES.md`](../WORK_SAMPLES.md)
- [`../methods/01-operational-risk-review.md`](../methods/01-operational-risk-review.md)
- [`../methods/02-third-party-risk-intake.md`](../methods/02-third-party-risk-intake.md)
- [`../methods/03-ai-assisted-evidence-review.md`](../methods/03-ai-assisted-evidence-review.md)
- [`../methods/04-change-triggered-reassessment.md`](../methods/04-change-triggered-reassessment.md)
- [`../templates/CHANGE_REASSESSMENT_RECORD.md`](../templates/CHANGE_REASSESSMENT_RECORD.md)
- [`../samples/MANAGEMENT_DECISION_MEMO.md`](../samples/MANAGEMENT_DECISION_MEMO.md)

These cases do not disclose real identities, organizations, incident records, private calibration logic, observer packs, anti-poisoning internals, or proprietary technical information.