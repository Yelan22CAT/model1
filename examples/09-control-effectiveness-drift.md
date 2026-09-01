# Case 09 — Control Effectiveness Drift After a Process Change

## Situation

A recurring operational control was previously reviewed and considered effective. The workflow later changed, but the prior assessment remained the main evidence being cited for continued reliance on the control.

No confirmed failure has been identified. The problem is that the evidence describes the old process state.

## Proposed consequential action

Continue relying on the previous control assessment without refreshing evidence under the changed workflow.

## Known facts

- the control was previously assessed;
- the operating workflow has changed since that assessment;
- the documented control objective remains relevant;
- no current post-change observation has yet confirmed whether the control operates as intended;
- no confirmed control failure has been established.

## Inferences, stale evidence, and unknowns

### Stale evidence

- the previous effectiveness assessment;
- historical samples collected before the workflow change.

### Inferences

- the control may still be effective;
- the workflow change may have altered how the control is performed, evidenced, or owned.

### Unknowns

- whether the control is operating consistently in the current workflow;
- whether evidence capture changed;
- whether ownership or approval behavior changed;
- whether exceptions are now handled differently.

## Risk and control decomposition

| Element | Review |
| --- | --- |
| Control objective | still relevant |
| Historical effectiveness | previously supported |
| Current effectiveness | not yet demonstrated |
| Evidence currency | stale |
| Control ownership | requires confirmation after change |
| Consequence | false reliance on a control that may no longer operate as designed |
| Reversibility | relatively high before a consequential approval; lower after repeated reliance |

## Evidence direction

**`0` — unresolved.**

The old evidence does not prove the control failed, but it also does not establish current effectiveness.

## Risk signal

**Yellow — slow down and refresh the decision-changing evidence.**

The correct response is not to assume failure and not to inherit assurance automatically.

## Control response

1. identify exactly what changed in the workflow;
2. identify which prior evidence was made stale by the change;
3. observe or test the control in the current process state;
4. confirm current owner and exception path;
5. record whether the prior conclusion remains valid, requires conditions, or must be reversed.

## Compact decision-support output

**Decision required:** Can the prior assessment still support current reliance?

**Conclusion:** Not yet. The control may remain effective, but the available evidence is temporally misaligned with the current operating state.

**Decisive evidence:** The workflow changed after the last effectiveness review.

**Unknowns:** Current execution, current ownership, and current exception handling.

**Evidence direction:** `0`

**Risk signal:** Yellow

**Control gap:** No current-state evidence of effectiveness.

**Reversal condition:** Current observation shows the control still operates as intended under the changed workflow.

**Safe next action:** Perform a targeted post-change reassessment rather than repeating the entire historical review.

**Human Final Gate:** The accountable control or process owner decides whether reliance may continue.

## Closure condition

The case closes when:

- the changed workflow is documented;
- current control operation is evidenced;
- ownership is confirmed;
- material exceptions are addressed;
- the current assessment is recorded with its effective state and date.

## Employer-facing capability demonstrated

- control effectiveness review;
- temporal validity and evidence currency;
- change-triggered reassessment;
- proportional control testing;
- distinction between historical assurance and current assurance;
- remediation and closure discipline.

## Public boundary

This is a generalized composite case. It contains no real employer, system, control record, incident, private threshold, or proprietary process detail.