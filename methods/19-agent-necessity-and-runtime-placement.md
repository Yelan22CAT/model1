# Agent necessity and runtime placement

**Status:** Public-safe architecture decision method, 2026-10-14; no single deployment topology required.

A powerful model, a product harness and an autonomous agent are not the same thing. Multiple model calls do not, by themselves, justify independent agents.

## Minimum sufficient architecture
| Level | Candidate topology | Why choose it? |
| --- | --- | --- |
| L0 | Model plus existing product harness | A bounded answer or tool-supported task is already sufficient. |
| L1 | Deterministic workflow | Steps, invariants and retries can be explicitly specified. |
| L2 | Constrained single agent | Dynamic tool selection or limited replanning is necessary. |
| L3a | Multiple-model routing | Specialization or costs justify distinct models without multiple autonomous actors. |
| L3b | Multiple agents | Independent roles/concurrency have demonstrated net quality, risk or latency benefit. |

These are alternative design choices, **not an obligatory ascending maturity ladder**. Reassess and downgrade when complexity no longer pays for itself.

## Separate lifecycles
- Logical task and plan;
- worker process or sandbox;
- VM/container/orchestrator instance;
- durable business state and effect receipts;
- identity, current permissions and revocation epoch.

A restarted process does not erase past effects; a restored checkpoint does not restore authority. A short-lived worker can use persistent state without a permanent dedicated VM. Container and VM isolation differ and must be selected against an explicit threat model.

## Admission and acceptance
Define: real user outcome, necessary autonomy, authorized effects, SLA, privacy/isolation risk, checkpoint/recovery guarantees, evidence sources, human review burden, latency and total cost of ownership. Compare a simpler baseline before expanding orchestration. Stop or revert when the result is worse.

**Invariant:** `Can act != May act != Should act`. A model's plan cannot mint its own authority or effect attestation.

**Boundary:** These are reusable selection criteria only, not public production runtime/source or a guarantee of safe agents.
