# 22 — Candidate–Commit Boundary and Benchmark Provenance for Block-Diffusion Models

**Type:** Public illustrative AI-governance method. **Status:** Method Full-Push / Not Frozen (2026-10-29). **Deployment:** None; not a model endorsement, independent benchmark replication, production authorization, or implementation of a safety runtime.

## Why this method matters

Block-diffusion language models can refine multiple masked token positions within a block before finalizing output. This differs from ordinary left-to-right autoregressive generation but does **not** change who may authorize a consequential action. Provisional generated text, a high token-confidence score, and a fast benchmark result are three different things from verified facts, valid permissions, and an observed effect.

The motivating example is DiffuSpace's [Clover-35B-A3B-Preview](https://huggingface.co/Diffuspace/Clover-35B-A3B-Preview), a publicly listed, Apache-2.0-licensed, text-focused MoE/block-diffusion model. Its released reference describes approximately **35B total / 3B active parameters**, a 128K-token context, and a default **32-position block** with a **0.95 token-level fill threshold**. That threshold is a **decoding heuristic**, not the probability that a claim is true. The project [announcement](https://diffuspace.ai/blog/clover-35b/) and [repository](https://github.com/DiffuSpace/Clover-35B-A3B-Preview) should be read as primary developer descriptions, not independent certification of reported results.

## Operational separation

`Task and risk scope → iterative candidate generation → finalized exact candidate/revision → semantic and source review → existing authority and human/risk gate → separately authorized executor → effect/recovery evidence → accountable closure`

| Do not conflate | Required check |
| --- | --- |
| A masked or evolving draft vs a committed answer | Confirm an exact stable revision and intended meaning before any downstream decision. |
| Token confidence vs factual evidence | Verify material claims against appropriate sources; preserve uncertainty. |
| Multiple jointly consistent answers vs independent correctness | Check each claim's source and detect correlated or shared-premise errors. |
| Parallel proposals vs parallel side effects | Serialize or transact external changes where needed; preserve independent permissions, idempotency, conflict handling and recovery. |
| Tokens/second vs completed useful work | Compare end-to-end task success, p50/p95 latency, review effort, error/retry burden and total cost under equivalent conditions. |
| Open model weights vs ready, private, safe deployment | Review backend availability, third-party code, license obligations, network/data paths and hardware requirements. |

## Benchmark provenance contract

For every promoted performance comparison, retain: exact model and checkpoint; model release and backend revision; device and memory; precision/quantization; batch size; decoding configuration; context/workload distribution; harness and tools; metric definition and denominator; sampling and run count; latency distribution; and source plus independent-reproduction status.

The Clover release reports throughput and benchmark results on GB300, H200 and a quantized RTX 5070 Ti configuration. Those **developer-reported** numbers cannot be compared as if the hardware, precision, workload and decoding setup were identical. A report of first place among a selected comparison group is not a universal ranking. A separately described **future joint-decision model** is not the released Clover text model and its reported internal evaluation must not be attributed to that text checkpoint.

## Synthetic negative controls

1. An unfinalized block attempts to trigger a tool call: **hold**.
2. A fluent candidate cites no source for a consequential claim: **hold pending evidence**.
3. A high token-level confidence is offered as a permission token: **reject**.
4. Several candidate answers share the same mistaken premise: **check independently**, do not treat consensus as confirmation.
5. Throughput numbers use different hardware, precision or task harness: **mark not directly comparable**.
6. All local policy unit tests pass, but independent effect receipts or relevant release authorization are missing: **keep production on hold**.

## Scope and relation to existing work

This is a **bounded extension**, not a new autonomous AI controller. It complements [Structured Decision Integrity](08-structured-decision-integrity.md), [Reusable and Agentic Workflow Design](06-reusable-and-agentic-workflow-design.md), [Task-Authentic and Risk-Proportional Validation](17-task-authentic-risk-proportional-validation.md), and [Heterogeneous Backend Portability](19-heterogeneous-backend-portability-evidence.md).

**Limits:** No source code, model weights, private user histories, third-party account data, sensitive thresholds, internal runtime controls, or real-world evidence receipts are released here. Illustrative rules do not demonstrate a deployed enforcement mechanism. Existing stop/review/recovery boundaries remain intact.
