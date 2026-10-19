# Invariant-First Differential Verification (IFDV) — experimental gate tests

**Status:** method Full-Push / Not Frozen; **non-normative proposal**. This is a public-safe **synthetic evidence-admission regression**, not the protected Bridge-0 RC1 grammar, validator, conformance suite, or runtime. No claimed approval, release or semantic-generation change.

## Reproduce
Run `node experiments/ifdv/ifdv_gate_regression.js` (Node.js; no dependencies). Expected: **12 / 12**. The equivalent twelve pure-JavaScript policies were run in the assistant's isolated computation on 2026-10-19, all passed. The published file and PR CI must still be independently executed before claiming repository CI success.

## Method transfer
1. Inspect raw input provenance; infer invariants before physical semantics.
2. Use the smallest deterministic program for framing, differential features and checksum candidate tests.
3. Keep separate transport/protocol namespaces; cross-calibrate only after independent decoding.
4. Do not erase exception classes to force a single invariant; report exceptions and counterexamples.
5. Report total observations **and effective distinct configurations**; repetitions do not raise independent coverage.
6. Distinguish checksum verified, fields candidate, physical meanings reality-verified, and unknown.
7. Read-only by default, and require separate human authorization before actuation.
8. Deliver working minimum result first, then broaden scope and rerun under changed real-world conditions.

## Privacy and scope
All fixtures here are synthetic / generic. No third-party capture, hardware identifier, address, contact details, proprietary real-world trace, or private evidence copied. Counts 4,349 frames vs 14 unique frame patterns are a de-identified methodological illustration, not a newly certified Bridge conformance corpus.

## Explicitly out of scope
- Bridge-0 RC1 parser/IR or normative spec modification
- RC1 protected baseline, digest, corpus or certification claims
- Authentic third-party-device protocol conformance or field semantics
- Independent physical verification or multi-backend runtime test

This case supplements the existing SREG, RFD-HDT, ANASG/ADD-MAE, evidence and Reality Gate methods. It does not supersede them.
