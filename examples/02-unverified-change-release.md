# Showcase Case 2 — Unverified Change Before Release

> Public-safe composite case. This is not a transcript of any single workplace event.

## Situation

A technical team makes a late change to a custom assembly after discovering a clearance problem. The proposed fix appears workable in a static check, but the full operating range has not been verified.

Schedule pressure encourages the team to proceed because the change looks small and the immediate obstruction appears removed.

## Proposed next action

Release the modified assembly without a full-range validation.

## Known facts

- a clearance issue was found;
- a local modification reduced the visible interference;
- only a limited check has been completed;
- the system has additional operating positions or load conditions;
- release would reduce the ability to investigate and correct the issue safely.

## Assumptions

- a successful local check represents the full operating range;
- the modification does not transfer stress to another connection;
- no secondary leak, contact, or wear condition will appear later;
- schedule pressure justifies accepting the remaining uncertainty.

These assumptions are not yet supported by complete validation.

## Risk decomposition

### Validation risk

A local fix can remove the visible symptom without resolving the underlying geometry or system interaction.

### Consequence risk

Premature release could create:

- repeated interference;
- transferred load or stress;
- leakage or component damage;
- field rework;
- safety exposure;
- unclear accountability after release.

### Reversibility

The change is easier to test and revise before release. Once deployed, access becomes harder, evidence may be lost, and correction becomes more expensive.

## Model 1 review

**Signal: 🔴 Red**

A consequential action is being proposed while a hard validation gap remains and reversibility is about to shrink sharply.

## Recommended control response

1. freeze release;
2. define the full operating envelope that must be checked;
3. verify clearance, connection integrity, and secondary effects across that envelope;
4. document the observed result and unresolved uncertainty;
5. escalate the release decision to the accountable technical owner;
6. proceed only after an explicit human sign-off based on evidence.

## Human Final Gate

The framework does not prescribe the engineering fix. It identifies that release should not occur until the validation gap is closed or consciously accepted by the responsible human authority.

## Capability demonstrated

- pre-execution risk review;
- technical issue escalation;
- reversibility analysis;
- distinction between symptom removal and root control;
- human accountability design;
- stop/release gate thinking.

## Public boundary

This case omits all real names, organizations, dates, equipment types, dimensions, drawings, failure records, and internal procedures. It demonstrates the control pattern without exposing a private incident or proprietary design information.
