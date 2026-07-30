# Showcase Case 4 — Vendor Onboarding With Missing Control Evidence

> Public-safe composite case. This is not a transcript of any single vendor review.

## Situation

A business team wants to onboard a specialized service provider quickly because the provider offers a needed capability and the current process is creating delay.

The vendor has completed an intake questionnaire and supplied marketing material, but several control claims are supported only by self-attestation. The service would become operationally important and would receive limited access to internal data.

## Proposed next action

Approve full onboarding immediately and collect the remaining evidence after the contract starts.

## Known facts

- the service addresses a real operational need;
- an internal business owner supports the onboarding;
- the vendor supplied basic corporate and service information;
- the vendor would receive limited internal data access;
- the service would become difficult to replace after implementation;
- business continuity, incident-notification, and subcontractor evidence remain incomplete;
- contract and access decisions would reduce reversibility.

## Assumptions

- self-attested controls operate as described;
- missing documents will be supplied after onboarding;
- the vendor can recover within an acceptable period after a disruption;
- subcontractors do not create additional material exposure;
- limited access cannot expand without a new review;
- commercial urgency justifies accepting unresolved evidence.

## Inherent risk

**Moderate to High**, because the proposed service creates:

- operational dependency;
- internal-data exposure;
- switching and transition cost;
- continuity and incident-response dependency;
- possible fourth-party exposure.

## Evidence-state review

| Control area | Evidence state | Assessment |
| --- | --- | --- |
| corporate identity and ownership | verified | sufficient for intake |
| service description and internal owner | verified | sufficient for scope definition |
| data-access scope | partially supported | technical access boundaries not finalized |
| incident notification | self-attested | contract and process evidence incomplete |
| business continuity | pending | plan summary supplied; test evidence absent |
| subcontractor governance | pending | fourth-party list incomplete |
| exit and transition support | unknown | no tested transition approach identified |

## Evidence direction

**Direction: `0` — unresolved.**

The evidence supports the business need but does not yet resolve whether the control environment is adequate for full onboarding.

## Risk signal

**Signal: 🟡 Yellow for a restricted pilot; 🔴 Red for full onboarding.**

A limited pilot may preserve reversibility. Full onboarding would create dependency and access before material evidence gaps are controlled.

## Control gaps

1. continuity capability is not independently supported;
2. incident-notification obligations are not fully defined;
3. subcontractor exposure is incomplete;
4. access boundaries are not finalized;
5. exit and transition conditions are unclear;
6. no time-limited exception owner has been identified.

## Recommended control response

### Before any pilot

- define the exact service scope;
- restrict data and system access to the minimum necessary;
- name the internal business and technical owners;
- confirm incident contacts and notification path;
- document the pilot end date and success criteria;
- preserve a manual fallback or alternate provider path.

### Before full onboarding

- obtain and review continuity and recovery evidence;
- confirm subcontractor and data-location information;
- include incident notification, access, audit, and exit terms in the contract;
- test the operational handoff and support process;
- document residual gaps and exception expiry;
- obtain accountable approval.

## Recommended disposition

```text
Pilot only — conditional approval
```

The pilot should not silently become production use. Full onboarding requires a new review against defined evidence and control conditions.

## Ongoing monitoring triggers

- scope or data-access expansion;
- repeated service failure;
- material incident;
- new subcontractor;
- ownership or geographic change;
- exception expiry;
- contract renewal;
- evidence that the fallback path is no longer viable.

## Reversal condition

The direction may move to `+` and the risk signal toward Green only when:

- required evidence is reviewed;
- access is bounded;
- continuity and incident obligations are defined;
- subcontractor exposure is understood;
- exit and fallback conditions are documented;
- the responsible owner approves the residual risk.

## Compact decision-support output

```text
Conclusion: Do not grant full onboarding from the current evidence.
Business value: supported.
Critical unknowns: continuity test evidence, subcontractors, exit support, final access scope.
Evidence direction: 0
Risk signal: Yellow for restricted pilot; Red for full onboarding.
Control gap: dependency and access would be created before required evidence is complete.
Reversal condition: evidence reviewed, terms defined, access bounded, fallback documented, owner approval.
Safe next action: approve only a time-limited, low-access pilot with explicit conditions.
Human Final Gate: the accountable business and risk owners decide.
```

## Capability demonstrated

- proportional third-party risk intake;
- inherent-risk classification;
- evidence-state assessment;
- distinction between business value and control adequacy;
- conditional approval and exception design;
- concentration, exit, and fourth-party thinking;
- ongoing monitoring design;
- concise risk communication.

## Public boundary

This case does not identify a real vendor, organization, contract, system, data set, questionnaire, certification, or internal policy. It demonstrates a TPRM control pattern without claiming a completed regulated vendor assessment.