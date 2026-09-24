# 12 — Bounded Judgment Middleware and Selective Agent Coordination

## Purpose

Use small, bounded judgment steps inside an AI-assisted workflow without promoting a fast classifier or judge into an unrestricted controller.

## Core pattern

```text
Main model / worker
→ bounded decision point
→ narrow judge or deterministic rule
→ logged effect
→ fallback / escalation when uncertain
```

Examples include context admission, drift checks, rewind triggers, completion verification, constraint checks, and deciding whether a finding is worth sharing with another agent.

## Decision-point contract

Each point should expose: question, state slice, candidate judge, mode (off / shadow / active), effect, fallback, hard rules before model, audit fields, and rollback path.

## Shadow-first activation

```text
candidate verdict
→ log only
→ compare with baseline and observed outcome
→ calibrate
→ activate only if useful
```

## Selective coordination

```text
Agent finding
→ Publish Gate
→ shared board
→ Relevance Gate
→ relevant recipient only
```

A delivered finding is evidence or a hypothesis, not an instruction. Disagreement may be marked supports / supersedes / contradicts and should trigger verification rather than majority-vote erasure.

## Authority boundary

Hard safety, permission, privacy, CI and release rules remain above model confidence.

## Boundary

This document does not publish private thresholds, production credentials, hidden runtime packs, unrestricted permissions, or the full private orchestration engine.
