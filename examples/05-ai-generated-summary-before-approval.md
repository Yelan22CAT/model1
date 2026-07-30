# Showcase Case 5 — AI-Generated Summary Before Management Approval

> Public-safe composite case. This is not a transcript of any single organization or AI workflow.

## Situation

A manager asks for a short decision brief based on several source documents: an operating report, a vendor response, email correspondence, and a draft action plan.

An AI assistant produces a clear summary and recommends approval. The summary is concise and plausible, but it combines verified facts, inferred explanations, and unsupported details without marking the difference.

## Proposed next action

Send the AI-generated brief to management as the final decision package and proceed with approval.

## Known facts

- multiple source documents exist;
- the documents have different dates and authority levels;
- the AI summary is not an original source;
- several statements in the summary are supported by only one source;
- at least one claim combines information from separate documents;
- management approval could create operational and financial consequences;
- the summary has not yet passed a claim-level human review.

## Examples of claim drift

| AI-generated claim | Source condition | Correct treatment |
| --- | --- | --- |
| “The control has been fully tested.” | a test was planned; final result absent | mark as unknown / pending |
| “The vendor can recover within four hours.” | target appears in a draft; no test evidence | mark as self-attested or unverified |
| “All owners approved the plan.” | one owner replied; others were copied | remove or narrow the claim |
| “The issue is resolved.” | immediate symptom was removed; closure evidence absent | state temporary containment only |

## Evidence direction

**Direction: `0` — unresolved.**

The source set may support parts of the proposed plan, but the AI-generated recommendation cannot be accepted until material claims are traced and corrected.

## Risk signal

**Signal: 🔴 Red for final approval use; 🟡 Yellow for internal drafting use.**

Using the document as a draft is reversible. Using it as final evidence for a consequential decision would transfer unsupported claims into management approval.

## Risk decomposition

### Source-authority risk

The summary may appear more authoritative than the underlying records because uncertainty and source hierarchy have been compressed.

### Claim-combination risk

Facts from separate versions, dates, owners, or events may be merged into one stronger claim than any source supports.

### Accountability risk

A decision owner may believe the analyst or AI has already verified the evidence, while the analyst may believe management will identify any issue. Responsibility becomes distributed and unclear.

### Reversibility risk

Once the brief is used for approval, spending, access, deployment, or external communication may begin. Correcting the record later becomes more difficult.

## Expected controls

- source hierarchy defined;
- material claims linked to supporting records;
- fact, inference, and unknown clearly separated;
- stale and conflicting sources identified;
- unsupported claims removed or narrowed;
- decision-changing unknowns stated;
- consequence and rollback reviewed;
- accountable human reviewer signs off.

## Recommended control response

1. freeze final distribution of the AI-generated brief;
2. extract the material claims into a review table;
3. link each claim to the source and document version;
4. mark verified, inferred, pending, contradicted, or unknown;
5. remove claims that exceed the source;
6. state the unresolved issues that could change the decision;
7. revise the recommendation and risk signal;
8. route the corrected package to the accountable human owner.

## Claim-review table

| Claim | Source | State | Consequence if wrong | Required action |
| --- | --- | --- | --- | --- |
| control tested | test plan only | pending | false assurance | obtain test result |
| recovery target met | draft target | unverified | resilience gap hidden | request evidence |
| all owners approved | incomplete correspondence | contradicted | authorization gap | obtain explicit approval |
| issue resolved | containment record only | inferred | premature closure | define closure evidence |

## Reversal condition

The direction may move to `+` only when:

- material claims are traceable;
- unsupported details are removed;
- decision-changing unknowns are resolved or explicitly accepted;
- the recommendation matches the evidence;
- the responsible owner understands the remaining risk.

## Compact decision-support output

```text
Conclusion: Use the AI output only as a draft, not as final approval evidence.
Decisive evidence: the summary contains claims that exceed or merge the source material.
Unknowns: test result, recovery evidence, complete owner approval, closure status.
Evidence direction: 0
Risk signal: Red for final approval; Yellow for controlled drafting.
Control gap: no claim-level source trace or accountable verification.
Reversal condition: claims traced, unsupported details removed, unknowns resolved or accepted.
Safe next action: perform a claim-by-claim source review and issue a corrected brief.
Human Final Gate: management approval remains with the accountable owner.
```

## Capability demonstrated

- AI-output evaluation;
- source hierarchy and traceability;
- hallucination and claim-drift control;
- version and authority awareness;
- uncertainty preservation;
- consequential-use gating;
- human-in-the-loop accountability;
- concise management communication.

## Public boundary

This case does not reproduce a real email, vendor response, management package, organization, contract, or AI transcript. It demonstrates a general AI-governance and evidence-review pattern.