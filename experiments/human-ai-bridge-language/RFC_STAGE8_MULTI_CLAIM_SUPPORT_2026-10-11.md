# RFC — Multi-Claim Support Without Evidence or Authority Promotion (Stage 8 Candidate)

> **Bridge-0 / Experimental / Human Review Requested / Not Production Ready**  
> Public-safe research note only. No private parser source, benchmark fixture, account identifiers or internal configuration.

## Motivation

Human–AI shared language must remain useful even when one task contains multiple claims with mixed evidence statuses. A well-formed declaration does not demonstrate its real-world truth, and a self-asserted verified label cannot grant execution authority.

The current Stage 8 *advisory-only* candidate explores the narrow interaction between a list of reason records and one ADD-MAE action record. It is **not** the normative grammar of Bridge-0 and **does not make conversational translation into a compiler mandatory**.

## Proposed invariants for review

1. `PARSE_SUCCESS != FACTUAL_VERIFICATION != AUTHORIZATION != CONFIRMED_EFFECT`.
2. Duplicate or unknown claim IDs invalidate claimed support bindings; no implicit fill-in.
3. Appending an unverified claim cannot turn an unverified goal into a verified one.
4. An `audited:`-prefixed string is **not** an independently authenticated evidence receipt.
5. Context, plan, policy, state and authorization-epoch mismatches require pause or revalidation.
6. Unsupported semantic entailment (negation, temporal scope, contradictory evidence and partial supports) remains unresolved; the test harness may model declared support edges only.
7. No claimed `COMPLETED`, route choice, or claim label may authorize external effects without an independent authority/effect-checking system.

## In-scope local synthetic test evidence

- 44/44 directed tests; 16,000/16,000 fixed-seed synthetic cases for authored invariants; zero unexpected outcomes **within this test design**.
- Same-session historical Stage 7/6/5 *selected* reproduction returned five successful subprocess statuses. Not a historical remote retest.
- No human-comprehension experiments, LLM generation A/B, production installation, external witness cryptographic attestation or real-world effect checks.

## Blocking negative findings

Earlier Stage 3 privileged mock-ledger attack yielded `forgery_accepted: true`. This remains **OPEN / BLOCKING**; no Stage 8 metric closes it. Trust-root rollback, provenance-registry integrity and grant-service impersonation also remain unproved.

## Review requests

Can a syntactically valid claim batch silently shift speaker identity, evidence role, scope or negative assertions? Can a support claim appear to verify a goal without proving logical entailment? Which minimal independently verifiable evidence contract is required before any execution gate could consume this language?

**Release boundary:** independent candidate test label only. No Bridge-0 version promotion or modification of the protected public Model 1 core. Human review before merging.
