# Public Work Samples

This page collects the strongest employer-facing artifacts in the repository.

The samples are not transcripts of a single workplace, employer, person, incident, vendor, or AI system. They are public-safe composites designed to show how I structure ambiguous operational problems.

## What an employer can assess here

A reviewer can evaluate whether I can:

- identify the real decision under review;
- separate facts, assumptions, inferences, stale evidence, and unknowns;
- distinguish missing evidence from evidence against a path;
- identify control gaps and accountable owners;
- connect technical conditions to business and operational consequences;
- preserve rollback, containment, recovery, and monitoring options;
- recognize when a material change invalidates prior assurance;
- distinguish product or deployment labels from verified operating boundaries;
- test whether a metric is aligned with the actual decision objective;
- write concise escalation and decision-support material;
- use AI without transferring final authority to AI.

For a direct role-to-proof view, see [`ROLE_EVIDENCE_MATRIX.md`](ROLE_EVIDENCE_MATRIX.md).

## Case portfolio

| Case | Primary domain | Main capability shown |
| --- | --- | --- |
| [Source Drift in a Procurement Decision](examples/01-source-drift-procurement.md) | procurement / master data | source-of-truth review, reversible approval |
| [Unverified Change Before Release](examples/02-unverified-change-release.md) | technical operations / change control | validation gate, release control, escalation |
| [Near-Miss Escalation Without a Complete Incident Record](examples/03-near-miss-escalation.md) | operational risk / safety governance | fact discipline, immediate containment, escalation |
| [Vendor Onboarding With Missing Control Evidence](examples/04-vendor-onboarding-control-gap.md) | TPRM / vendor risk | evidence request, conditional approval, exception ownership |
| [AI-Generated Summary Before Management Approval](examples/05-ai-generated-summary-before-approval.md) | AI governance / decision support | claim verification, source trace, Human Final Gate |
| [Critical Dependency Failure and Recovery Decision](examples/06-critical-dependency-recovery.md) | operational resilience | dependency mapping, containment, fallback, restart criteria |
| [Vendor Monitoring Trigger After Onboarding](examples/07-vendor-monitoring-trigger.md) | TPRM / continuous monitoring | material-change trigger, stale evidence, reassessment |
| [AI Recommendation With Broken Claim Trace](examples/08-ai-evaluation-claim-trace.md) | AI evaluation / governance | atomic claims, stale-source detection, grounding review |
| [Control Effectiveness Drift After a Process Change](examples/09-control-effectiveness-drift.md) | risk & controls / GRC | temporal validity, targeted retesting, current-state assurance |
| [“Local” AI With an Unverified Cloud Dependency](examples/10-local-ai-hidden-cloud-dependency.md) | AI governance / deployment risk | system-boundary review, data-egress uncertainty, approval gating |
| [Metric / Decision-Objective Mismatch](examples/11-metric-decision-objective-mismatch.md) | AI evaluation / model risk | metric-goal alignment, exception design, authority limits |

## Method samples

| Method | Purpose |
| --- | --- |
| [Operational Risk Review](methods/01-operational-risk-review.md) | convert an operating concern into a bounded risk and control review |
| [Third-Party Risk Intake](methods/02-third-party-risk-intake.md) | perform proportional vendor intake without reducing review to a checklist |
| [AI-Assisted Evidence Review](methods/03-ai-assisted-evidence-review.md) | use AI for organization and comparison while preserving source authority and human accountability |
| [Change-Triggered Reassessment](methods/04-change-triggered-reassessment.md) | refresh only the evidence affected when a material change makes prior assurance potentially stale |

## Work-product samples

| Artifact | Output produced |
| --- | --- |
| [Risk Review Template](templates/RISK_REVIEW_TEMPLATE.md) | concise risk assessment with evidence direction, control gap, and next action |
| [Control Gap Log](templates/CONTROL_GAP_LOG.md) | register of expected control, observed condition, owner, and remediation status |
| [Escalation Brief](templates/ESCALATION_BRIEF_TEMPLATE.md) | management-ready issue summary with decision required |
| [Change Reassessment Record](templates/CHANGE_REASSESSMENT_RECORD.md) | prior decision, material-change trigger, stale evidence, targeted refresh, and closure record |
| [Management Decision Memo](samples/MANAGEMENT_DECISION_MEMO.md) | one-page options, recommendation, reversal condition, and Human Final Gate |

## How the samples fit together

```text
Operating observation
→ Risk Review
→ Control gap identified
→ Control Gap Log
→ Material change?
   → if yes: Change Reassessment Record
→ Decision or ownership needed
→ Escalation Brief / Decision Memo
→ Human-owned approval, containment, remediation, monitoring, reassessment, or closure
```

For vendor work:

```text
Service dependency
→ Third-Party Risk Intake
→ Evidence request
→ Approval / condition / exception
→ Material-change trigger
→ Reassessment and ongoing monitoring
```

For AI-assisted work:

```text
Source material / model output / deployment claim
→ Human checks claim trace, source state, and operating boundary
→ Unsupported or stale claims are removed, refreshed, or marked unknown
→ Metric and decision objective are checked for alignment when relevant
→ Consequence and reversibility are reviewed
→ Human Final Gate
```

## Review standard used across all samples

Each sample follows a common sequence:

1. define the proposed consequential action;
2. state what is known;
3. state what is assumed, inferred, stale, or unknown;
4. identify evidence direction: `+ / 0 / -`;
5. identify control, ownership, consequence, and reversibility;
6. check whether prior evidence still describes the current state;
7. assign a Green / Yellow / Red review signal;
8. state what would reverse the conclusion;
9. recommend one safe and reversible next action;
10. preserve the Human Final Gate.

## Boundary

The samples intentionally omit real names, organizations, private records, proprietary specifications, private thresholds, calibration chains, observer packs, autonomous execution logic, and complete private-engine structure.

The goal is to make the capability visible without transferring private source material or an unrestricted decision engine.