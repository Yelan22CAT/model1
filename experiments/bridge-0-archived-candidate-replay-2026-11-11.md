# Bridge-0 archived candidate regression | 2026-11-11

**Status:** Experimental / read-only local replay / **not production ready**. This is a test-status note, not a method release, grammar change, or production security certification.

## What was actually rerun

Previously archived, independently copied Bridge-0 candidate packages were restored into isolated local directories and tested with Python standard-library code. Original ZIP files were not altered.

| Test | Fresh local outcome |
| --- | --- |
| Stage3 directed | 41/41 |
| Stage8 directed | 44/44 |
| Stage8 fixed-seed synthetic | 16,000; unexpected 0 |
| Stage9 ConflictTriage directed | 32/32 |
| Stage9 fixed-seed synthetic | 16,000; unexpected 0 |
| Historical typed case fixtures | 13/13 expected outcomes |
| Stage11 ExternalWitness candidate 0.2 | 36 directed; 72 parallel fixture operations; 5,200 synthetic fuzz, unexpected 0 |
| Voice/transcript text-only sidecar | 23/23 directed |
| Stage3 forged effect-receipt negative probe | **forgery_accepted=true (security failure)** |

The Stage3/8/9 archived manifest checks matched all 14/14, 14/14, and 37/37 listed hashes, respectively. Reproducing an expected negative attack with process exit 0 is **not** a security PASS. Stage11 still uses a same-host fixture issuer and lacks independent production-effect attestation, trustworthy external monotonic state, and protection against fully privileged rollback.

## Unresolved gates

- **Production authorization remains FAIL/HOLD** due to the unresolved original Stage3 forged-receipt defect and broader witness/issuer authority assumptions.
- Older remote Verified v0.147 and local synthetic v0.272 are historical high-water labels, **not rerun** here. Later 0.273–0.283 versions retain Candidate/Human Review status.
- No actual audio ASR, independent semantic oracle, remote model test, external action, production deployment, model-weight update, or canonical Bridge grammar/runtime change was performed.
- The HCRS-G twelve scenario designs were **not executed as an implemented HCRS-G runtime**; the fresh tests above are from archived prior suites.
- New user-supplied examples have not yet been received, so no result is claimed for them.

## Privacy and release

This public status note deliberately excludes personal history, speaker identities, raw images, private source archives, privileged harness details, production secrets, financial information and relationship records. The detailed source hashes and local logs remain in the user's private evidence archive.

A proposed test extension should first preserve the exact user example, separate observation and interpretation, explicitly enumerate intended result and counterexamples, run an independent replay, and retain Human Final and change-approval gates.

**Status:** scoped archived-candidate reproducibility PASS; production security **FAIL/HOLD**; human review pending.