# Bridge-0 v0.20 CVE triage — Local synthetic test evidence

- Date: 2026-10-21 (user local)
- Test mode: isolated Python 3 standard-library local code, no network and no production effects
- Candidate path: `experiments/human-ai-bridge-language/security_triage_v0_20/`
- Commands: `python -m compileall -q .`, `python -m unittest -v test_security_triage_v0_20.py`, and demo CLI invocation with synthetic host context
- Observed result: **15 unit test methods PASS**; internal state matrix includes **27 combinations** of affected/reachable/trust states, all without granting execution or permission to claim an asset safe.
- Candidate implementation SHA256: `a2692962cff76b6d373b6ca3158a5e67b06c0113fb2d5edb55a121726d16fc1f` (local content digest).
- Test source SHA256: `d52270d2cd0696c8cfc714f0211c8479b1faa269a1e83121ffb327a8385015fe`.
- Caveat: no live installed-package inventory, SBOM, certificates, endpoints, customer assets, external threat-feed ingestion, vulnerability scanner, authenticated trust anchors, legacy v0.19 test suite, real signed approvals, or production rollback has been tested. External trusted context is a **simulation input**; production attestation requires separate assurance.
- Never merge or deploy from the passing test report alone. Review, human comprehension and independent security validation remain pending.