# RFC — Adaptive Workload Routing, Reasoning Budget & Structural Distillation

> Status: Experimental extension / Not Production Ready

## Motivation

Modern agent models increasingly differ not only in benchmark score, but in
context capacity, reasoning controls, modality support, tool reliability,
latency, cost, privacy boundary, provider identity, and runtime behavior.

Bridge should therefore route by a typed workload contract rather than by a
single "best model" score.

## 1. Reasoning budget is not authority

```text
MoreReasoning != MoreAuthority
```

Higher reasoning effort, longer context, more retries, or a slower path may
consume more compute, but they do not expand permissions, tool access, action
scope, or human-approval authority.

Reasoning budget belongs to the compute/routing plane, not the authority plane.

## 2. Context presence is not context trust

```text
ContextPresent != ContextTrusted
```

Large context windows can preserve more state, but may also preserve stale,
revoked, conflicting, poisoned, or superseded state.

Material context entries therefore need provenance, freshness, current
version/epoch, conflict state, and authority lifecycle binding.

## 3. Modality is not epistemic authority

```text
InputModality != EpistemicAuthority
```

Text, image, audio, video, and tool output are input channels. Their presence
does not automatically promote a claim to fact or authorize an action.

## 4. Routing is constrained optimization

A Bridge workload profile may include:

```text
semantic difficulty
context requirement
modality requirement
tool / schema capability
latency target
cost target
privacy boundary
data residency
runtime identity requirement
authority constraints
partial-effect / recovery state
```

Candidate models/runtimes are first filtered for correctness and trust
constraints. Optimization happens only inside the feasible set.

```text
BestBenchmarkScore != ValidRoute
```

A cheaper, faster, longer-context, or higher-scoring route is invalid if it
drops a required tool schema, modality, output contract, privacy boundary,
residency constraint, authority condition, or recovery state.

## 5. Popularity is an adoption signal, not capability proof

```text
Popularity != Capability
UsageVolume != ModelQuality
```

Blind or anonymous real-world traffic can be useful evidence of adoption and
workload fit, but it must remain separated from:
- price/free-access effects;
- default-router bias;
- promotional traffic;
- workload skew;
- provider concentration;
- benchmark evidence;
- model identity.

## 6. Mechanism should survive model disappearance

```text
ModelMayDisappear
MechanismShouldSurvive
```

Bridge should bind to capability contracts and verifiable routing profiles, not
to one vendor/model name. A preview or stealth model may disappear without
breaking the semantic architecture.

## 7. Structural distillation

Bridge prefers structural learning over black-box cloning:

```text
publicly observable behavior/design
→ identify strength
→ abstract mechanism
→ generalize
→ compatibility check
→ adversarial test
→ integration
```

```text
StructuralDistillation != WeightCloning
```

This RFC does not authorize restricted reverse engineering, proprietary-weight
copying, or bulk output extraction contrary to provider terms.

## Reference routing pipeline

```text
Task
↓
Semantic Difficulty Estimate
↓
Required Context
↓
Required Modality
↓
Capability Requirements
↓
Latency / Cost Target
↓
Trust / Privacy / Residency Envelope
↓
Reasoning Budget
↓
Model / Runtime Route
↓
Verification
```

## Local synthetic tests

Current local synthetic tests include:

- **v0.211** — reasoning-budget non-elevation;
- **v0.212** — long-context provenance and freshness;
- **v0.213** — workload-router constraint preservation;
- **v0.214** — blind-adoption / popularity evidence boundary.

These are structural tests only.

```text
local simulation != closure
```

## Verification boundary

This RFC does not claim:
- that any named preview model is universally superior to another model;
- that high traffic proves higher capability;
- that a stealth model's developer or training lineage is known;
- that local synthetic tests prove production routing safety.
