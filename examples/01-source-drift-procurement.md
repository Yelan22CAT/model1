# Showcase Case 1 — Source Drift in a Procurement Decision

> Public-safe composite case. This is not a transcript of any single workplace event.

## Situation

A team needs to order a component for an upcoming build. Two internal records appear to describe the same item, but the naming order and conversion direction are inconsistent. One record points to specification A; the other appears to point to specification B.

The immediate pressure is to place the order quickly so the schedule does not slip.

## Proposed next action

Approve the purchase using the first matching record.

## Known facts

- two records refer to what may be the same component;
- the naming convention is inconsistent;
- the records do not clearly identify which specification is current;
- the order would create cost and schedule consequences.

## Assumptions

- the first matching record is the intended one;
- the two records are interchangeable;
- the specification difference will not affect fit or function.

None of these assumptions has been verified.

## Risk decomposition

### Source risk

The apparent duplication may be a master-data problem rather than a harmless formatting difference.

### Consequence risk

A wrong order could create:

- unusable inventory;
- production delay;
- emergency reordering;
- hidden rework;
- repeated future errors if the source record remains uncorrected.

### Reversibility

The decision is partially reversible before purchase approval, but much less reversible after the order is placed and received.

## Model 1 review

**Signal: 🟡 Yellow**

The issue is not that the purchase is definitely wrong. The issue is that evidence and assumption are mixed while reversibility is shrinking.

## Recommended control response

1. pause approval;
2. compare the records against an authoritative drawing, specification, or verified prior use;
3. identify the current source of truth;
4. correct or flag the duplicate record;
5. preserve a clear audit note for the final choice;
6. return the decision to the responsible human owner.

## Human Final Gate

The framework does not choose the component. It identifies why approval should pause until the source conflict is resolved.

## Capability demonstrated

- source discipline;
- operational risk framing;
- master-data quality awareness;
- consequence analysis;
- reversible decision design;
- escalation without unnecessary alarm.

## Public boundary

This case omits all real names, organizations, dates, product identifiers, drawings, quantities, and internal records. It demonstrates the reasoning pattern without exposing a private case or proprietary source data.
