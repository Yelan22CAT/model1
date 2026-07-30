# Showcase Case 6 — Critical Dependency Failure and Recovery Decision

> Public-safe composite case. This is not a transcript of a single employer, outage, incident, or supplier event.

## Situation

A small operating team depends on one external component and one internal approval path to complete a time-sensitive service. The component becomes unavailable, and the normal approver cannot respond. Staff can improvise a temporary workaround, but it has not been tested under the full operating conditions.

## Proposed consequential action

Use the temporary workaround and continue normal operations without defining a recovery owner or restart conditions.

## Known facts

- the normal component is unavailable;
- the standard approval path is temporarily unavailable;
- a workaround exists;
- the workaround has only been checked under limited conditions;
- continued operation would increase exposure if the workaround fails;
- no single owner has been assigned for recovery and restart approval.

## Inference and unknowns

- the workaround may remain stable during the full operating period;
- the missing component may become available soon;
- the approval delay may be brief;
- downstream teams may be able to absorb a disruption;
- the workaround may create hidden maintenance or safety consequences.

These points are unresolved.

## Dependency map

```text
External component availability
        +
Internal approval availability
        ↓
Operating capability
        ↓
Customer / service commitment
```

The issue is therefore not only a missing part or unavailable approver. It is a combined dependency failure affecting operating continuity.

## Control gaps

- no tested fallback standard;
- no named recovery owner;
- no maximum operating window for the workaround;
- no restart criteria;
- no explicit residual-risk acceptance;
- no trigger for escalation if the dependency remains unavailable.

## Evidence direction

**Direction: `0` — unresolved**

There is enough evidence to support temporary containment, but not enough to support normal operation as though resilience has been restored.

## Risk signal

**Signal: 🔴 Red**

A critical dependency is unavailable, the workaround is incompletely validated, and ownership for recovery is unclear.

## Recommended control response

1. classify the workaround as temporary containment, not restored normal operation;
2. define the maximum permitted operating window and conditions;
3. identify a recovery owner and an accountable restart approver;
4. document the dependency, affected process, and downstream consequence;
5. establish fallback and stop triggers;
6. test the workaround only within a bounded operating envelope;
7. review residual risk before continuing beyond the containment window.

## Reversal condition

The conclusion may move from Red toward Yellow or Green when:

- the normal dependency is restored; or
- the workaround is validated across the required operating envelope;
- recovery ownership is assigned;
- restart criteria and rollback are documented;
- residual risk is explicitly accepted by the accountable human owner.

## Compact management output

```text
Decision required: approve bounded temporary containment or stop the affected process
Current state: normal capability not restored
Primary gap: unvalidated workaround and missing recovery ownership
Immediate control: restrict scope, set time limit, assign owner, define stop trigger
Residual risk: disruption or secondary failure remains possible
Human Final Gate: accountable operational owner
```

## Capability demonstrated

- operational resilience;
- critical-dependency analysis;
- containment versus recovery distinction;
- fallback and restart criteria;
- residual-risk communication;
- accountable ownership design.

## Public boundary

This case omits real organizations, suppliers, components, dates, customers, service levels, and internal procedures. It demonstrates the control pattern without disclosing a private continuity event.