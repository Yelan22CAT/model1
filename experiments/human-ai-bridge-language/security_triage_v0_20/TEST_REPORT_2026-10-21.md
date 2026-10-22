# Bridge-0 v0.20 | Corrected candidate verification and safety-scope report

**Date:** 2026-10-21; branch-only experimental change. **Candidate / Human Review Pending / Not Production Ready.**

## Findings and correction history

1. Initial candidate failed to bind the material `affected`, `reachable`, and `trust` claims to external context. A simulated input could shift unknown exposure to a more positive claim. This was identified **after** original five-smoke CI passed.
2. Further negative testing found a contradictory `affected=no` and `reachable=yes` state could be incorrectly regarded as no exposure. The corrected candidate holds this state for review.
3. Hardened local candidate binds all those fields to an independently supplied host context and retains the read-only execution deny. **Host-supplied context authenticity is not established by this program.** An untrusted caller can fabricate the context; do not equate matching inputs with independent attestation.

## Reproducible test identities

- Hardened runtime SHA-256: `a9ee8c7cfbca47cfad60dc1f3178ebbbcf66395b2e1afa0fd2d4fe612fc85ab6`
- Extended tests SHA-256: `30bf85064f63614bdacb35fa226c9fd5aac6f8e04d06c103edaca762bbb28222`
- Updated experimental GitHub branch stores both files byte-for-byte consistent with local verified SHA-256 values. CI checks these digests before test execution.
- Local Python 3.13.5: 16 extended unittest methods plus 5 independent smoke methods **PASS**; one extended test checks 27 affected/reachable/trust combinations; `py_compile` **PASS**.
- GitHub CI status must be read separately from the actual workflow result. **This document is not a CI pass certificate.**

### Minimal commands

Run from the candidate directory:

```sh
python -m py_compile security_triage_v0_20.py test_security_triage_v0_20.py test_security_triage_v0_20_extended.py
python -m unittest -v test_security_triage_v0_20 test_security_triage_v0_20_extended
python security_triage_v0_20.py triage_demo_v0_20.bridge --context triage_context_sample.json
```

## Limits

- Local synthetic Python semantics, test fixtures and GitHub repository files **only**.
- No authenticated external CVE feed, SBOM, agent permissions, compromised root mitigation, real running services, deployed PHP/Go/Node inventory, network scanning, real malware/exploit testing, live trust stores or runtime authority proof.
- Matching host context is not proof of source authenticity, independence, or trust-root currency.
- This profile is not the original Bridge-0 v0.19 parser or frozen RC1 runtime, so a pass here does not establish old-broker regression.
- Always `execution_allowed=false`, `may_publish_safe_claim=false`. No authority to merge, patch, deploy, sign, publish safety attestations or override Human Final.
- Integration remains **Draft** pending owner comprehension review, independent expert security review, compatibility assurance and a separately authorized merge/release.

**Status:** Hardened branch candidate synchronized to GitHub; test execution evidence local PASS; branch GitHub CI check pending independent retrieval.
