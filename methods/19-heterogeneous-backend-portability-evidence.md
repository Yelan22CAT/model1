# 19 — Heterogeneous Backend Portability and Evidence Gate

**Method:** Full-Push / Not Frozen (2026-10-23). **Deployment:** none.

AI accelerator portability is neither guaranteed by an open-source announcement nor refuted by the existence of vendor-specific optimizations. A PyTorch-facing API, compiler lowering, numerical semantics, full workload throughput and operational total cost are different claims.

## Evidence ladder

| Gate | What it establishes |
|---|---|
| P0: Public announcement/source available | A project or implementation is described, not proven production-equivalent |
| P1: API and model support | Specific examples execute under stated versions |
| P2: Semantic/numerical equivalence | Validated tolerances, reproducibility, stability and failure handling |
| P3: Workload-level performance | Matched model, sequence/batch/precision, memory, accuracy and overhead |
| P4: Operations/economic fit | Availability, runtime maintenance, tooling, staffing, integration, actual cost |
| P5: Authorized and reversible use | Explicit owner decision, bounded rollout, rollback path and current real observations |

Use one semantic contract across backends; test each mapping against a reference implementation with negative cases. A compiler succeeds does not establish numerical identity or safe operational substitution. Observed differences may require documented tolerances instead of naive bitwise equivalence.

## Boundary

The 2026 TorchTPU/TPU Agent Suite discussion motivated this abstraction. Do not infer a measured GPU displacement, universal cost advantage, guaranteed kernel coverage, or production-readiness from the announcement. This method extends existing `Spec → Reference Implementation → Conformance → Runtime → Multi-Backend` and Reality Gate disciplines; it is not a new accelerator benchmark and modifies no deployed system.
