# RFC — Observation-Grounded Agency, Trajectory Learning & Search–Execution Separation

Status: **Experimental / Not Production Ready**

This RFC extends Bridge-0 from reasoning/planning into interactive agent execution. It treats ReAct-, Reflexion-, and LATS-style mechanisms as useful patterns that require explicit state, authority, provenance, memory and commit boundaries.

## 1. Core loop

```text
State / Goal
↓
Deliberation
↓
Candidate Action
↓
Authority + Capability + Means Gate
↓
Action
↓
Effect Receipt
↓
Observation
↓
Provenance / Freshness / Causal Binding
↓
State Update
↓
Continue / Replan / Reflect / Stop
```

The key rule is that neither reasoning nor observation is automatically executable truth.

## 2. Core invariants

```text
Reasoning != Authority
Action != Authority

Observation != GroundTruth
ToolResult != WorldState
ObservedAfterAction != CausedByAction

Reflection != VerifiedLesson
Failure != LearningSignalWithoutValidEvaluation
TrajectoryMemory != UniversalPolicy
PastSuccess != CurrentValidity

RewardSignal != GoalSatisfaction

SearchBranch != AuthorizationToCauseRealEffect
SimulationBranch != RealExecutionBranch
BestSearchNode != ExecutableFinalAction

MoreIterations != MoreProgress
SearchBudget != Authority
```

## 3. Observation contract

Observations used for material state transitions should preserve, where applicable:

- source/tool identity;
- timestamp and freshness;
- entity binding;
- action/effect-receipt binding;
- environment/state version;
- partial/complete status;
- error status;
- uncertainty or confidence.

Temporal proximity alone is not sufficient causal evidence.

## 4. Reflexion and memory promotion

A verbal reflection is a candidate lesson, not memory authority.

```text
Trajectory
↓
Outcome evidence
↓
Evaluator
↓
Reflection candidate
↓
Scope + provenance + contradiction check
↓
Bounded lesson
↓
Memory
```

Memory entries should carry the task/environment scope and invalidation conditions that make later reuse auditable.

## 5. Search–execution separation

Tree search may explore hypothetical futures, but a search branch is not permission to create a real-world effect.

For branches capable of external effects, the runtime should distinguish:

```text
simulated/sandbox branch
!=
real-effect branch
```

Material branches need state isolation, scoped credentials, effect receipts, compensation/reset semantics when available, and a final commit gate.

## 6. Evaluator and reward integrity

Positive reward is evidence, not proof of goal satisfaction. Reward hacking, proxy mismatch, stale goals, partial completion, shared generator/evaluator blind spots, and adversarial tool feedback must remain representable.

## 7. Loop termination

Interactive agents need explicit retry, branch, tool/API and cost budgets plus progress, freshness, escalation and safe-exit conditions.

Failure does not grant more authority or unlimited budget.

## 8. Final commit revalidation

Before executing the selected branch, revalidate:

```text
current state
current authority
current goal
already-created effects
final candidate verification
```

A branch can become stale while search is running.

## 9. Local structural evidence

The following local synthetic tests support the structure:

- v0.256 Observation Provenance & Freshness Closure
- v0.257 Action–Observation Causal-Binding Closure
- v0.258 Reflection-to-Memory Promotion Gate
- v0.259 Trajectory Scope & Replay-Contamination Closure
- v0.260 Search-Branch Effect-Isolation Closure
- v0.261 Evaluator & Reward-Integrity Closure
- v0.262 Agent Loop-Termination & Budget-Governance Closure
- v0.263 Search-to-Commit Final-Revalidation Closure

Boundary:

```text
local simulation != closure
```

These tests are structural local evidence only. They do not advance remote or production verification.

## 10. Relationship to other Bridge RFCs

This RFC composes with:

- Adaptive Deliberation Policy;
- State-Bound Planning and Replanning;
- Means-Constrained Agency;
- Reality-Final Verification;
- Generator–Verifier Independence;
- Effect Receipts and Recovery;
- Agentic Containment.

Bridge should model agent interaction as an auditable typed state-transition system rather than as unstructured free-form action loops.
