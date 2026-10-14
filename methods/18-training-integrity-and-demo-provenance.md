# Training integrity and demo provenance

**Status:** Public-safe security and research-integrity pattern, 2026-10-14. Proposed controls, not proof of effective deployment.

Research organizations need separate assurance for training infrastructure and for the identity of a demonstrated model. A working demo does not automatically establish that the claimed internal training run produced it.

## Two independent threat surfaces

### Training execution integrity
- **Immutable and attributable build inputs:** pin code, containers, libraries, model weights, feature caches and data revisions; authenticate provenance independently of the account running training.
- **Constrained write permissions:** limit who can modify shared assets, installed libraries, launch parameters, checkpoint directories and experiment metadata.
- **Cross-worker consistency:** compare expected optimizer mode, gradient treatment, data sampler, seeds, collective-communication membership and environment digests across workers.
- **Tamper-aware incident response:** retain independent logs and chain of custody; distinguish natural faults from deliberate environment changes without presuming sabotage from every intermittent error.
- **Need-to-know investigations:** normal debug collaboration does not imply unlimited access to sensitive security-investigation details.

### Demo-to-training provenance
Require an inspectable chain:
`User input -> prompt transforms -> inference build -> model artifact digest -> checkpoint -> training run -> source/data/environment provenance -> independent acceptance`.

An unexplained preprocessing step, an opaque binary or attractive output is a reason to seek more evidence—not proof of misconduct. Reference comparisons must control for preprocessing, versions, randomness and deployment artifacts.

## Evidence grades
- Vendor-reported or witness-stated claim;
- contemporaneous records and independently preserved artifacts;
- independently reproduced observation;
- separately authorized deployment and externally observed effect.

Never promote an allegation directly to an independently verified fact.

## Controls to test later
Include dependency tampering with preserved timestamps, unauthorized shared-folder modification, cross-rank drift, suspicious process termination, stale checkpoint replay, model substitution, undisclosed prompt transformations and forged review receipts. **No tests are claimed to have run.**

## Motivation and sources
The ByteDance 2024 AI-training interference case had an official public acknowledgment; detailed later allegations about methods and a separate model demonstration remain evidence-sensitive and disputed. This method abstracts general defensive lessons without naming individuals, copying allegation-specific exploit code, or claiming a forensic finding.

**Boundary:** No attack scripts, access secrets, private incident logs or production claims. Human oversight, least privilege and independent evidence remain required.
