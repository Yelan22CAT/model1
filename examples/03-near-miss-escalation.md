# Showcase Case 3 — Near-Miss Escalation Without a Complete Incident Record

> Public-safe composite case. This is not a transcript of any single workplace event.

## Situation

During a custom-equipment test, a component moves unexpectedly and creates a potential strike or crush exposure. No injury is confirmed, the equipment is stopped, and the immediate area is cleared.

The initial record is incomplete. Several people describe the event differently, and there is pressure to restart work after a quick visual check because production is already delayed.

## Proposed next action

Return the equipment to testing without a structured review because no injury occurred and the immediate symptom appears to be gone.

## Known facts

- unexpected movement occurred during testing;
- the movement created a plausible hazardous exposure;
- testing was stopped;
- no injury has been confirmed from the available record;
- the exact initiating mechanism has not been verified;
- the current record does not establish that the relevant control has been restored.

## Unknowns

- whether the event resulted from design, assembly, setup, control, component, or operating conditions;
- whether the full travel or load range was tested;
- whether the hazard can recur;
- whether evidence was preserved before adjustments were made;
- who has authority to approve restart;
- whether a formal incident or near-miss record is required under the organization's process.

## Evidence direction

**Direction: `-` — current evidence opposes immediate restart.**

The available evidence does not establish that the hazard is understood or controlled.

## Risk signal

**Signal: 🔴 Red**

Restart would reduce the ability to preserve evidence and could recreate a hazardous condition before the control gap is understood.

## Risk decomposition

### Safety and operational risk

The absence of a confirmed injury does not establish that the control was effective. A near miss can reveal a failure path before loss occurs.

### Evidence risk

Adjusting, disassembling, or restarting too early can erase the original condition and weaken later root-cause analysis.

### Governance risk

If restart authority, inspection criteria, and sign-off are unclear, responsibility may be transferred informally to the people closest to the equipment rather than retained by the accountable technical or operational owner.

### Resilience risk

A fast restart may restore activity without restoring reliable operating capability. Repeated stops, rework, or a later incident can create greater disruption than a bounded investigation.

## Expected controls

- immediate containment and area control;
- preservation of relevant evidence;
- factual event record separating observation from interpretation;
- defined inspection and validation scope;
- accountable technical and operational ownership;
- explicit restart criteria;
- documented authorization before testing resumes.

## Control gaps

- incomplete source record;
- root cause unverified;
- restart criteria undefined;
- authority and ownership unclear;
- no evidence that the full operating condition has been revalidated.

## Recommended control response

1. keep the affected test path frozen;
2. record observed facts, time sequence, configuration, and changes already made;
3. separate witness observations from causal hypotheses;
4. identify the accountable technical and operational owners;
5. define the inspection and test envelope required before restart;
6. verify that temporary changes do not introduce secondary hazards;
7. document residual unknowns;
8. require explicit human sign-off for restart.

## Decision required

The responsible owner must decide whether:

- more evidence is required before testing;
- a controlled limited test is permitted;
- engineering or safety review is required;
- the equipment remains out of service.

## Reversal condition

The Red signal may be reduced only after evidence shows that:

- the failure path has been bounded;
- required controls are restored;
- the test envelope is defined and completed;
- restart authority is clear;
- residual risk is accepted by the responsible owner.

## Compact decision-support output

```text
Conclusion: Do not restart from the current record.
Decisive evidence: unexpected hazardous movement occurred and restored control has not been verified.
Unknowns: initiating mechanism, recurrence path, full validation status, restart authority.
Evidence direction: -
Risk signal: Red
Control gap: no verified restart condition or accountable sign-off.
Reversal condition: bounded cause, restored controls, completed validation, authorized restart.
Safe next action: preserve evidence and issue a short escalation brief to the responsible owner.
Human Final Gate: restart remains an accountable human decision.
```

## Capability demonstrated

- operational-risk framing;
- near-miss and control-failure thinking;
- evidence preservation;
- fact / inference separation;
- containment and restart governance;
- concise escalation;
- operational-resilience reasoning;
- Human Final Gate design.

## Public boundary

This case omits all real names, organizations, dates, equipment identifiers, dimensions, photos, medical information, internal procedures, and private incident records. It demonstrates a reusable control pattern rather than reproducing a real event.