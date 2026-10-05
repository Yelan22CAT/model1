# Bridge-0 Verification Status — v0.20 to v0.50

> **Experimental / public-safe summary / Not Production Ready**

This file summarizes the post-v0.19 adversarial verification campaign without publishing private harness internals or sensitive attack corpora.

## Consolidated milestones

| Range | Main assurance question | Public result |
|---|---|---|
| v0.20–v0.22 | Canonical semantics and parser/resource boundaries | Explicit semantic types, strict transport grammar, fail-closed verifier/resource policy |
| v0.23–v0.25 | State/time/revocation drift | State/auth/policy/time/replay binding plus atomic execution recheck |
| v0.26–v0.30 | History, delegation, quorum and policy composition | Split-view resistance, attenuated delegation, distinct-principal quorum, snapshot-bound policy composition |
| v0.31–v0.34 | Receipts, selective disclosure and schema evolution | Dependency-complete receipts, disclosure limits, freshness separation, downgrade-resistant schemas |
| v0.35–v0.37 | Mixed fleets and supply chains | Semantic serving eligibility, runtime identity, build/supply-chain provenance |
| v0.38–v0.40 | Claim-scope substitution and stale/circular proofs | Typed claim scope, well-founded derivation, support-aware truth maintenance |
| v0.41–v0.43 | Conflict and source independence | First-class CONFLICT, authenticated correction lifecycle, provenance-graph independence |
| v0.44–v0.46 | Confidence, action and human approval | Confidence/truth/action separation, risk-policy separation, scoped/current approval |
| v0.47–v0.49 | Planning, recovery and long-lived restore | First-class plans, partial-plan recovery, coherent restore generation |
| v0.50 | Full-stack composition | First-class Assurance Context plus exact cross-layer dependency graph |

## Selected invariants

```text
Semantic type != Runtime native type
Integrity != Authenticity
Authenticity != Authorization
Verified once != Authorized to execute later
Executed once != Effect happened exactly once
Claimed time != Trusted time
Checkpoint authentic != Globally consistent history
Signed capability != Valid capability
Key diversity != Principal diversity
Allow exists != Authorized
Past PASS != Current PASS
Selective disclosure != Unlinkability
Unknown field != Safe to ignore
Attested runtime != Correct runtime
Reproducible build != Benign build
Authentic evidence != Evidence for any claim
Circular support != Independent evidence
Revoked support != Refuted claim
Conflict != Unsupported
Copy count != Independent source count
Confidence != Truth state
Probability != Action
Signed approval != Informed understanding
Local safe != Globally safe
Compensation != Rollback
Backup authentic != Backup fresh enough to restore
All layers individually valid != End-to-end valid
```

## v0.50 regression note

The full-stack v0.50 campaign composed representative evidence, confidence, decision, review, authorization, plan, runtime, restore, and execution layers.

Directed tests used real Ed25519 signatures. The large randomized phase treated per-layer cryptographic verification as already completed and concentrated on composition semantics.

A test-harness shortcut initially skipped both repeated signature work and a semantic spec-identity check. Audit identified the harness bug, the shortcut was repaired, and the corrected randomized composition run produced:

```text
100,000 compositional cases
naive false accepts: 74,944
strict false accepts: 0
strict false rejects: 0
```

This is corpus evidence, not a universal security proof.

## Current convergence target

Bridge-0 should not become v1.0 merely because v0.50 was reached.

Proposed convergence criterion:

1. cover the remaining high-value orthogonal attack families;
2. observe several consecutive families with no new structural SPEC revision;
3. run full cumulative regression;
4. repeat cross-runtime / cross-version verification;
5. freeze public specification and compatibility rules;
6. only then consider a v1.0 release candidate.