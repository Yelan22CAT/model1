# Comprehension Debt

## Definition

**Comprehension debt** is a qualitative description of AI-generated conclusions, dependencies, decisions, or actions that have become operationally relevant before accountable humans have sufficiently understood, verified, or integrated them.

It is not a validated quantitative metric.

## Why it matters

A system can be locally correct while the human supervisory layer becomes progressively less able to explain:

- what the system currently believes;
- which conclusions depend on which earlier outputs;
- what remains uncertain;
- what permissions are active;
- why the next action is justified;
- how to return to a known safe state.

That can create a gap between nominal oversight and effective oversight.

## Qualitative relationship

```text
Comprehension Debt increases
+
Autonomy increases
+
External reach increases
+
Reversibility decreases
=
Higher priority for pause, review, or freeze
```

A compact form is:

```text
Context uncertainty × consequence risk ↑
→ review depth ↑
```

## Signals that debt may be rising

Examples include:

- long chains of AI-generated claims are reused without independent checking;
- humans can approve outcomes but cannot reconstruct the path that produced them;
- system state changes faster than operators can review it;
- generated code, plans, or proofs become prerequisites for later work before they are understood;
- exceptions and unresolved warnings accumulate;
- human reviewers begin relying on prior AI summaries instead of source evidence;
- multiple agents recursively depend on each other's unverified outputs;
- rollback becomes harder because no one can clearly identify the last trusted state.

## What this concept does not mean

Comprehension debt does not imply that humans must understand every low-risk token, intermediate calculation, or implementation detail before any AI system can continue.

The concept is most useful when the unresolved material becomes **consequential**, **structurally reused**, **hard to reverse**, or **necessary for human control**.

## Suggested response ladder

```text
Low debt / low consequence
→ continue with ordinary review

Rising debt
→ slow down, compress, explain, verify

Material debt + consequential action
→ Human Catch-up Gate

Frozen state
→ review + Dual-Key Resume Lock
```

## Core distinction

```text
Correctness
≠
Human comprehension
≠
Knowledge integration
≠
Authorization to continue indefinitely
```
