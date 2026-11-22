# 35 — Knowledge Distillation vs. Structural Knowledge Transfer: An Evidence-Gated Taxonomy

**Status:** User-authorized method-level **Full-Push / Not Frozen** (2026-11-22). This is a public-safe terminology and evaluation method. It is not a claim of successful model distillation, teacher internals access, production training, or modified foundation-model weights.

## Problem
The word *distillation* can describe a human-readable synthesis of third-party ideas, supervised training of a small model, or an actual teacher–student knowledge-transfer optimization. These activities share an analogy but have different measurable artifacts. Ambiguity can make documentation sound like a larger or more privileged experiment than was actually run.

**Rule:** A teacher's observed behavior, a model's training gradients, a probability distribution, a chain-of-thought-like explanation, and a written method card are distinct objects. None implies access to the others.

## Method taxonomy

| Process | Required evidence | Classification |
| --- | --- | --- |
| Summarize published methods and integrate reviewed decision principles | Source, abstraction, provenance, versioned method artifact; no student trained | **Structural knowledge transfer / cross-model structural synthesis**, not ML knowledge distillation |
| Specify a deterministic parser, policy, or regression test | Code, test receipt, source and effect boundaries; no trained student | **Rule / software engineering**, not ML knowledge distillation |
| Train an ML model on original labeled/synthetic task data | Training data, optimizer, local parameter delta, task metrics; no teacher-target link | **Supervised learning (non-KD)** |
| Update a trained model using reviewed, permissioned new cases | Old/new checkpoints, accepted-case ledger, holdout and rollback; no teacher-target link | **Continual learning (non-KD)** |
| Train a student on teacher-generated outputs, hard labels or responses | Named teacher, authorized dataset lineage, student updates, train/evaluation split | **Black-box/output-based KD** where teacher-output-based training is demonstrated |
| Train a student with accessible teacher logits or intermediate representations | Actual score/feature tensors, alignment loss, student updates and permissions | **Signal-access / white-box-style KD**; specify precisely which signals are accessible |
| Train with API-returned logprobs but no hidden states | Provider-exposed output distributions, training records and permitted use | **Output-distribution / gray-box KD**; API access does not imply full weight/internal access |
| Query a teacher or collect responses but never train a student | Teacher outputs only, without student-update evidence | **KD candidate, not completed KD** |

The informal black/white distinction is not a rigid permission model. Full teacher weights are not always necessary for logits-based training. An API may expose token logprobs without granting hidden-state or weight access. Record the actual access scope rather than assert a false binary.

## Training signals and gradients

- Logits and temperature-scaled soft targets describe a **distribution over predictions**, not the teacher's complete internal reasoning.
- KL divergence is one possible distribution-matching objective; feature matching and supervised losses are other options. A student parameter gradient is calculated during optimization; it is **not identical** to a teacher output probability.
- A natural-language explanation or self-reported 'confidence: 90%' is not authenticated teacher logits and need not faithfully represent a model's computation.
- Hard-label teacher supervision can still qualify as **output-based KD** when teacher-generated examples actually train a student; soft labels are not a universal prerequisite.
- A larger teacher does not guarantee that the student must be smaller, cannot outperform it on a task, or will improve downstream decisions.

## Evidence and authorization gate

`Observed source -> Define teacher signal and access level -> Verify training-data rights -> Verify teacher-to-student target lineage -> Verify student parameter update -> Assign taxonomy -> Compare with independent baselines, held-out/OOD tests and calibration -> Reality/effect gate -> Human Final`

1. **Fail closed on missing training evidence.** Do not label a method card, GitHub documentation, or inference-time retrieval as model KD.
2. **Preserve source-level claims.** Do not infer hidden chain of thought, weights, private prompt or gradients from surface outputs.
3. **Separate technical feasibility from permission.** Authorized use, provider terms, IP/privacy constraints and provenance govern whether teacher outputs may become training data. A technical KD classification does not imply authorized deployment.
4. **Hold weakly verified synthetic benchmarks in scope.** Local parameter deltas and synthetic scores support local training claims, not real-world superiority.
5. **Make claims falsifiable.** Record teacher ID, output type, temperature/loss where applicable, student checkpoint, dataset rights, holdout/OOD, false-positive cases, resources and observed effect.
6. **Reconcile prior uses without silent rewrites.** An informal 'structural reverse distillation' label may remain as a historical metaphor but receives the precise formal classification alongside it.

## Illustrative negative tests (method-only)

- A system summarizes another model's public design and writes an audited checklist → structural synthesis, **not KD**.
- A local classifier learns from authored synthetic labels, with recorded weight changes → supervised learning, **not automatically KD**.
- A student is trained on authorized teacher-completed examples, without logits → potential black-box KD, contingent on verifiable teacher–student lineage.
- A generated explanation claiming '90% confidence' → not teacher logits, no white-box entitlement.
- Two agents agree on an answer, or a teacher answer is saved as a document → neither verifies training nor truth.

**Scope limits:** This method does not alter the production Bridge grammar, safety authorization, training infrastructure, private data, model weights or any previously frozen/sealed status. Legacy safety/provenance blockers and production HOLD remain active. No independent real-world outcome is claimed.