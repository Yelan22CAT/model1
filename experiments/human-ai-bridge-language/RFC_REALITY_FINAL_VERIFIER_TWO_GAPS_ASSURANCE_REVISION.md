# RFC — Reality-Final Verification, Requirement/Model Gaps & Assurance Revision

Status: **Experimental / Public-safe architecture RFC / Not Production Ready**

## Motivation

A system can pass tests, satisfy a formalized requirement set, and still fail its stakeholders after deployment.

The reason is that three different objects are routinely collapsed:

```text
Stakeholder intent
!=
Recorded requirements

Deployment reality
!=
Development/world model

Requirement satisfaction under a model
!=
What a bounded evaluator actually checks
```

Bridge should make these gaps explicit instead of treating verification as a one-time closure event.

## Core model

```text
Stakeholder Intent (I)
        ↓
Requirements (R)
        ↓
Implementation / Agent
        ↓
Evaluator (E) under World Model (M)
        ↓
Deployment in Reality (W)
```

We distinguish:

```text
Requirement Gap = mismatch(I, R)
Model Gap       = mismatch(W, M)
Evaluation Gap  = incomplete coverage of R under M by E
```

The Evaluation Gap may sometimes be reduced substantially, or even closed for a bounded formal model.

That does **not** imply the Requirement Gap or Model Gap are closed.

## Normative invariants

```text
RequirementConformance != StakeholderIntentSatisfaction

ModelValidity != RealityValidity

EvaluatorPass != DeploymentAcceptability

FormalProof != IntentCompleteness

PreviouslyAccepted != CurrentlyAcceptable

BroadKnowledge != LocalContext

OpenWorldAssurance != PermanentClosure
```

## Assurance-Revision Loop

Bridge treats deployment evidence as a first-class input to assurance.

```text
Intent
↓
Bridge semantic contract
↓
Requirements + constraints + authority + evidence
↓
World/deployment model
↓
Implementation
↓
Predeployment verification
↓
Deployment observation
↓
Reality evidence
↓
Diagnose gap
↓
Revise requirements / model / evaluator / policy / runtime
↓
Reverify
```

A PASS is therefore always scoped to:

- requirement version;
- world-model version;
- evaluator version;
- runtime/environment identity;
- authority/policy epoch;
- evidence time window.

## Bridge is a gap-narrowing interface, not an intent oracle

Bridge does not claim to infer complete human intent.

Its role is to:

- preserve explicit ambiguity;
- distinguish facts, hypotheses and unknowns;
- expose omitted assumptions;
- record trade-offs and conflicts;
- make constraints machine-verifiable;
- preserve provenance and freshness;
- route consequential ambiguity back to accountable humans.

```text
Bridge != Intent Oracle
Bridge = Gap-Narrowing Semantic Interface
```

## Human escalation

Human review is not required for every low-risk operation.

It becomes first-class when uncertainty and consequence interact:

```text
Ambiguity × Consequence -> ClarifyOrEscalate
```

Examples include:

- conflicting requirements;
- tacit or changing stakeholder intent;
- privacy/security trade-offs;
- irreversible effects;
- novel deployment failures;
- low-evidence/high-impact decisions.

## Context asymmetry

A model can have broad general knowledge and still lack task-local context.

```text
BroadKnowledge != LocalContext
```

Useful local context may include:

- current user state;
- organization policy;
- recent actions;
- physical environment;
- task history;
- private constraints.

Local context is useful only when provenance, freshness, consent and privacy scope are explicit.

```text
MoreContext != MoreTrustedContext
```

## Open-world non-closure

In an open, changing environment:

```text
successful predeployment verification
-> provisional assurance

not

successful predeployment verification
-> permanent closure
```

New workload classes, failures, dependencies, attacks, regulations or changed stakeholder intent can invalidate a prior acceptance.

## Relationship to formal verification

Formal methods remain valuable.

They can greatly reduce the Evaluation Gap for a bounded formal model.

But stronger formalization over a narrower specification can still omit:

- implicit goals;
- contextual exceptions;
- priority ordering;
- social or organizational norms;
- future adaptation requirements.

Therefore:

```text
FormalProof != IntentCompleteness
```

## Cross-layer infrastructure implication

AI infrastructure increasingly uses cross-layer optimization across model, runtime, scheduler, memory, network, storage and accelerator layers.

Bridge permits explicit cross-layer contracts but rejects invisible dependency creation.

```text
LocalOptimization != SystemOptimization

CrossLayerOptimization != InterfaceErasure
```

Cross-layer changes must preserve or explicitly revise:

- global SLOs;
- semantic contracts;
- recovery guarantees;
- security boundaries;
- portability assumptions;
- ownership/version boundaries;
- observability.

## Evidence boundary

This RFC is architecture guidance, not a claim that any one benchmark, formal method, endpoint-context mechanism or world model eliminates the gaps.

All synthetic adversarial tests associated with this RFC remain:

```text
STRUCTURAL FINDING / LOCAL SYNTHETIC TEST ONLY

local simulation != closure
```

## Research lineage

This RFC is informed by the public two-gap framework in:

- Alexander Krentsel, Shubham Agarwal, Mert Cemri, Shu Liu, Sidharth Sankhe, Ziming Mao, Matei Zaharia, Ion Stoica, *Reality Is the Final Verifier: On Two Key Gaps in Agentic Software Engineering*, arXiv:2609.12039 (2026).

Bridge extends that framing with explicit semantic-state, authority, provenance, context-freshness and runtime-verification contracts.
