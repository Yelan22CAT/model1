# RFC — State-Bound Planning, Replanning & Reality Checkpoints

Status: **Experimental / Public-safe / Not Production Ready**

## Purpose

Bridge-0 treats a plan as a stateful executable semantic object, not a prose checklist.

## Plan object

```text
Plan =
goal
+ step graph
+ dependencies
+ preconditions
+ required capabilities
+ authority bindings
+ resource/state versions
+ validity window
+ expected intermediate states
+ recovery/replan policy
```

## Execution path

```text
Goal
↓
Candidate Plan
↓
Dependency DAG
↓
Precondition / Capability / Authority Check
↓
Bind current state + versions
↓
Execute allowed prefix
↓
Observe actual state
↓
Compare prediction vs reality
↓
still valid?
├─ yes → continue
└─ no  → revalidate / replan / recover
↓
Effect receipt
```

## Core invariants

```text
Reasoning != Planning
Planning != Authority
Planning != Execution
PlanPlausibility != PlanExecutability
PreviouslyValidPlan != CurrentlyExecutablePlan
TaskList != DependencyClosedPlan
ModelDescriptionMatch != RuntimeCapabilityMatch
WorldModelPrediction != WorldState
HighRewardInSimulation != ValidRealWorldPlan
Simulation != Reality
```

## Replanning triggers

Revalidation or replanning is required when material state changes, including:

- resource version changes;
- authorization revocation;
- environment drift;
- dependency-result changes;
- user-priority changes;
- validity-window expiry;
- observed effects differing from predicted effects.

## Model/tool routing

Metadata is not sufficient evidence of runtime capability.

Before execution, the selected model/tool/runtime must be rechecked for availability, modality support, output contract, license, latency, trust/privacy constraints, and current authority.

## World-model boundary

Planning over simulated future states can improve long-horizon search, but the world model is a fallible proxy.

```text
better search over a wrong model
can still yield a worse real-world action
```

Use uncertainty tracking and reality checkpoints.

## Evidence boundary

The v0.251–v0.255 tests are **local synthetic structural tests only**.

```text
local simulation != closure
```
