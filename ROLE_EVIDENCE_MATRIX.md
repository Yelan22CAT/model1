# Role Evidence Matrix

This page maps target role families to visible evidence in the public portfolio.

The purpose is not to claim experience that is not demonstrated. It is to show how hands-on technical operations, troubleshooting, issue escalation, and structured judgment transfer into risk, governance, resilience, and AI-assisted decision-support work.

## Evidence standard

Each capability should be supported by at least one of the following:

- a composite case showing the reasoning in context;
- a reusable method showing the review sequence;
- a template showing the expected work product;
- an architecture or safety document showing the control boundary.

## Role-to-evidence map

| Role family | Typical responsibility | Demonstrated capability | Public evidence |
| --- | --- | --- | --- |
| Operational Risk Analyst | identify process failure, consequence, owner, and control response | bounded risk review, consequence analysis, escalation, rollback, reassessment after change | Cases 2, 3, 6, 9; Methods 1 and 4; Risk Review Template |
| Risk & Controls Analyst | test whether a stated control exists and works in the current process state | expected-control vs observed-condition comparison, gap logging, temporal validity, targeted retesting | Cases 4, 7, 9; Control Gap Log; Change Reassessment Record |
| Operational Resilience Analyst | assess critical dependencies and recovery conditions | dependency mapping, containment, fallback, restart criteria, residual risk | Case 6; Method 1; Decision Memo Sample |
| GRC Analyst | translate policy intent into reviewable evidence and exceptions | evidence-state discipline, exception ownership, control currency, concise decision records | Cases 3, 4, 9; Methods 1, 2, and 4; Escalation Brief |
| Vendor / Third-Party Risk Analyst | review vendor access, dependency, evidence, exceptions, and monitoring | proportional intake, missing-vs-failed evidence, conditional approval, material-change triggers | Cases 4 and 7; Methods 2 and 4 |
| Change / Release Governance Analyst | prevent unverified or materially changed conditions from entering production or field use | validation gate, release hold, accountable sign-off, rollback readiness, post-change reassessment | Cases 2 and 9; Methods 1 and 4 |
| AI Governance / Evaluation Analyst | assess whether AI output and deployment behavior are sufficiently grounded for consequential use | claim-level verification, deployment-boundary review, metric-goal alignment, uncertainty preservation, Human Final Gate | Cases 5, 8, 10, and 11; Method 3; Safety |
| AI / Model Risk Analyst | identify when technical performance evidence does not support the actual decision use | metric-to-objective alignment, consequence-sensitive exception design, limits on model authority | Cases 8 and 11; Method 3; Judgment Language |
| AI-Assisted Decision Support Analyst | turn mixed information into a compact, reviewable decision brief | fact/inference/unknown separation, two-axis output, reversal condition, safe next action, current-state check | Judgment Language; Cases 5, 8, 11; Decision Memo Sample |
| Technology / AI Risk Analyst | assess system boundaries, dependencies, data paths, and consequential deployment conditions | local-vs-offline distinction, unresolved egress review, fallback and dependency analysis | Case 10; Methods 2 and 4; Safety |
| Technical Operations Analyst | connect technical observations to operational and business consequences | troubleshooting decomposition, issue ownership, escalation, recovery thinking, change awareness | Cases 1, 2, 3, 6, and 9 |

## What this matrix shows

A reviewer should be able to trace the same operating discipline across domains:

```text
Observe the operating condition
→ separate fact, inference, stale evidence, and unknown
→ identify the consequential decision
→ test the control, dependency, and evidence state
→ check whether prior assurance still describes the current state
→ assess consequence and reversibility
→ define containment, escalation, rollback, monitoring, or reassessment
→ preserve an accountable Human Final Gate
```

## What this matrix does not claim

It does not claim:

- formal authority to certify compliance;
- production ownership of an enterprise GRC platform;
- licensed engineering, legal, privacy, security, or regulatory judgment;
- autonomous AI decision authority;
- disclosure of private employers, incidents, vendors, or source records.

It is an evidence map for transferable capability, not an inflation of title or authority.