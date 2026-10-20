# RFC — Multi-Interface Execution & Verifiable Task Factory

> Status: Experimental extension / Not Production Ready  
> This RFC does not change the v1.0-rc1 normative baseline by itself.

## Motivation

A real agentic task may expose the same underlying work state through more than
one interface:

- GUI / screen interaction;
- code or shell;
- MCP tools;
- API calls.

Bridge should therefore avoid binding one semantic task to one execution
surface. The semantic task, authority, evidence, state identity, and allowed
effects remain canonical; the interface is a route selected at execution time.

## Core distinction

```text
Task semantics != interface
Interface route != authority
Trace equality != semantic outcome equivalence
```

A different route is acceptable only if it preserves the same declared
semantic contract.

## Interface-plural execution contract

For each candidate route, Bridge should bind:

- canonical task identity;
- current state/version identity;
- required capabilities;
- route/interface identity;
- authority and scope;
- allowed effect surface;
- expected postconditions;
- evidence/provenance requirements;
- recovery and replay behavior.

A route switch after partial execution requires a fresh observation and
revalidation of material state before continuing.

```text
route switch
+ stale state assumption
= reject / re-observe
```

## Cross-interface state-equivalence oracle

When multiple interfaces expose the same underlying state, Bridge can use them
as differential views.

Example:

```text
same initial state
├─ GUI route
├─ MCP route
├─ API route
└─ code route
        ↓
compare canonical postconditions
+ prohibited side effects
+ state/version identity
```

The traces do not need to be identical. The semantic postcondition and effect
contract must be equivalent within the declared scope.

This provides a stronger test than checking that each interface succeeds in
isolation.

## Trajectory as a first-class verification artifact

For long-running agent execution, the final answer is insufficient evidence.

A Bridge trajectory should be able to bind, at minimum:

- task and plan identity;
- observation/state reference;
- chosen interface and route;
- requested action;
- tool/runtime result;
- effect receipt;
- state transition;
- route-switch reason, if any;
- verifier result;
- recovery/replay metadata where applicable.

A trajectory is evidence about execution history. It is not automatically
proof that each model rationale is correct.

## Verifiable task factory

Bridge testing should be able to generate or assemble interactive tasks from
public-safe specifications, documentation, fixtures, and synthetic state.

Each generated task should include:

- explicit initial state;
- available interface surfaces;
- expected postconditions;
- forbidden effects;
- deterministic or independently checkable verifier;
- reset/replay path;
- capability and authority boundaries.

Hybrid tasks that expose the same state through two or more interfaces are
especially valuable because they permit cross-interface differential testing.

## Harness boundary

The model is not the whole agent.

```text
model
+ harness
+ memory/context management
+ interface adapters
+ state observation
+ verification
= executable agent system
```

Bridge therefore evaluates the execution stack as a composed system rather
than attributing end-to-end correctness to the model alone.

## Failure classes to test

- stale GUI view while API/MCP state has advanced;
- route switch that loses state/version binding;
- fallback route that broadens authority;
- hidden side effect present only on one interface;
- duplicate effect after partial execution;
- interface alias pointing to a different resource;
- semantically different tool implementations sharing one label;
- code/shell path bypassing a higher-level guard;
- unavailable route silently replaced by a broader route;
- successful trace with incorrect final canonical postcondition.

## Evidence boundary

This RFC is inspired by public evidence that contemporary computer-use agent
systems can combine GUI, code, MCP, and API interfaces, use long-horizon
harnesses, and publish trajectory-level benchmark evidence.

Bridge adopts the general mechanisms, not any vendor-specific benchmark claim
or proprietary implementation.

Local synthetic tests do not establish production closure.

```text
local simulation != closure
```
