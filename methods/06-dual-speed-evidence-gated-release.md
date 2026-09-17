# Method 06 — Dual-Speed Development and Evidence-Gated Release

> A public work sample for change/release governance across software, hardware and AI-assisted systems. Conceptual review guidance only; not a safety standard, engineering certification, deployed interlock, automated release workflow or substitute for qualified domain review.

## Decision problem

Software modules and physical components often evolve on different schedules. A short AI/code iteration does **not** make its change automatically compatible with mechanical, firmware, supply-chain or safety constraints. Conversely, physical-product development need not be uniformly sequential: scoped iteration can take place within explicit review stages. The review question is **what evidence is necessary before changes cross a subsystem or consequential-use boundary**.

## Terms are different

| Term | Meaning in this method |
| --- | --- |
| Waterfall | A largely sequential software/product lifecycle; still a documented option, not a universally abandoned software practice. |
| Stage-Gate | Milestone reviews, entrance/exit criteria or approval boundaries; can accompany iterative work. |
| Agile | Iterative/adaptive development and feedback practices. |
| CI/CD | Integration and delivery tooling/practices; passing checks demonstrates only the checks performed, not whole-system safety. |

NASA's Software Engineering Handbook `SWE-019` describes waterfall, incremental, iterative, spiral and Agile lifecycles, the importance of tailoring and system-level coordination, and states no model fits every situation. Cooper & Sommer (2016) examine an Agile–Stage-Gate hybrid for physical products; the study describes initially limited evidence rather than a guarantee of benefit.

**Sources (accessed 2026-09-17):**

- [NASA Software Engineering Handbook — SWE-019: Software Life Cycle](https://swehb.nasa.gov/spaces/7150/pages/16449735/SWE-019%2B-%2BSoftware%2BLife%2BCycle).
- [Cooper & Sommer (2016), The Agile–Stage-Gate Hybrid Model, DOI:10.1111/jpim.12314](https://doi.org/10.1111/jpim.12314).

`Dual-Speed` here is a helpful architectural description, **not** the name of an external industry certification or a claim that every hardware team uses Waterfall.

## Public review flow

```text
Change request + owner + current configuration
  ├─ Software / AI: scoped iteration → unit/integration tests → version
  └─ Physical / hardware: prototype → build → interface & acceptance tests
                      ↓
Affected interfaces, BOM/supply dependencies and release scope
                      ↓
Refresh evidence made stale by the change
                      ↓
Independent safety/security/permission review as applicable
                      ↓
Accountable human release decision: approve / revise / hold / reject
                      ↓
Controlled deployment → observe → targeted reassessment
```

**Principle:** iterate within a bounded module at the speed supported by its tests; cross interfaces, physical action or material risk boundaries only with current compatibility and validation evidence. Review intensity is proportional to consequence and reversibility, not a fixed universal checklist.

## Seven review questions

| Review | Question | Evidence to request |
| --- | --- | --- |
| 1. Scope | What actually changed: document, AI/model, software, firmware, electrical, mechanical, supplier or integrated system? | Change description, current version, accountable owner. |
| 2. Requirements | What requirements and assumptions apply, and which are unknown? | Traceable requirements, relevant baselines, open questions. |
| 3. Interface | Are units, timing, APIs, signal/connector contracts, dimensions and expected failure behavior compatible? | Affected interface list, compatibility/negative tests. |
| 4. Change impact | Which earlier tests, reviews, inventory, dependencies or approvals may now be stale? | Targeted impact analysis and evidence refresh. |
| 5. Safety and permissions | Could the change alter real-world action, data access, safe state or rollback feasibility? | Appropriate independent controls, authorization owner and domain review. |
| 6. Release | Have the required integration/exception tests and acceptance conditions been met? | Results, unresolved failures, approve/hold/rework decision. |
| 7. Reality | Did the new version behave as expected in the actual approved environment? | Observed outcome, incident/feedback record, monitoring and reassessment trigger. |

Apply the repository's [Change-Triggered Reassessment](04-change-triggered-reassessment.md) when a material change makes an old approval potentially stale. The standard [Human Final Gate](../README.md#human-final-gate) remains the accountable decision point.

## Synthetic example — electromechanical product

A generic electromechanical device receives a proposed controller-software update and a substitute mechanical component. Developers can validate software functions rapidly, but a joint release review still checks mechanical clearance, component interchangeability, electrical interfaces, version pairing, abnormal conditions and applicable safety controls. A software unit-test pass cannot prove that the assembled physical system has passed its acceptance tests. If supplier fit or fault behavior remains unknown, hold the affected release and request targeted evidence.

This is a **fictional, non-identifying illustration**, not a report of an employer, incident, product defect or actual release outcome.

## AI / robotics boundary

AI-generated code, a new model version or a proposed robot skill is a *candidate*, not an approved physical capability. Deployment requires applicable interface checks, safety review, integration/negative tests and an accountable release decision. No AI model may treat its own output as permission to change safety settings, override independent interlocks or grant actuator access. An explicit programmatic stop/fallback must be implemented and verified independently where required; a Markdown policy alone does not enforce one.

Software changes are not always cheap or reversible either: migration, data compatibility and distributed dependencies can increase release impact. Judge the specific change rather than the substrate label alone.

## Compact public output

```text
Change and configuration:
Accountable owner:
Affected interfaces and dependencies:
Current evidence / stale evidence / unknowns:
Negative and integration tests:
Control gap and consequence:
Recovery or safe containment:
Evidence direction (+ / 0 / -):
Risk signal (Green / Yellow / Red; review only):
Required evidence refresh and reversal condition:
Human Final Gate / release decision:
Post-release outcome and next reassessment trigger:
```

## Boundaries

- No claim that any organization, product or individual follows this method or has been audited.
- A passing CI pipeline, completed document or merged PR does not establish functional safety, regulatory compliance or production readiness.
- The method specifies review questions but does not publish proprietary configurations, thresholds, private incidents, detailed autonomous execution logic or a complete decision engine.
- Actual high-consequence equipment requires qualified owners, relevant standards, independent controls and system-specific testing; not inferred from this public document.

**Compact principle:** Fast iteration is a development capability; evidence-based release is a separate authorization decision.
