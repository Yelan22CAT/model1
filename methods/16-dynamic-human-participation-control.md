# 16 — Dynamic Human Participation Control

## Purpose

Autonomy should not be framed as a binary choice between "human-in-the-loop" and "no human." Human participation is **phase-specific, task-specific and consequence-sensitive**. A single workflow may use different participation modes at different stages.

This method separates the execution mode from the governance layer.

## Execution modes

### 1. Human Direct / AI-Assisted

The human performs the consequential action while automation supplies information, recommendations or low-level assistance.

### 2. Human-in-the-Loop (HITL)

A human participates inside the execution loop. Designated actions wait for human judgment, approval, correction or direct operation.

### 3. Human-on-the-Loop (HOTL)

The system continues by default while a human supervises and retains the ability to intervene or take over.

### 4. Full Auto / Human-out-of-the-Loop

The system executes inside a granted authority envelope without synchronous human participation during normal operation. Human governance may still exist before, around and after the run.

**Full Auto does not mean unbounded authority.**

## Governance layer: Human-on-the-Boundary

Human-on-the-Boundary is not an execution mode. It defines:

- granted authority;
- irreversible-action limits;
- escalation rules;
- stop / preempt conditions;
- human re-entry conditions;
- decisions reserved for Human Final.

## Corrected architecture

```text
                    Human-on-the-Boundary
                  authority / consequence limits
                              |
                              v
                   Selective Intervention
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
      Human Direct /        HITL             HOTL            FULL AUTO
       AI-Assisted      human inside     human supervises    no synchronous
                         the loop          + takeover          human in run
             \                |                |                /
              +--------------- dynamic mode routing -----------+
                              |
                              v
                    PREEMPT / Human Final
```

The modes are **not a linear maturity ladder**. They are routing choices.

## Phase-Specific Participation

Do not label an entire domain or workflow with one permanent human-participation mode.

```text
workflow phase A → Full Auto
workflow phase B → Human-on-the-Loop
workflow phase C → Human-in-the-Loop
workflow phase D → Human Direct
```

A mode can change when the operating phase, environment, consequence or recovery conditions change.

This is especially important in long-running physical systems, but the same principle applies to digital workflows.

## Intervention-Latency / Takeover-Feasibility Gate

Human-on-the-Loop is useful only when supervision can realistically prevent or contain harm.

A simplified design check is:

```text
detect
+ understand
+ decide
+ intervene
< time-to-boundary / time-to-harm
```

If the operator cannot observe the state, rebuild context and take effective control before the consequence becomes irreversible, "human supervision" is nominal rather than protective.

Therefore HOTL should not be inserted merely as a compromise between HITL and Full Auto.

## Mode-routing variables

Useful routing variables include:

- consequence severity;
- uncertainty;
- irreversibility;
- recoverability;
- observability;
- takeover feasibility and time-to-harm;
- authority or permission expansion;
- state / provenance integrity;
- rollback and alternate-path availability;
- validated automation capability;
- cost and latency of synchronous human participation.

A low-risk, reversible digital task may move directly to Full Auto. A consequential checkpoint may stay HITL. A continuously observable physical process may use HOTL when takeover is feasible. Some phases may remain Human Direct.

## Aviation analogy — bounded, not literal

Aviation is useful as an analogy for **phase-specific mode switching**, but it should not be simplified into "takeoff and landing are always manual, cruise is always automatic."

Certified autoland exists, and FAA guidance explicitly tells crews conducting coupled or autoland operations to monitor the automatic flight-control system and be prepared to intervene. Airbus has also demonstrated fully automatic takeoff in research testing. Actual operating modes depend on aircraft, certification, operator procedures, airport capability and conditions.

References:
- FAA, Navigation Aids / autoland monitoring guidance: https://www.faa.gov/air_traffic/publications/atpubs/aip_html/part2_enr_section_4.1.html
- Airbus, Autoland flight-test overview: https://flightsafety.airbus.com/2023/02/28/flight-test-autoland-tests/
- Airbus, 2020 automatic takeoff demonstrator: https://www.airbus.com/en/newsroom/press-releases/2020-01-airbus-demonstrates-first-fully-automatic-vision-based-take-off

The architectural lesson is not a specific aviation procedure. It is:

> participation mode follows the phase and risk state, not the industry label.

## Key distinction

```text
Boundary governs.
Full Auto delegates.
On-the-Loop supervises.
In-the-Loop participates.
Human Direct executes.
```

Human-in-the-Loop does not disappear as autonomy improves. Human-on-the-Loop also does not need to appear everywhere. Both are selectively invoked when they add control value.

## Relationship to Selective Intervention

Selective Intervention asks:

> Should execution continue, remain under observation, reroute, or be preempted?

Dynamic Human Participation asks:

> Who should be operationally engaged right now, and at what depth?

Together they support high-throughput autonomy without silently removing accountable human authority.

## Public acceptance tests

A future implementation should be able to demonstrate that:

1. low-risk reversible work can proceed without unnecessary synchronous approval;
2. Full Auto remains inside a bounded permission envelope;
3. Human-on-the-Loop supervision does not falsely imply that every action was human-approved;
4. HOTL is used only where state observability and takeover latency make intervention credible;
5. Human-in-the-Loop steps wait where policy requires synchronous human participation;
6. mode transitions are logged and reviewable;
7. hard authority or irreversible boundaries can trigger Preempt independently of model confidence;
8. failure of the monitoring or judgment layer does not silently expand execution authority.

## Boundary

This is a public-safe architecture method. It does not publish private thresholds, credentials, runtime enforcement rules or safety-critical operating procedures. The aviation references are reality checks on the analogy, not claims that this framework is certified or deployed in aviation, medicine, robotics or other high-consequence systems.
