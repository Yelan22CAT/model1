# 16 — Dynamic Human Participation Control

## Purpose

Autonomy should not be framed as a binary choice between "human-in-the-loop" and "no human." Human participation can change dynamically with consequence, uncertainty, reversibility and authority.

This method separates three distinct concepts:

- **Human-in-the-Loop (HITL):** a human participates inside the execution loop; designated steps wait for human judgment, approval or correction.
- **Human-on-the-Loop (HOTL):** the system continues by default while a human supervises and retains the ability to intervene or take over.
- **Human-on-the-Boundary:** a governance layer that defines authority, irreversible-action limits, escalation rules and conditions for human re-entry. It is not itself an ordinary execution state.

## Architecture

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
      AUTO       Human-on-the-Loop  Human-in-the-Loop
 autonomous        supervision       human participates
 execution          + takeover        inside the loop
        |                |                |
        +--------- dynamic switching -----+
                         |
                         v
                PREEMPT / Human Final
```

These modes are **not a linear maturity ladder**. The same system may move among them as operating conditions change.

## Dynamic re-entry signals

Useful signals for increasing or decreasing human participation include:

- uncertainty;
- consequence severity;
- irreversibility;
- recoverability;
- authority or permission expansion;
- time pressure;
- state/provenance integrity;
- credible rollback or alternate path availability.

A low-risk, reversible task may remain autonomous. A monitored task may stay Human-on-the-Loop. A high-uncertainty or high-consequence decision may require Human-in-the-Loop. A hard authority or irreversible boundary may trigger Preempt and Human Final.

## Key distinction

```text
Boundary governs.
On-the-Loop supervises.
In-the-Loop participates.
```

Human-in-the-Loop therefore does not disappear as autonomy improves. Its role changes from a default per-step requirement to a selectively invoked control state.

## Relationship to Selective Intervention

This method extends Method 14.

Selective Intervention answers:

> When should the system continue, remain under observation, or be preempted?

Dynamic Human Participation answers:

> How deeply should a human participate under the current risk and authority state?

Together they support high-throughput autonomy without silently removing accountable human authority.

## Public acceptance tests

A future implementation should be able to demonstrate that:

1. low-risk reversible work can proceed without unnecessary synchronous approval;
2. Human-on-the-Loop supervision does not falsely imply that every action was human-approved;
3. Human-in-the-Loop steps block or wait only where policy requires human participation;
4. hard authority or irreversible boundaries can trigger Preempt independently of model confidence;
5. transitions among AUTO, HOTL and HITL are logged and reviewable;
6. failure of the monitoring or judgment layer does not silently expand execution authority.

## Boundary

This is a public-safe architecture method. It does not publish private thresholds, credentials, runtime enforcement rules, safety-critical operating procedures, or a claim that these controls are already deployed or validated in aviation, medicine, robotics or other high-consequence systems.
