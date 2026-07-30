# Portfolio Map — From Technical Operations to Risk and AI-Assisted Decision Support

## Positioning

My background is rooted in manufacturing operations, field service support, assembly, troubleshooting, inventory checks, issue escalation, and practical work in high-variance environments.

This portfolio shows how that operating experience can be translated into structured work in:

- operational risk and controls;
- operational resilience;
- governance, risk, and compliance;
- vendor and third-party risk;
- change and release governance;
- AI-assisted decision support;
- AI governance, evaluation, and safety operations.

The common thread is not a change from “technical” work to unrelated office work. It is a move from solving individual operating problems to designing repeatable ways to identify, communicate, and control risk.

## Transfer path

```text
Hands-on operations and field troubleshooting
→ recognize failure conditions and incomplete information
→ separate observation, assumption, and unknown
→ identify consequence, ownership, and reversibility
→ design pause, escalation, validation, and rollback controls
→ support operational risk, GRC, TPRM, resilience, and AI-governance work
```

## Capability map

| Operating capability | Risk and governance translation | Evidence in this repository |
| --- | --- | --- |
| Troubleshooting under uncertainty | issue decomposition and evidence-state review | `docs/02-judgment-language.md`, Case 2, Case 3 |
| Reading conflicting records and field conditions | source-of-truth and data-quality control | Case 1 |
| Recognizing unsafe or incomplete release conditions | validation gate and escalation design | Case 2, Case 3 |
| Working across technical and non-technical owners | responsibility mapping and concise escalation | `templates/ESCALATION_BRIEF_TEMPLATE.md` |
| Inventory, parts, suppliers, and documentation | vendor intake and third-party control thinking | Case 4, Method 2 |
| AI-assisted analysis | source-state separation and Human Final Gate | Case 5, Method 3 |
| Preserving a stop or rollback path | operational resilience and reversibility analysis | `ARCHITECTURE.md`, Method 1 |
| Turning repeated problems into a framework | control design and reusable documentation | this repository as a whole |

## Role alignment

### Operational Risk / Risk & Controls

Relevant demonstrated work:

- define the consequential action under review;
- identify the failure mode and affected process;
- distinguish observed fact, inference, and unknown;
- identify control gaps and control owners;
- assess consequence and reversibility;
- recommend pause, validation, escalation, or rollback;
- preserve an auditable human decision point.

### Operational Resilience / Business Continuity

Relevant demonstrated work:

- identify critical dependencies;
- examine what happens when a process, supplier, record, or approval path fails;
- separate local symptom removal from restored operating capability;
- define temporary containment and recovery conditions;
- document ownership, fallback, and restart criteria.

### Vendor / Third-Party Risk

Relevant demonstrated work:

- identify the service or component dependency;
- classify access, data, operational, financial, and continuity exposure;
- request evidence proportional to risk;
- distinguish missing evidence from failed evidence;
- define onboarding conditions, exceptions, and accountable approval;
- design ongoing review triggers rather than treating onboarding as a one-time checklist.

### GRC / Governance Support

Relevant demonstrated work:

- translate operational observations into control language;
- connect policy intent to actual operating evidence;
- record exception ownership and remediation status;
- maintain a clear distinction between documented control and effective control;
- create concise, reviewable decision records.

### AI Governance / AI Evaluation / Decision Support

Relevant demonstrated work:

- treat AI output as a candidate, not authority;
- separate facts, assumptions, unknowns, and generated claims;
- require source verification before consequential use;
- preserve uncertainty rather than forcing binary certainty;
- block automatic execution from a judgment signal;
- retain a Human Final Gate and accountable owner.

## Public work samples

The strongest employer-facing path is:

1. [`WORK_SAMPLES.md`](WORK_SAMPLES.md)
2. [`examples/README.md`](examples/README.md)
3. [`methods/01-operational-risk-review.md`](methods/01-operational-risk-review.md)
4. [`methods/02-third-party-risk-intake.md`](methods/02-third-party-risk-intake.md)
5. [`methods/03-ai-assisted-evidence-review.md`](methods/03-ai-assisted-evidence-review.md)
6. [`templates/RISK_REVIEW_TEMPLATE.md`](templates/RISK_REVIEW_TEMPLATE.md)
7. [`templates/CONTROL_GAP_LOG.md`](templates/CONTROL_GAP_LOG.md)
8. [`templates/ESCALATION_BRIEF_TEMPLATE.md`](templates/ESCALATION_BRIEF_TEMPLATE.md)

## What this portfolio does not claim

This portfolio does not claim:

- production deployment of an enterprise GRC platform;
- authority to make legal, regulatory, engineering, medical, employment, or safety decisions;
- formal certification in a framework not explicitly listed;
- autonomous AI execution;
- disclosure of private case records or proprietary employer information.

It demonstrates transferable judgment, control design, documentation, and risk-analysis capability through public-safe composite work samples.