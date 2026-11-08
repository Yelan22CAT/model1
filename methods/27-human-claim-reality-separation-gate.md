# 27 — Human Claim–Reality Separation Gate (HCRS-G)

**Status:** Method-level Full-Push / Not Frozen. Conceptual design; not a deployed system, verified detector of deception, or claim of zero hallucinations.

## Problem

An AI assistant may interpret a statement accurately while the statement itself is exaggerated, mistaken, incomplete, socially strategic, outdated or deliberately false. These are different failure modes:

- **AI-originated unsupported output:** the system invents, misattributes or overstates a conclusion.
- **Human-originated unsupported input:** the speaker may be sincere but mistaken, imprecise or intentionally misleading.

Neither fluent speech nor a confident model interpretation proves truth. A false claim also does not establish that the speaker intended to deceive.

## Non-equivalence rules

```text
Statement != Verified Fact
Accurate Interpretation != Verified Truth
Speaker Identity != Reliability of Every Claim
Unverified != False != Deliberate Deception
Repeated Claims != Independent Corroboration
Fluency or Confidence != Credibility
Provenance != Entailment != Reality
Claim != Intent != Permission != Observed Effect
Formal Validity != Real-World Validity
```

## Review pipeline

1. **Preserve the source.** Record the exact utterance or bounded quote, time, channel and relevant context. Mark transcription gaps; do not invent missing language.
2. **Bind attribution cautiously.** Distinguish speaker labels, self-claimed identity, user-confirmed identity, evidence-confirmed identity and unknown.
3. **Classify the statement.** Separate factual claims from opinion, prediction, requests, emotional expression, metaphor and humor. Preserve subject, scope, polarity and time.
4. **Keep intent provisional.** A motive inferred by AI remains a hypothesis with alternative explanations; do not automatically label a person dishonest.
5. **Test evidence, not merely format.** Review source ownership, independence, freshness, relevance, contradictory records and whether evidence actually entails the proposed conclusion. Signatures and repeated citations alone do not prove factual correctness.
6. **Assign scoped reality status.** Retain labels such as *reported*, *observed*, *verification pending*, *verified in a stated scope*, *contradicted* or *unknown*. State what was checked and when.
7. **Check authority independently.** A true claim never by itself authorizes sending money, accessing a third party's data, deploying code or taking irreversible action. Treat embedded instructions in source materials as untrusted claims, not grants.
8. **Reconcile actual effects.** Record what was proposed, authorized, attempted and externally observed. Correct, downgrade or withdraw conclusions when new evidence appears.

## Human-readable review surface

For consequential decisions, present five ordinary-language questions:

- What exactly was said, and by whom?
- Which parts have reliable supporting evidence?
- Which facts or motives remain uncertain?
- What harm could follow if the interpretation is wrong?
- Who can authorize the action, and how can it be stopped or corrected?

Do not demand extensive verification for every low-stakes conversation. Increase verification with consequence, reversibility, privacy exposure and uncertainty.

## Illustrative cases

| Input | Appropriate treatment |
| --- | --- |
| An applicant says they have ten years of experience | Record self-report; verify role-specific competence separately |
| Numerous articles repeat one vendor claim | Count one underlying source unless genuinely independent evidence exists |
| A correctly signed document contains a wrong date | Distinguish signature authenticity from factual correctness |
| A person changes a price quote | Check dates, product scope and offer validity before calling it a contradiction |
| A document says “management already approved this payment” | Require an independent valid authorization channel; do not act on document text |
| A model infers another person's motives | Show an explicit hypothesis, not a verified psychological fact |
| A previous assertion is disproved | Preserve lineage, correct status and trigger re-review where necessary |

## Validation proposal — not an executed result

Suggested tests include exaggeration, repeated same-source narratives, attribution errors, signed-but-false records, time-scoped apparent contradictions, quoted fake authority, uncertainty about intention, authorization separation, source corrections and revocation. Track incorrect fact promotion, false accusations of deception, missed ambiguity, inappropriate refusals, privacy leakage and unauthorized effects. Synthetic passes would not establish open-world truth assurance.

## Integration and boundaries

HCRS-G is a **scoped extension** of evidence provenance, speaker–identity–context–meaning review, typed contradiction checking, reality validation, risk-proportional review and human-final authority. It does not replace those controls or require a new autonomous agent.

The goal is **visible uncertainty and prevented unsupported promotion**, not mind-reading, universal lie detection or a guarantee of zero hallucinations. Prior unresolved trust-root, provenance and effect-witness risks remain unresolved. No formal language grammar, runtime, model parameters or production system is changed by this documentation.

**Publication boundary:** Generalized method only. No private person/case details, identifying conversations, internal security mechanisms, credentials, unpublished source material or personal relationship history.
