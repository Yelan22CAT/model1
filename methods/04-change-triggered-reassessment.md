# Method 04 — Change-Triggered Reassessment

## Purpose

A control, vendor assessment, technical approval, or AI evaluation is not permanently valid because it was valid once.

This method is used when a prior decision remains on record but the operating state may have changed.

The public principle is simple:

> Prior approval is evidence about a prior state, not automatic authority over the current state.

This is especially relevant to operational risk, GRC, third-party risk, change governance, resilience, and AI governance.

## When to use it

Use a triggered reassessment when a material change affects one or more of the following:

- process flow;
- system or model version;
- vendor service or ownership;
- data access or data sensitivity;
- approval path;
- operating environment;
- dependency or fallback path;
- control owner;
- evidence source;
- consequential-use context.

The method does not assume that a change creates a failure. It asks whether the old evidence is still valid enough for the new state.

## Review sequence

### 1. Identify the prior decision

Record:

- what was previously approved or accepted;
- what evidence supported that decision;
- which operating state that evidence described;
- who owned the decision.

### 2. Identify the change trigger

Describe the change without immediately classifying it as safe or unsafe.

Examples:

- workflow changed;
- vendor expanded access;
- model or software version changed;
- control ownership changed;
- recovery path changed;
- source document was replaced;
- service that was described as local introduced a remote dependency.

### 3. Reclassify evidence state

For each decision-changing item, mark it as:

- **Current** — still directly describes the present state;
- **Stale** — once valid, but may no longer describe the present state;
- **Unsupported** — asserted without adequate evidence;
- **Unknown** — information required for the decision is not yet available;
- **Opposed** — current evidence directly conflicts with the proposed path.

Stale evidence is not automatically false. It is simply not strong enough to carry the same decision weight without refresh.

### 4. Determine what the change invalidates

Ask:

- Which assumptions no longer hold automatically?
- Which controls need to be re-observed or re-tested?
- Which dependencies changed?
- Did consequence or reversibility change?
- Did the accountable owner change?
- Did a previously bounded risk become broader?

### 5. Reassess the consequential action

Use the standard public interface:

```text
Current facts / inferences / stale evidence / unknowns
→ Evidence direction: + / 0 / -
→ Consequence and reversibility
→ Control gap and accountable owner
→ Risk signal: Green / Yellow / Red
→ One safe and reversible next action
→ Human Final Gate
```

### 6. Define the minimum refresh needed

The goal is not to repeat every historical review.

Refresh only the evidence made decision-relevant by the change.

Examples:

- observe the control under the new workflow;
- obtain current vendor evidence for the expanded service;
- verify current network behavior after a deployment change;
- retest decision-changing AI claims against current sources;
- confirm that recovery and rollback remain available.

### 7. Record reversal and closure conditions

A reassessment should specify:

- what evidence would support proceeding;
- what evidence would require continued hold or escalation;
- what conditions close the reassessment;
- when another material-change trigger would reopen it.

## Compact output

```text
Prior decision:
Material change:
Evidence made stale or uncertain:
Current decisive evidence:
Control gap:
Evidence direction:
Risk signal:
Reversal condition:
Required refresh:
Accountable owner:
Human Final Gate:
```

## What this demonstrates

For an employer, this method demonstrates:

- temporal validity awareness;
- change-triggered control testing;
- evidence refresh proportional to risk;
- distinction between historical assurance and current assurance;
- controlled exception handling;
- concise reassessment documentation;
- human-owned decision authority.

## Public boundary

This method does not disclose private thresholds, calibration chains, observer packs, internal promotion logic, or proprietary incident history.

It is a public control method, not the complete private engine.