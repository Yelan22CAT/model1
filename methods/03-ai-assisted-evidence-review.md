# Method 3 — AI-Assisted Evidence Review

## Purpose

This method shows how AI can help organize and compare information without becoming the source of truth or final decision-maker.

It is designed for work such as:

- summarizing documents or issue records;
- comparing vendor responses;
- preparing a risk review;
- extracting claims and missing information;
- drafting an escalation brief;
- identifying contradictions across sources;
- preparing a management decision package.

## Core rule

> AI may organize evidence. It may not silently create evidence, authority, or approval.

## Workflow

```text
Source material
→ AI extraction and organization
→ claim-by-claim source check
→ fact / inference / unknown separation
→ consequence and reversibility review
→ human correction and approval
→ controlled use
```

## Step 1 — Lock the task

Define what the AI is being asked to do.

Acceptable task examples:

- extract key claims from supplied documents;
- compare two versions of a procedure;
- identify missing vendor evidence;
- draft a summary using only cited material;
- convert an issue description into a structured review template.

The task should state what the AI must not do, such as:

- invent missing facts;
- infer authorization;
- make a professional determination;
- contact people or systems;
- approve or execute an action.

## Step 2 — Identify authoritative sources

Record the source hierarchy before analysis.

Example:

```text
1. signed contract or approved policy
2. current controlled procedure
3. original record or system entry
4. verified correspondence
5. working notes
6. AI-generated summary
```

An AI summary remains below the original source.

## Step 3 — Extract atomic claims

Break the material into claims small enough to verify independently.

Weak claim:

> The vendor has strong resilience controls.

Better atomic claims:

- the vendor supplied a continuity plan;
- the plan identifies a recovery location;
- the plan was last tested on a stated date;
- evidence of the test result was not supplied;
- the contract does or does not define notification obligations.

Atomic claims reduce the risk that one supported detail makes an entire paragraph appear verified.

## Step 4 — Assign source state

For every material claim, mark:

- **Verified:** supported by an authoritative source;
- **Observed:** directly visible but not independently confirmed;
- **Inferred:** interpretation based on stated evidence;
- **Pending:** source requested but not received;
- **Unknown:** insufficient information;
- **Contradicted:** reliable sources conflict;
- **Deprecated:** no longer current.

## Step 5 — Test traceability

A reviewer should be able to answer:

- Which source supports this claim?
- Is the source current?
- Does the source support the whole claim or only part of it?
- Has context been omitted?
- Did the AI combine separate events, versions, or entities?
- Would the conclusion change if this source were removed?

A fluent paragraph without traceable support is not evidence.

## Step 6 — Review consequence and reversibility

The required review depth depends on how the output will be used.

### Lower consequence

- internal brainstorming;
- draft structure;
- non-binding comparison;
- question generation.

### Higher consequence

- vendor approval;
- public release;
- access or permission change;
- spending or contract commitment;
- employment decision;
- safety or operational release;
- legal, regulatory, medical, or financial use.

Higher-consequence use requires stronger source checking and explicit human ownership.

## Step 7 — Produce the two-axis output

### Evidence direction

- `+` — verified evidence supports the proposed conclusion;
- `0` — evidence is incomplete, mixed, or unresolved;
- `-` — verified evidence opposes the proposed conclusion.

### Risk signal

- **Green:** low-consequence use, traceable sources, and no material stop trigger;
- **Yellow:** unresolved claims, stale sources, or reduced reversibility require review;
- **Red:** unsupported material would enter a consequential decision or execution path.

## Step 8 — State reversal conditions

Every material conclusion should state what would change it.

Examples:

- receipt of current independent test evidence;
- confirmation from the accountable owner;
- correction of a source record;
- discovery that the document version is obsolete;
- evidence that two apparently related records concern different events.

## Step 9 — Apply the Human Final Gate

The final reviewer must:

- inspect the material sources;
- correct unsupported claims;
- confirm the intended audience and use;
- check privacy and authorization;
- understand the consequence;
- decide whether the output may be used.

The Human Final Gate is accountability placement, not a decorative approval box.

## Compact output

```text
Task:
Intended use:
Authoritative sources:
Claims verified:
Claims inferred:
Claims unknown or pending:
Contradictions:
Evidence direction: + / 0 / -
Risk signal: Green / Yellow / Red
Reversal condition:
Safe next action:
Human reviewer / final owner:
```

## Quality checks

Before use, confirm:

- no unsupported detail has been added;
- dates, names, quantities, and versions match the source;
- separate entities or events have not been merged;
- uncertainty has not been rewritten as certainty;
- source wording has not been overstated;
- the output does not disclose unnecessary private information;
- no action is triggered automatically.

## Common failure patterns

- treating the AI answer as a source;
- accepting citations without checking what they support;
- allowing a summary to replace the original record;
- using confidence of language as confidence of evidence;
- forcing an unresolved result into approval or rejection;
- letting a low-risk drafting workflow become a high-consequence execution workflow without a new gate.

## Boundary

This method supports structured analysis and documentation. It does not authorize autonomous execution or replace qualified legal, regulatory, safety, engineering, privacy, security, medical, financial, or management judgment.