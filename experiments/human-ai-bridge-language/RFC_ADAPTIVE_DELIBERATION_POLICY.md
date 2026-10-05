# RFC — Adaptive Deliberation Policy

Status: **Experimental / Public-safe / Not Production Ready**

## Purpose

Bridge-0 separates **reasoning budget**, **reasoning strategy**, and **verification strategy**.

A harder task may justify more compute without receiving more authority. A high-risk task may require stronger verification even when the reasoning strategy is simple.

## Strategy families

```text
Direct / minimal reasoning
Sequential decomposition
Sample-and-aggregate
Branch/search/backtrack
Critique-and-refine
```

These are different tools, not a universal maturity ladder.

## Core invariants

```text
Consensus != Correctness
ManySamples != IndependentEvidence
MoreBranches != MoreTruth
SearchDepth != SearchQuality
SelfCritique != IndependentVerification
Convergence != Correctness
OneReasoningMode != UniversalStrategy
DeliberationStrategy != Authority
MoreReasoning != MoreAuthority
```

## Router

```text
Task
↓
difficulty / branching / uncertainty
↓
cost + latency budget
↓
risk / reversibility
↓
evidence requirement
↓
deliberation strategy
↓
candidate result
↓
verification strategy
```

## Independence boundary

Multiple samples can share the same prompt bias, model lineage, retrieval error, tool error, or hidden assumption.

Therefore:

```text
sample count != independence count
```

Tree search also depends on branch generation, pruning, state freshness, and judge quality.

Self-refinement can improve an answer while preserving the same generator/critic blind spot.

## Evidence boundary

The v0.246–v0.249 tests are **local synthetic structural tests only**.

```text
local simulation != closure
```
