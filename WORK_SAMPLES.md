# Public Work Samples

This page collects the strongest employer-facing artifacts in the repository.

The samples are not transcripts of a single workplace, employer, person, incident, or vendor. They are public-safe composites designed to show how I structure ambiguous operational problems.

## What an employer can assess here

A reviewer can evaluate whether I can:

- identify the real decision under review;
- separate facts, assumptions, and unknowns;
- distinguish missing evidence from evidence against a path;
- identify control gaps and accountable owners;
- connect technical conditions to business and operational consequences;
- preserve rollback, containment, and recovery options;
- write concise escalation and decision-support material;
- use AI without transferring final authority to AI.

## Case portfolio

| Case | Primary domain | Main capability shown |
| --- | --- | --- |
| [Source Drift in a Procurement Decision](examples/01-source-drift-procurement.md) | procurement / master data | source-of-truth review, reversible approval |
| [Unverified Change Before Release](examples/02-unverified-change-release.md) | technical operations / change control | validation gate, release control, escalation |
| [Near-Miss Escalation Without a Complete Incident Record](examples/03-near-miss-escalation.md) | operational risk / safety governance | fact discipline, immediate containment, escalation |
| [Vendor Onboarding With Missing Control Evidence](examples/04-vendor-onboarding-control-gap.md) | TPRM / vendor risk | evidence request, conditional approval, exception ownership |
| [AI-Generated Summary Before Management Approval](examples/05-ai-generated-summary-before-approval.md) | AI governance / decision support | claim verification, source trace, Human Final Gate |

## Method samples

| Method | Purpose |
| --- | --- |
| [Operational Risk Review](methods/01-operational-risk-review.md) | convert an operating concern into a bounded risk and control review |
| [Third-Party Risk Intake](methods/02-third-party-risk-intake.md) | perform proportional vendor intake without reducing review to a checklist |
| [AI-Assisted Evidence Review](methods/03-ai-assisted-evidence-review.md) | use AI for organization and comparison while preserving source authority and human accountability |

## Template samples

| Template | Output produced |
| --- | --- |
| [Risk Review Template](templates/RISK_REVIEW_TEMPLATE.md) | concise risk assessment with evidence direction, control gap, and next action |
| [Control Gap Log](templates/CONTROL_GAP_LOG.md) | structured register of expected control, observed condition, owner, and remediation status |
| [Escalation Brief](templates/ESCALATION_BRIEF_TEMPLATE.md) | short management-ready issue summary with decision required |

## How the samples fit together

```text
Operating observation
→ Risk Review Template
→ Control gap identified
→ Control Gap Log
→ Decision or ownership needed
→ Escalation Brief
→ Human-owned approval, containment, remediation, or closure
```

For vendor work:

```text
Service dependency
→ Third-Party Risk Intake
→ Evidence request
→ Control assessment
→ Approval / conditional approval / rejection / exception
→ Ongoing review trigger
```

For AI-assisted work:

```text
Source material
→ AI organizes claims
→ Human checks source state
→ Unsupported claims are removed or marked unknown
→ Consequence and reversibility are reviewed
→ Human Final Gate
```

## Review standard used across all samples

Each sample follows a common sequence:

1. define the proposed consequential action;
2. state what is known;
3. state what is assumed or unknown;
4. identify evidence direction: `+ / 0 / -`;
5. identify control, ownership, consequence, and reversibility;
6. assign a Green / Yellow / Red review signal;
7. state what would reverse the conclusion;
8. recommend one safe and reversible next action;
9. preserve the Human Final Gate.

## Boundary

The samples intentionally omit:

- real names and organizations;
- exact incident dates and private records;
- proprietary drawings, specifications, quantities, or systems;
- private thresholds and calibration chains;
- private observer packs;
- autonomous execution logic;
- complete private-engine structure.

The goal is to make the capability visible without transferring private source material or an unrestricted decision engine.