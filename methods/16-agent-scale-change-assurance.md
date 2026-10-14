# Agent-scale code-change assurance

**Status:** Public-safe method proposal, 2026-10-14. Not production-deployed, independently audited, or a claim of verified safety.

## Problem
An AI-assisted organization can merge changes faster than a human can read every line. High merge volume does not prove product value, code correctness, or safe deployment. A report of **more than 30,000 merged changes per day** in Anthropic's monorepo illustrates a workload-specific scaling challenge; it does not mean Git or GitHub is obsolete for ordinary repositories.

**Source:** [Anthropic engineering, “Redesigning source control at Anthropic,” 2026-10-13](https://www.anthropic.com/engineering/redesigning-source-control). Architecture and performance figures are vendor-reported, not independently benchmarked here.

## Non-promotion invariants
- `Merge throughput != Delivered value != Verified correctness`.
- `Code authored != Authorized merge != Validated release != Observed effect`.
- `CI green at revision A != CI green at revision B`.
- `Human intent review != Semantic correctness proof`.
- `Content hash != Authenticated provenance or authority`.
- `AI can write != May merge != Should deploy`.

## Minimal review contract
For a proposed change, record: change ID; exact base/head/tree hashes; affected code owners and dependencies; intended outcome and falsification criteria; authorization scope; risk class; generated versus human-edited provenance; tests and their exact revision/environment; reviewer identity; release decision; rollback/compensation route; evidence of real-world result.

## Proportional workflow
1. **Admit** the change only if tied to a valid need. No-output and deletion/refactor outcomes are first-class options.
2. **Route** a low-risk, reversible change to automation plus sampled oversight; sensitive changes require independent domain-owner review and explicitly scoped approval. Do not mandate human clicks for every trivial edit.
3. **Verify** tests against the exact artifact intended for deployment. Re-run affected checks after concurrent merges change the tested tree.
4. **Separate states:** proposed, reviewed, merged, integration-tested, release-authorized, deployed, observed, rolled back. None silently implies the next.
5. **Measure** defect escape, incident rate, rollback speed, post-merge regressions, reviewer burden, product outcome, cost and latency—not only PR/commit counts.

## Adversarial checks (design only)
Review plans should challenge stale CI evidence, forged attestations, privilege escalation, hidden dependency changes, protected paths, silent retries, failed release reconciliation, and a high-volume stream of useless changes. These are **unexecuted test ideas**, not an achieved security result.

## Scaling decision
Prefer Git and the existing CI/review stack until reproducible workload metrics show that its cost, latency or availability is the limiting factor. Specialized centralized systems may be justified for AI-heavy monorepos but introduce additional service availability and trust-root requirements.

**Boundary:** Educational/public governance interface only. No operational enforcement code, private thresholds, customer or internal repository data, signing keys, or permission to deploy. Human accountability remains with the designated owner.
