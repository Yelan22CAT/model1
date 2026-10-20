# Bridge-0 RC Qualification — v1.0-rc1 Candidate

> **Experimental / Not Production Ready**

## Convergence evidence

Five consecutive orthogonal post-terminal-boundary test families required no new structural specification revision:

- v0.61 — raw parser / canonicalization
- v0.62 — resource identity / resolver drift
- v0.63 — delayed / duplicated / out-of-order events
- v0.64 — cross-tenant / cross-environment isolation
- v0.65 — privacy-preserving audit / redaction integrity

## Cumulative regression

v0.66 representative assurance regression:

```text
41 directed invariant/attack families
500 pairwise attack compositions
250,000 randomized cumulative scenarios
strict false accepts: 0
strict false rejects: 0
```

## Cross-runtime reproduction

v0.67 deterministic canonical RC corpus:

```text
20,000 cases
Python 3.13.5
Node 22.16.0
Ruby 3.3.8
exact decision-output equality: yes
semantic mutation detected: yes
```

Verified common output digest:

`d462c4b301c06d89ab02bded6ced3bdb0f5a008054d12aa672905ca6c259c119`

## Freeze audit

v0.68 produced a machine-readable invariant registry and checked the RC specification/compatibility contract for missing required boundaries and prohibited overclaims.

```text
40 invariant records
freeze audit: PASS
registry digest: aa1cfd6c0b4903bbadec015b69b1124667b5ea78a4da8ec672f67fd8c483a292
```


## Evidence visibility

Bridge-0 separates **qualification evidence** from **publicly reproducible evidence**.

| Evidence | Visibility | What an external reviewer can do |
|---|---|---|
| v0.61–v0.65 convergence results | Public summary | Review the stated invariant/failure classes and public consolidation |
| v0.66 41-family / 250,000-case cumulative regression | Internal qualification evidence; summarized publicly | Review the result summary, but not the complete private adversarial corpus |
| v0.67 20,000-case Python/Node/Ruby corpus | Internal qualification evidence; summarized publicly | Review the reported digest/runtime result, but not the complete private corpus |
| v0.68 invariant registry / freeze contract | Public | Inspect `INVARIANTS_RC1.json`, the RC specification, and compatibility contract |
| RC1 256-case deterministic reproduction kit | Publicly reproducible | Regenerate the public corpus, run Python/Node/Ruby validators, compare the published digest, and inspect GitHub Actions |

The larger internal campaigns are intentionally not represented as fully public reproductions. Public reviewers should use the RC1 reproduction kit for independent reruns and treat the larger counts as scoped qualification evidence.

## Important boundary

These are corpus and model verification results, not a universal security proof. The candidate remains Experimental / Not Production Ready.

## Public reproduction kit

A bounded public-safe deterministic reproduction kit is available at:

- [public_repro_rc1](public_repro_rc1/README.md)

It uses a fixed seed, a specified SHA-256 counter PRNG, and 256 public-safe cases across Python, Node.js, and Ruby, with expected output digest:

`6e91757ca0921a94ac4300fcee1918f85d862039354da1b542560536083136bf`

The public kit is intentionally smaller than the private/internal 20,000-case qualification corpus. It exists so external reviewers can independently rerun representative RC semantics without publishing sensitive attack fixtures or private thresholds.

## Current external-witness / material-projection state

- current projection: `bridge-material-v3`;
- current material-state SHA-256: `1eaea2d0e7c106c973b78ab7209f33937bad12bbea78fb04303c151458a4ca93`;
- current witness generation: **6**;
- historical v1/v2 witnesses remain historical and MUST NOT be reused as current v3 proof;
- baseline→projection derivation is separately verified from the projection's own digest;
- Material Projection v3 retains governance claim-scope coverage and unknown-field fail-closed rules, and adds NFC-normalized canonicalization with post-NFC key-collision rejection;
- Drive + Gmail are redundant service surfaces in one Google/account trust domain, not two independent principals;
- `SECOND_EXTERNAL_TRUST_DOMAIN_REQUIRED` is the fail-closed state if the entire current external witness domain is unavailable/untrusted.

Public contact/review remains on GitHub. Private witness-account identifiers are not reviewer contact information.
