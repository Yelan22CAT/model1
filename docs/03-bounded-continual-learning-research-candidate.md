# Bounded Continual Learning and User Adaptation — Research Candidate

**Status:** Candidate / Verification Pending / Not Full-Push for the *new continual-learning implementation* (2026-11-14). Parent LCR-G and MISA-G methods are user-authorized Full-Push. Public-safe design note only.

## Proposed controlled loop

Minimal goal → candidate hidden constraints → one discriminating probe → conditional executable recipe → observed user/real-world feedback → provenance and consent gate → replay and regression tests → accept a bounded update or roll it back → versioned, revocable user preference overlay.

**Two separate learning channels:**

- **Reality/task learning:** Factual case labels must be independently authenticated, within scope, and authorized for training. Model-generated conclusions, repeated hearsay, or purported human verification do not automatically become ground truth.
- **User habit adaptation:** User-confirmed low-risk answer style and presentation preferences may adapt in a separate per-user layer. Direct preferences take priority over inferred habits; reversals and revocation remain effective. Neither habits nor repeated feedback grant tools, data disclosure, access, or authority.

## Current experimental boundaries

A local restricted-class incremental text classifier was built and tested with synthetic examples. It can adjust its *own* learned parameters on provided events and reject a candidate update when protected development examples regress. Its representation remains limited to a fixed feature vocabulary and predetermined labels. The local tests do **not** demonstrate open-world continuous self-improvement, authenticated online learning, independent held-out generalization, verified useful end-to-end recipes, or changes to GPT model weights. It runs when deliberately invoked, not in a background agent.

**Open gates:** independently authored and sealed blind cases; live source/user authentication and consent; train/holdout separation; domain shift and poisoning controls; authentic rollback and audit; verified physical outcome and fairness/safety review. Until those pass, production autonomy remains on hold.

**Publication boundary:** No raw private case examples, personal preference records, training events, runnable private pipeline, model binaries, secrets or elevated permissions.
