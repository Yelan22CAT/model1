# Changelog

## 2026-09-26｜Autonomy-governance and provenance update

### Added

- Added `methods/14-selective-intervention-autonomy-governance.md` to move Pre-Stop from a presumed per-step choke point into a selective intervention control plane with Free Run / Shadow / Preempt states.
- Added `PROVENANCE.md` as a dated contribution and influence ledger.
- Added `CITATION.cff` so later users, researchers and derivative work have a canonical citation target.
- Added `methods/15-originality-provenance-defense.md` with public priority anchors, derivation classes, citation spine, claim boundaries and supersession-without-erasure.
- Public citation identity is the repository handle `Yelan22CAT`; personal legal-name mapping remains outside the public artifact.

### Updated

- Updated the public README and methods index through Method 14.
- Reframed Human Final as an authority boundary rather than mandatory human approval of every low-risk step.
- Added trajectory recoverability as the main control objective for autonomous workflows.

### Scope

This is architecture documentation, not a claim of deployed runtime enforcement. The provenance record documents dated publication and contribution boundaries; it does not assert blanket originality, patent rights or legal ownership.

## 2026-09-24｜Weekly public update — memory governance, judgment middleware and cross-model reconciliation

### Added

- Added `methods/11-layered-context-memory-governance.md`.
- Added `methods/12-bounded-judgment-middleware-coordination.md`.
- Added `methods/13-cross-model-evidence-reconciliation.md`.

### Updated

- Updated the method index and public README through Method 13.
- Added a bounded external engineering reference to `qybaihe/mu`.

### Scope

This is a controlled public projection. It does not publish private prompts, thresholds, person/case records, credentials, hidden runtime packs, unrestricted agent permissions, or the complete private engine. External performance claims remain source-reported unless independently reproduced.

## 2026-09-15｜Public safety companion — Human Catch-up Gate and Dual-Key Resume Lock

### Added

- Added `safety/HUMAN_CATCHUP_GATE.md` as a public-safe external pacing-control primitive for cases where consequential AI progression can outpace human comprehension, verification, or supervision.
- Added `safety/DUAL_KEY_RESUME_LOCK.md` as a second lock: after freeze, resume requires both explicit human authorization and an external control-plane invariant check.
- Added `safety/COMPREHENSION_DEBT.md` to define unresolved human-understanding debt as a qualitative risk concept rather than a validated quantitative metric.
- Added `safety/THREAT_MODEL.md` to state bypass conditions, control-boundary limits, and what the stop/resume primitives do not solve.
- Added `safety/DESIGN_PRINCIPLES.md` and `safety/README.md` as compact public navigation and design-rule layers.

### Updated

- Updated `README.md` to 2026-09-15 and added the public safety companion without replacing the canonical Model 1 v1.0 judgment core.

### Public structure

```text
RUNNING
→ Human Catch-up Gate
→ PRE-STOP / FREEZE
→ Snapshot + Trace
→ Human Review
→ Dual-Key Resume Lock
→ Resume / Modify / Rollback / Reject
```

The second lock requires:

```text
Authorized human decision
AND
External control-plane invariant check
```

Neither the stopped model nor a single stale approval can self-authorize restart.

### Design boundary

This update does not claim to solve AI alignment or catastrophic risk as a whole and does not assign a numerical probability to catastrophic or existential AI risk.

It deliberately publishes only small control primitives and public design rules. It does not publish private thresholds, observer packs, calibration chains, hidden runtime packs, anti-poisoning internals, or autonomous execution logic.

## 2026-09-01｜Monthly public update — current-state assurance and AI decision-risk review

### Added

- Added `methods/04-change-triggered-reassessment.md` to show how a prior approval or assessment is refreshed after a material operating-state change without automatically repeating every historical review.
- Added three public-safe composite cases:
  - `examples/09-control-effectiveness-drift.md` — temporal validity, evidence currency, and targeted control retesting after a process change;
  - `examples/10-local-ai-hidden-cloud-dependency.md` — local-vs-offline distinction, deployment-boundary review, unresolved data egress, and accountable approval gating;
  - `examples/11-metric-decision-objective-mismatch.md` — metric usefulness vs decision-objective alignment, exception design, and limits on model authority.
- Added `templates/CHANGE_REASSESSMENT_RECORD.md` as a reusable work product for prior decision, material-change trigger, affected evidence, current-state review, reversal condition, and Human Final Gate.

### Updated

- Updated `README.md` to September 2026 and added the new methods, cases, and reassessment work product while preserving the canonical v1.0 basic core.
- Updated `PORTFOLIO_MAP.md` with temporal-validity, deployment-boundary, and metric-goal alignment evidence.
- Updated `ROLE_EVIDENCE_MATRIX.md` with additional Risk & Controls, GRC, Technology / AI Risk, AI Governance, and AI / Model Risk evidence paths.
- Updated `WORK_SAMPLES.md` and `examples/README.md` from eight to eleven composite cases.
- Updated `FOR_RECRUITERS.md` with a September ten-minute review path and current-state assurance examples.

### Public structure

The stable public v1.0 core remains:

```text
Proposed consequential action
→ Scope Lock
→ Source-State Check
→ Evidence Direction: + / 0 / -
→ Boundary / Consequence / Reversibility
→ Risk Signal: Green / Yellow / Red
→ Human Final Gate
```

The September release adds a reusable outer loop:

```text
Prior decision
→ material change
→ identify affected evidence
→ refresh current state
→ rerun the same public v1.0 core
→ Human Final Gate
```

### Capability demonstrated

- temporal validity and current-state assurance;
- change-triggered control reassessment;
- distinction between historical assurance and current assurance;
- AI deployment-boundary and data-egress review;
- local-vs-offline / no-egress distinction;
- metric-to-decision-objective alignment;
- model-risk and decision-risk separation;
- continued human ownership of consequential decisions.

### Scope

This update is a public-safe employment and work-sample expansion. It does not publish:

- private formation history or identifiable case chains;
- real employers, vendors, people, systems, or confidential deployment details;
- private observer packs, thresholds, or calibration chains;
- detailed market, interaction, allocation, or pacing models;
- anti-poisoning implementation internals;
- hidden runtime packs or autonomous execution logic;
- the complete private engine.

## 2026-07-30｜Employer-facing work-sample expansion

### Added

- Added `PORTFOLIO_MAP.md` to explain the transfer path from manufacturing operations and field service into operational risk, resilience, GRC, TPRM, and AI-assisted decision support.
- Added `WORK_SAMPLES.md` as the employer-facing index of cases, methods, and templates.
- Added three public methods:
  - `methods/01-operational-risk-review.md`;
  - `methods/02-third-party-risk-intake.md`;
  - `methods/03-ai-assisted-evidence-review.md`.
- Added three public-safe composite cases:
  - `examples/03-near-miss-escalation.md`;
  - `examples/04-vendor-onboarding-control-gap.md`;
  - `examples/05-ai-generated-summary-before-approval.md`.
- Added three reusable work-product templates:
  - `templates/RISK_REVIEW_TEMPLATE.md`;
  - `templates/CONTROL_GAP_LOG.md`;
  - `templates/ESCALATION_BRIEF_TEMPLATE.md`.

### Updated

- Updated `README.md` with employer-facing positioning, career direction, expanded work portfolio, methods, cases, templates, and a current repository map.
- Updated `FOR_RECRUITERS.md` with a two-minute scan, ten-minute review, deeper technical path, role alignment, and work-product examples.
- Updated `examples/README.md` from two to five public showcase cases and added domain coverage and supporting-method links.

### Capability demonstrated

- operational-risk and control-gap analysis;
- operational-resilience, containment, restart, fallback, and closure thinking;
- proportional vendor and third-party risk intake;
- conditional approval, exception ownership, and monitoring triggers;
- AI claim verification, source traceability, and consequential-use gating;
- concise escalation and management decision support;
- translation of hands-on technical operations into structured risk work.

### Scope

This update deliberately publishes more cases, analysis structure, and work products for employment review.

It still does not publish:

- identifiable private cases or original incident records;
- real organizations, vendors, people, drawings, or confidential systems;
- private observer packs, thresholds, or calibration chains;
- detailed market, interaction, allocation, or pacing models;
- anti-poisoning implementation internals;
- hidden runtime packs or autonomous execution logic;
- the complete private engine.

## 2026-07-28｜Judgment-language interface and two-axis public output

### Added

- Added `docs/02-judgment-language.md` as the public-safe V1 guide for:
  - fact / inference / unknown separation;
  - evidence direction `+ / 0 / -`;
  - Green / Yellow / Red action-risk signals;
  - gray analysis and hard boundaries;
  - canonical public states;
  - compact decision-support output;
  - closure awareness and Human Final Gate.

### Updated

- Updated `README.md` with the two-axis public architecture, current reading paths, machine-readable summary, and 2026-07-28 update date.
- Updated `FOR_RECRUITERS.md` to demonstrate uncertainty calibration, judgment-interface design, compact decision communication, and workflow assurance.
- Updated `docs/00-start-here.md` and `docs/01-basic-principles.md` with evidence-direction language and hard-boundary handling.
- Updated `ARCHITECTURE.md`, `MODEL1_MINIMAL_CORE.md`, `README_FOR_CODERS.md`, and `CONTROL_VOCABULARY.md` so active public artifacts use the same source-state → direction → risk-signal → Human Final Gate sequence.
- Updated `INTRO_CN.md` and `INTRO_EN.md` as the current bilingual public tutorials.
- Updated `GLOSSARY.md` with canonical states, balanced ternary, two-axis output, reversal condition, and closure awareness.
- Updated both public showcase cases and `examples/README.md` to display evidence direction separately from risk signal and to use a compact decision-support summary.
- Updated `SAFETY.md` to clarify that neither `+ / 0 / -` nor Green / Yellow / Red creates execution, ranking, punishment, or control authority.

### Public structure

```text
Proposed consequential action
→ Fact / inference / unknown
→ Evidence direction: + / 0 / -
→ Boundary / consequence / reversibility
→ Risk signal: Green / Yellow / Red
→ Human Final Gate
```

### Scope

This update publishes only the beginner-safe V1 judgment-language interface.

It does not publish:

- private cases or identifiable narratives;
- private observer packs, thresholds, or calibration chains;
- detailed market, interaction, allocation, or pacing models;
- anti-poisoning implementation internals;
- hidden runtime packs or autonomous execution logic;
- the complete private engine.

## 2026-07-22-b｜Public showcase cases and connected learning path

### Added

- Added `examples/01-source-drift-procurement.md` as a public-safe composite case demonstrating source reconciliation, master-data risk, and reversible approval design.
- Added `examples/02-unverified-change-release.md` as a public-safe composite case demonstrating validation gaps, escalation, rollback analysis, release control, and the Human Final Gate.
- Added `examples/README.md` as the public case index.

### Updated

- Connected `docs/00-start-here.md` and `docs/01-basic-principles.md` to the two public showcase cases.
- Updated the beginner reading path from principles to practice, architecture, and safety.
- Updated `FOR_RECRUITERS.md` with direct case links.

### Scope

The showcase cases are composite, anonymized, and generalized.

This update does not add:

- real names, organizations, dates, or equipment identifiers;
- private cases or incident records;
- identifiable workplace, relationship, family, medical, or financial details;
- drawings, quantities, internal records, or proprietary thresholds;
- private calibration chains or runtime packs;
- autonomous execution;
- complete private engine logic.

## 2026-07-22｜Job-search positioning and recruiter entry

### Added

- Added `FOR_RECRUITERS.md` as a recruiter-facing capability and role-relevance guide.
- Added `docs/01-basic-principles.md` as a public-safe explanation of the framework's core principles.

### Updated

- Refocused the README first screen around operational risk, GRC, AI governance, decision support, source discipline, and human-in-the-loop control design.
- Added separate recruiter and general-reader navigation paths.
- Clarified that the repository is a portfolio documentation artifact, not a production deployment or autonomous system.
- Standardized Green / Yellow / Red as review prompts rather than commands or permissions.

### Scope

This update demonstrates capability without transferring the private core.

It does not add:

- private archive content;
- private cases or identifiable narratives;
- workplace, relationship, family, medical, or financial details;
- private calibration chains, thresholds, or runtime packs;
- autonomous execution;
- professional advice;
- complete private engine logic.

## 2026-06-12｜Beginner start-here guide

### Added

- Added `docs/00-start-here.md` as a beginner-friendly public entry point for Model 1 v1.0.
- Added README entry link to the beginner start-here guide.

### Scope

This is a public scaffold update only.

It does not add:

- private archive content;
- private cases;
- identifiable personal information;
- relationship, family, medical, workplace, or financial details;
- third-person profiling;
- manipulation or persuasion guidance;
- autonomous execution;
- medical, legal, financial, or mental health advice;
- private engine logic.

## 2026-06-06-d｜README first-screen positioning update

### Updated

- Improved README first-screen project positioning.
- Added machine-readable project summary for human and LLM discovery.
- Standardized README Mermaid and signal table display with 🟢 Green / 🟡 Yellow / 🔴 Red.
- Strengthened public-facing keywords:
  - AI workflow
  - judgment framework
  - human final gate
  - source discipline
  - risk boundary
  - anti-weaponization
  - decision support
  - not automation executor

### Scope

This is a public-facing README clarity update only.

It does not add:

- private archive content;
- private cases;
- identifiable personal information;
- relationship, family, medical, or financial details;
- third-person profiling;
- relationship prediction;
- manipulation or persuasion guidance;
- autonomous execution;
- medical, legal, financial, or mental health advice.

## 2026-06-06-c｜README entry and signal display note

### Updated

- Added README entry points for `INTRO_CN.md`, `INTRO_EN.md`, and `CHANGELOG.md`.
- Added suggested reading order for new readers.
- Standardized Green / Yellow / Red display using GitHub-stable emoji signals:
  - 🟢 Green
  - 🟡 Yellow
  - 🔴 Red

### Scope

This is a navigation and formatting update only.

It does not add:

- private archive content;
- third-person profiling;
- manipulation or persuasion guidance;
- autonomous execution;
- medical, legal, financial, or mental health advice.

## 2026-06-06-b｜Public intro tutorial expansion

### Added / Updated

- Expanded `INTRO_CN.md` from a minimal starter card into a short public intro tutorial.
- Expanded `INTRO_EN.md` as a plain-English companion version.
- Added basic usage flow:
  - write the next action;
  - check real-world consequence;
  - verify key facts from real sources;
  - check stop / rollback;
  - mark Green / Yellow / Red;
  - keep final decision human-controlled.
- Added simple purchasing-email example.
- Added explicit Final Gate section.
- Added stronger misuse boundaries.

### Scope

This update remains within Model 1 v1.0.

It does not add:

- private archive content;
- third-person analysis;
- relationship prediction;
- manipulation guidance;
- autonomous execution;
- medical, legal, financial, or mental health advice.

## 2026-06-06｜Public intro tutorial update

### Added

- `INTRO_CN.md`
- `INTRO_EN.md`

### Purpose

Add a minimal public entry point for Model 1 v1.0.

The intro files explain Model 1 as a first-person stop-loss guardrail before action.

### Scope

This update is limited to:

- first-person self-check;
- stop-loss judgment;
- Green / Yellow / Red signal;
- human-controlled final decision.

### Excluded

This update does not include:

- private archive content;
- third-person profiling;
- persuasion or manipulation use;
- autonomous execution;
- hidden model layers.