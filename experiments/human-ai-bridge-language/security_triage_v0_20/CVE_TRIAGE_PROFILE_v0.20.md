# Bridge-0 v0.20 Candidate | Security Signal–Exposure Triage Profile

**Status:** Candidate / Local Synthetic Tests / Human Comprehension Review Pending / Not Production Ready. **Proposed syntax and read-only runtime modification** on an **isolated branch only**. Existing v0.19 parser, RC1 grammar, invariants, broker, policy authority, and baseline are unchanged. This document is **not** a release of v0.20 as the canonical language.

## Motivation and evidence boundary

An official CVE advisory is not evidence that a specific asset is affected, reachable, exploited, or remediated. Self-declared `source_state=verified` is not proof; independently supplied host-verified advisory and *fresh* inventory context must match the artifact. This experimental check **never grants** deployment or a claim of global safety.

Go CVE-2026-111943 in examples is a **synthetic asset fixture**. It is not a finding about the user's computers, GitHub repos, or any named person's systems.

## Candidate four-line surface grammar (strict order)

```
⊙ [P1] security_triage profile=v0_20
◆ [E1] advisory cve=CVE-2026-111943 source_ref=go_official_sample source_state=verified
○ [A1] asset asset_id=fixture_go component=go version=1.26.9 cve=CVE-2026-111943 affected=unknown reachable=unknown trust=unknown
! [G1] gate action=release requires=human_final
```

The UTF-8 symbols are inherited from the original Bridge vocabulary. The `security_triage`, `advisory`, `asset`, and `gate` keyword subset and strictly typed fields are **new v0.20 candidate syntax**. All other forms fail closed. A historical/unsupported parser MUST NOT silently interpret this new profile.

### Semantic status

- `source_state`: `claimed | verified | unknown`, a declarative source statement; `verified` is not trusted by itself.
- `affected`, `reachable`: `yes | no | unknown`. Unknown remains unresolved.
- `trust`: `current | revoked | unknown`. `revoked` blocks positive disposition.
- `trusted_context`: separately supplied inventory/source match plus independent affected/reachability/trust state and host-declared freshness; **this candidate cannot authenticate the host**. Do not describe it as a cryptographic trust proof.
- Statuses: `hold_unknown_or_untrusted`, `affected_escalate_to_human`, `bounded_reachability_review`, `bounded_no_exposure_candidate`. The last is **not a verified claim of safety**.
- Always: `execution_allowed=false`, `may_publish_safe_claim=false`, `human_final_required=true`.

### Integration / boundaries

Experimental, read-only triage sidecar. No HTTP, registry, CA-store, network, package install, patch, procurement or production effect. No code execution, tool authority, agent delegation, revocation, credential handling, or signed attestation. Output JSON includes canonical SHA256 digest for repeatability, *not* authenticity. A trust-anchor loss requires independent adjudication, never assistant-created fresh authority.

## Validation plan

Run `python3 -m unittest -v test_security_triage_v0_20 test_security_triage_v0_20_extended` and compile candidate Python. The first module has five public smoke tests; the second has sixteen extended negative/consistency test methods including a matrix of 27 typed-state combinations. The PR workflow pins SHA-256 digests for the hardened runtime and extended tests, and checks both before executing them. Synthetic negative tests cover malformed or duplicate fields, invalid CVE, mixed CVEs, unsupported schema, confused source state, stale/untrusted host context, recalled trust root, tampered IR, matrix of 27 typed state combinations, and no execution/safety-claim authority. CI is restricted to candidate paths. Existing RC1 signed/frozen baseline intentionally untouched. The existing prototype CI passed on this branch; this does **not** amount to complete independent RC1 or v0.19 security qualification.

## Scope caveats

These are software-property tests on a stand-alone experimental fixture. They are **not** tests of Model Root as a deployed service, the user's devices, installed Go/PHP/Node versions, network trust stores, dependency SBOM, credential stores, or the eMudhra incident exposure on any real asset. Independent host-source verification, user ownership/authorization, vulnerability applicability, patch verification, production test evidence, and formal human comprehension are all pending.

**Can Parse != Source Verified != Affected != Exploited != Safe != Permission To Deploy.**