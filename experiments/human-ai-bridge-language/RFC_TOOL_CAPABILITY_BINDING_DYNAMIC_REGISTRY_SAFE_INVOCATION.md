# RFC — Tool Capability Binding, Dynamic Registry & Safe Invocation

> Status: Experimental / Not Production Ready

## Purpose

Tool use expands an agent's capability surface. It must not silently expand the agent's authority surface.

This RFC treats tools as typed, versioned capability contracts rather than opaque function names.

## Control path

```text
Intent
↓
Tool discovery
↓
Tool identity / version binding
↓
Functional fit
↓
Capability / authority / policy checks
↓
Argument construction
↓
Semantic validation / taint checks
↓
Runtime availability recheck
↓
Effect-class / commit gate
↓
Invocation
↓
Effect receipt
↓
Output provenance / trust classification
↓
State update / next tool / stop
```

## Core invariants

```text
ToolExists != ToolAuthorized
ToolAvailable != CapabilityGranted

KnownTool != CurrentTool
DocumentationMatch != RuntimeSchemaMatch

SchemaValid != SemanticallyValid
ValidArguments != SafeArguments

BestFunctionalTool != SafestAuthorizedTool

ToolOutput != TrustedInstruction
ReturnedSuccess != VerifiedEffect

EachToolCallValid != ToolChainAuthorized

ToolToken != ToolIdentity
LearnedToolMapping != CurrentToolBinding

ToolDiscovered != ToolUsableNow

ValidToolCall != AuthorizedEffect
RetryableCall != IdempotentEffect
```

## Tool contract

A Bridge tool contract should be able to represent, as applicable:

```text
tool_id
provider
semantic_version
schema_version
input_semantics
output_semantics
capabilities
required_authority
effect_class
tenant / region scope
data / network / secret scope
runtime availability
quota / cost policy
trust / provenance
validity window
receipt semantics
recovery / compensation
```

## Selection

Functional match is necessary but insufficient.

Selection should also preserve least privilege and current runtime constraints. A read-only task should not prefer a broader write-capable or administrative tool simply because that tool can perform the same function.

## Registry freshness

Tool descriptions can come from model weights, prompt context, retrieval, or a runtime registry. None of these should be assumed permanently current.

The runtime registry is the source of truth for current binding and availability.

Material changes include:

- API version changes;
- removed endpoints;
- renamed parameters;
- deprecation;
- schema changes;
- regional or quota changes;
- updated policy or pricing constraints.

## Argument semantics

Schema validation only establishes structural conformance.

A schema-valid call may still be unsafe because of:

- wrong units;
- wrong entity binding;
- unsafe values;
- tainted input;
- silent defaults;
- cross-field constraint violations.

Bridge should preserve semantic types and constraints above ordinary JSON/schema validity.

## Tool-output trust

External tool output is evidence/data, not authority.

It may contain stale state, hostile prompt text, malicious metadata, poisoned documents, or spoofed success messages.

```text
ToolOutput != TrustedInstruction
```

Effect success should be supported by an effect receipt or equivalent runtime evidence where material.

## Tool chains

Locally valid calls can compose into an invalid chain.

A chain can widen scope, forward credentials, cross tenants, convert untrusted content into commands, or lose provenance.

Therefore:

```text
EachToolCallValid != ToolChainAuthorized
```

End-to-end scope, provenance, authority, and effect semantics must survive composition.

## Generative tool identity

ToolGen-style learned tool tokens can reduce retrieval overhead, but a generated token should not be the final executable identity.

Preferred path:

```text
generated tool token
↓
stable tool identity
↓
current registry entry
↓
version / schema / policy / availability recheck
↓
invocation
```

This protects against stale learned mappings, token collisions, alias drift, removed tools, and rapid tool churn.

## Hybrid discovery

Retrieval-aware selection can adapt to changing documentation but depends on retrieval quality. Generative selection is efficient but can become stale.

Bridge should support a hybrid path:

```text
learned candidate
+ current registry
+ selective retrieval when needed
```

## Effect classes

Tool interfaces should expose effect classes such as:

```text
pure / read-only
reversible write
external communication
financial / contractual
destructive / irreversible
privileged administration
physical-world effect
```

Higher-effect classes require stronger commit gates.

Material actions may require:

- preview / dry run;
- explicit authority;
- state/version binding;
- idempotency keys;
- compensation plans;
- durable effect receipts;
- final revalidation.

## Retry semantics

Transport retryability does not imply idempotent real-world effects.

```text
RetryableCall != IdempotentEffect
```

Retries should bind to effect identity where possible.

## Local structural tests

The associated local campaign covers:

- v0.264 — tool existence vs authorized capability;
- v0.265 — registry freshness / version drift;
- v0.266 — semantic argument safety;
- v0.267 — least-privilege tool selection;
- v0.268 — tool-output trust / taint;
- v0.269 — tool-chain confused deputy;
- v0.270 — generative tool-token identity / churn;
- v0.271 — discovery vs runtime availability;
- v0.272 — side-effect classification / commit gate.

All evidence remains:

```text
STRUCTURAL FINDING / LOCAL SYNTHETIC TEST ONLY

local simulation != closure
```

## Relationship to other RFCs

This RFC extends:

- State-Bound Planning, Replanning & Reality Checkpoints;
- Observation-Grounded Agency;
- Heterogeneous Semantic Lowering & Capability Contract;
- Multi-Interface Execution;
- Policy-Plane Separation;
- Reality-Final Verification;
- Semantic-First AI Programming Assurance.

It does not replace them.
