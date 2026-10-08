# ADD-MAE Stage 3 — Public Evidence Status (2026-10-08)

**Scope:** Human–AI Bridge experimental ADD-MAE effect-recovery **candidate**. This page is a limited public evidence synopsis, not an assurance or software-release claim.

| Test plane | Status |
| --- | --- |
| Local proposal/decision checks | Synthetic cases passed in their tested bounds |
| Single-host mock effect/journal recovery | Unit/integration and crash tests passed in local harness |
| Privileged witness forgery | **FAIL / OPEN:** mock receiver allowed forged receipt accepted by reconciliation |
| Independent authenticated witness | **NOT IMPLEMENTED** |
| Multi-host external effect exactly-once | **NOT VERIFIED** |
| Formal Bridge-0 grammar admission | **PENDING** |
| Independent human/AI surface comprehension | **NOT TESTED** |
| Production deployment / training | **NOT AUTHORIZED** |

The local results include 41 passing directed unit/integration tests, 1,200 synthetic scenarios with 3,083 assertions, and a red-team case that was intentionally **accepted by the vulnerable implementation**. No later positive test cancels that negative evidence without a new authenticated-witness design and re-test.

The historical Bridge-0 remote-verified high-water remains **v0.147**; subsequent local candidate numbers must not be presented as remotely verified. This ADD-MAE candidate uses **0.3** as a local Stage 3 sidecar label, not an official Bridge-0 version.

See [ADD-MAE decision discipline RFC](RFC_ADDMAE_DECISION_DISCIPLINE_TRUSTED_EFFECTS.md) for the interface-level design and limitations. This file intentionally excludes private implementation and test artifacts.
