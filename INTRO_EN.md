# Model 1 Intro Tutorial

Updated: 2026-07-28  
Scope: Model 1 v1.0 / first-person human-controlled judgment guardrail only

## What this is

Model 1 v1.0 is a minimal judgment and stop-loss guardrail.

It does not make decisions for you. It helps you pause before real-world action and check:

- what the next action actually is;
- what is fact, inference, assumption, and unknown;
- whether current evidence supports, fails to resolve, or opposes the path;
- whether a boundary is being crossed;
- whether the action can still be stopped, corrected, rolled back, or exited.

In one sentence:

> Model 1 is not an answer machine.  
> It is a judgment interface and brake check before action.

## When to use it

Use it before actions such as:

- sending an important email;
- placing an order or making a payment;
- approving a change;
- publishing content or deploying code;
- making a work, relationship, money, safety, or access decision;
- using AI-generated content in the real world;
- continuing under urgency, fatigue, emotion, or incomplete information.

## When not to use it

Model 1 v1.0 is not for:

- analyzing, diagnosing, judging, or ranking other people;
- persuasion, manipulation, pressure, or control;
- predicting entire relationships, organizations, or markets;
- replacing medical, legal, financial, safety, or mental-health advice;
- autonomous execution by AI;
- proving what another person “really is.”

This is a first-person judgment tool. It is not a third-person judge or control system.

## Step 1: Write the next action

Write down:

> The next real-world action I am about to take is: ______

If the next action is unclear, do not continue yet.

## Step 2: Separate fact, inference, and unknown

Classify the information:

- **Fact / observation:** directly seen, recorded, or verified;
- **Inference / hypothesis:** a bounded explanation that may fit the evidence;
- **Unknown / verification pending:** missing, conflicting, stale, or unchecked information.

Do not treat AI fluency, repetition, or confidence as verification.

## Step 3: Assign evidence direction `+ / 0 / -`

For the proposed action, use a bounded direction:

- `+` — current evidence supports the path;
- `0` — evidence is insufficient, mixed, or unresolved;
- `-` — current evidence opposes the path.

`0` is a valid result. It is not hidden approval, hidden rejection, or failure.

Evidence direction describes the present evidence. It does not authorize action.

## Step 4: Check consequence, boundary, and reversibility

Ask:

- What real-world effect can this action create?
- Is a safety, authorization, contractual, privacy, consent, validation, or personal boundary being crossed?
- Are time, money, responsibility, exposure, or safety costs rising?
- Can the action still be withdrawn, corrected, or rolled back?
- Who owns exceptions, maintenance, rollback, and final approval?

Evidence may be gray. A clear boundary must not be washed away by complexity.

## Step 5: Assign the action-risk signal

### 🟢 Green｜No current stop-loss trigger

No stop-loss condition is currently identified from the stated input.

This is not a guarantee and not permission for automatic execution.

### 🟡 Yellow｜Slow down and verify

Yellow may apply when:

- key facts are incomplete;
- the source is unclear;
- consequence or cost is increasing;
- reversibility is shrinking;
- AI output is fluent but unverified;
- responsibility or rollback is unclear.

Action:

> Pause.  
> Verify the missing facts.  
> Preserve options.  
> Review again.

### 🔴 Red｜Freeze, escalate, or exit

Red may apply when:

- a safety or authorization boundary is crossed;
- required validation is missing;
- key facts cannot be verified;
- consequence is highly irreversible;
- AI output would directly trigger real-world execution;
- the cost of being wrong is high.

Action:

> Do not execute automatically.  
> Freeze and route to human review or proper escalation.  
> Exit if needed.

## Do not confuse the two output axes

Model 1 uses:

1. **Evidence direction:** `+ / 0 / -`
2. **Risk signal:** Green / Yellow / Red

They answer different questions:

- Direction: What does the current evidence say about the path?
- Signal: How strongly should the person pause before acting?

Examples:

- Evidence may support a path (`+`) while the action remains Yellow because rollback is weak.
- Evidence may remain unresolved (`0`) while a mandatory validation gap requires Red.
- Evidence may oppose a path (`-`) without dramatic language; stopping or choosing a more reversible alternative may be enough.

## Minimal output format

A useful public output should normally show:

```text
Conclusion:
Decisive evidence:
Unknowns:
Evidence direction: + / 0 / -
Risk signal: Green / Yellow / Red
Boundary status:
Cost / reversibility status:
What would reverse the conclusion:
One safe next action:
Human Final Gate: the final decision remains mine
```

## Simple example

You ask AI to draft a purchasing email to a supplier.

Before sending, check:

- Is the order number from the original source?
- Is the quantity verified?
- Is the part description and version consistent?
- Is the recipient correct?
- Will sending trigger purchasing, payment, or production?

If key fields conflict:

```text
Evidence direction: 0 | unresolved
Risk signal: Yellow | pause and reconcile the source
```

If the message would trigger high-cost purchasing while required fields remain unverifiable:

```text
Evidence direction: 0 or -
Risk signal: Red | do not send; route to human review
```

## Final Gate

AI-generated content is always a draft.

Any action with real-world consequences must pass a final human-controlled review before execution.

The Final Gate checks:

- key facts and sources;
- inferences and unknowns;
- evidence direction;
- recipient or execution target;
- file version, quantity, amount, and date;
- boundary, consequence, and responsibility;
- whether the action can still be stopped or rolled back.

No Final Gate, no real-world execution.

## Public boundary

This tutorial exposes only the minimal public judgment interface. It does not publish:

- private cases or identifiable narratives;
- private observers, thresholds, or calibration chains;
- detailed market, interaction, allocation, or pacing models;
- anti-poisoning implementation internals;
- hidden runtime or autonomous execution logic;
- the complete private engine.

Model 1 does not choose for you, carry the consequence for you, or control other people.

Final action must remain human-controlled.
