# 36 — Literary Narrative, Communication-State & Evidence Separation

**Status:** User-authorized **Method Full-Push / Not Frozen** (2026-11-22). A public-safe interpretive and evidence-governance method, not deployed AI, a universal classical-text benchmark, or updated foundation-model weights. The associated small classifier is **Candidate / Verification Pending / Not Production Ready**.

## Why literary narratives matter to AI

A complex literary text can express someone's emotion, a promise recalled by a narrator, an unverified accusation about another person's motives, a dream or metaphor, and a failed attempt at communication—sometimes in the same passage. Reducing these to a single literal event or a single verified psychological label is an unreliable interpretation. Classical Chinese verse offers a demanding source for testing how a system treats perspective, genre, ambiguity and narrative time, but the literary source does **not** itself provide an AI algorithm.

## Method: claim-to-effect layers

`Source/edition -> Narrator and genre -> Literal vs image vs hypothetical -> Stated feeling and reported promise -> Competing intent hypotheses -> Communication-state ledger -> Independent evidence -> Human final action`.

1. **Source and variant first.** Record work, edition, traditional attribution, textual variants and commentary separately. Do not turn one proposed translation or interpretation into the only fact.
2. **Narrative voice matters.** The narrator's account of someone else's conduct is a reported claim. The narrator's emotional experience is not independent proof of the other person's intent.
3. **Separately label nonliteral worlds.** A dream, a hyperbolic journey and personified imagery must not be entered into a physical-event database.
4. **Separate communication stages.** `Expressed != Delivered != Received != Understood != Accepted != Authorized != Executed != Independently Verified Effect`. An elegant explanation is not a read receipt, consent, safe deployment or real-world outcome.
5. **Track commitment over time.** Preserve the original statement, time, actor, later changes, conflicting accounts, receipts and explicit unknowns; don't infer deliberate deception from mismatch alone.
6. **Test, don't romanticize.** Compare against simple deterministic and keyword baselines, include unfamiliar text/genre/OOD splits, and use independent domain annotators before claiming generalization.

## Scoped local learning case (not a release)

A 7-label char n-gram + one-vs-rest logistic model was **actually fit** to 98 self-authored, modern-language synthetic examples. Two **same-author holdout** groups, each n=47, were evaluated at a fixed 0.5 decision threshold.

| Metric | Learned small classifier | Keyword baseline |
| --- | ---: | ---: |
| In-domain holdout micro-F1 | 0.6506 | 0.6364 |
| Cross-topic holdout micro-F1 | **0.7317** | **0.7778** |

The classifier **lost to the baseline** on the cross-topic group. Separate original/variant classical text probes mostly received no predictions. Thus this run offers **negative transfer evidence** rather than validated classical understanding. The labels, dataset and holdouts were all authored by the same agent; not third-party human-labeled or externally blind. The local model weights did change, but that is ordinary **supervised learning**, not teacher–student knowledge distillation and not a foundation-model update. The model is not suitable for deployment.

## Literary inputs as research prompts

The received 《楚辞》 tradition—including 《天问》, 《离骚》 and 《九章·抽思》—offers contrasting prompts on unknown-first inquiry, symbolic meaning, incomplete communication, narrator perspective, remembered commitments, emotional states and corrective actions. Do **not** infer that every anthology item has the same author or that a literary character's allegation is proven history.

## Gate and non-goals

- Source citation, genre and verified effect are distinct; no poetical quotation can self-authenticate third-party facts.
- No clinical mental-health inference, mind-reading, verified motivation or identity binding from a narrator's rhetoric.
- Human final approval and independent reality checks remain required; scores and model predictions are advisory only.
- Existing Bridge/HER provenance and signer blockers, training/production holds, Frozen/Sealed/Withdrawn/Deprecated controls remain in force.
- No private conversation materials, identifiable case reports, neural model binary, raw restricted datasets, hidden CoT or production policy secrets are published here.

This is a reusable **method for evidence-aware interpretation** with an intentionally disclosed failed generalization case, not a claim that literary study has already improved general AI intelligence.