# 34 — Selective Algorithm Selection & Decision-Metric Preservation

**Status:** User-authorized method-level Full-Push / Not Frozen (2026-11-21). Public-safe research and governance method. **Not** a trained 25-model ensemble, model-weight update, validated production system, or approved action policy.

## Problem
An introductory list of machine-learning algorithms is not a system architecture. A more complex model can outperform on an in-distribution score yet fail the actual decision, miss relevant low-variance state, or generalize poorly to a changed environment. Treating a model's confidence as verified evidence or permission compounds the failure.

The method selects the **least sufficient algorithm for the task and evidence**, then tests whether a more complex candidate provides a measured benefit without weakening provenance, decision relevance, or authority controls.

## Selective 25-algorithm reference catalog

| Role | Algorithms | Intended scope |
| --- | --- | --- |
| **Core baselines (7)** | Linear regression; logistic regression; decision trees; k-nearest neighbors; Bayesian analysis; principal component analysis; basic neural networks/MLPs | Interpretable predictions, case comparisons, probabilistic sensitivity, representation checks, baseline benchmarking |
| **Conditional candidates (11)** | Random forests; support vector machines; gradient-boosted trees; XGBoost; K-means; hierarchical clustering; DBSCAN; CNN; RNN; LSTM; Transformer | Tabular nonlinear comparison, clustering/novelty exploration, image and temporal representations—only when a concrete task justifies their cost |
| **Isolated simulation research (5)** | Q-learning; SARSA; deep Q-networks; policy gradients; actor–critic | Simulated planning/learning comparisons only; **no real-world execution authorization** |
| **Reference-only (2)** | AdaBoost; t-SNE | Optional benchmark and exploratory visualization references, not automatically new core modules |

The catalog classifies **use and admission**, not accuracy ranking. These are overlapping families, not 25 mutually independent advances. Bayesian reasoning is a broad inference framework; XGBoost is a gradient-boosting implementation family; LSTM belongs to the RNN family; Transformers are architecture families rather than a substitute for world-model objectives.

## Decision procedure

`Authorized task -> Source and label provenance -> Observability and required history -> Deterministic/physics/simple ML baseline -> Conditional candidate -> Decision-relevant IID/OOD evaluation -> Independent reality/effect verification -> Human final approval`

1. **Specify the decision.** Define data provenance, task, real-world loss function, failure cost, acceptable latency/compute and human authority.
2. **Check observability.** Identify whether necessary variables and temporal context are present. A better learner cannot recover logically missing information.
3. **Establish a simple baseline.** Compare deterministic rules, physics, linear models, or nearest-case methods before expanding complexity.
4. **Measure decision fidelity.** Check calibration, subgroup/context shifts, temporal leakage, out-of-distribution performance, and whether latent distances rank actual task progress.
5. **Separate artifacts and claims.** Classifier scores, clusters, nearest neighbors and synthetic tests are observations or hypotheses—not independently authenticated facts, identity bindings, permissions, or successful effects.
6. **Escalate only on net benefit.** If increased complexity cannot improve a relevant metric under reproducible validation, retain the simpler design or abstain.
7. **Preserve safe reversibility.** Candidate promotion requires documented evidence, human acceptance and rollback; RL remains in isolated simulation without real-world action rights.

## Specific failure modes

- **Variance preservation is not decision preservation.** PCA can retain high-variance features while discarding a low-variance feature crucial to a label or safety decision. Validate *task-dependent* preservation rather than variance alone.
- **IID fit is not OOD robustness.** Flexible ensembles and neural nets may interpolate successfully but fail outside observed training ranges; meaningful physical or linear baselines can sometimes extrapolate better.
- **Similarity is not identity.** KNN or clustering cannot by itself establish person/entity identity or causal links.
- **A probabilistic estimate is not permission.** Bayesian or logistic outputs cannot override independent evidence or authorization checks.
- **RL optimization is not deployment assurance.** A policy score or critic estimate cannot produce real-world actuation rights, proof of safety, or effect receipts.
- **Visualization is not verification.** t-SNE plots do not establish causal or global geometric truth.

## Evidence scope
Limited, self-authored synthetic comparisons illustrate the above failure modes; they **do not** establish general algorithm rankings, independent real-world validation, foundation-model training, or production readiness. The underlying implementation is a separate candidate and remains subject to reproducibility and external acceptance gates.

## Integration boundary
This method adds an **algorithm-selection discipline** under existing task/agent necessity, evidence provenance, neural-state representation, decision-metric alignment, risk-proportional validation and human-final approval. It is **not a competing governance control plane**.

Maintain known unresolved witness-authenticity, independent signer and replay/repeatability issues as **OPEN / Production HOLD**. Do not interpret method-level Full-Push as production admission, formal Bridge grammar ratification, executable authority, or model-weight changes.

**Public-release boundary:** generalized methodology only; no private case narratives, internal exploit details, confidential experiment materials, sensitive sources, proprietary thresholds, personal data, or executable control paths.
