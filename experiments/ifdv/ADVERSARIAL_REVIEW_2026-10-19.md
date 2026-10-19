# IFDV adversarial regression, 2026-10-19

The v1 synthetic gate passed 12/12 previously, but new adversarial probes exposed **4 failures out of 10**: string-as-proof, negative independent count, zero unique count, lowercase I-page alias. A synthetic test passing only its positive examples does not certify that its security boundary is correct.

The v2 rule tightens input types and counts, and requires explicit boolean `true` for the illustrative proof/authorization flags. **This is not real proof verification**; production-grade provenance and authorization need separate trust evidence. The v2 corpus has 22 cases (12 original + 10 adversarial).

Reproduce: `node experiments/ifdv/ifdv_gate_regression_v2.js`.

Scope: synthetic policy admission **only**, not Bridge-0 grammar, RC1 parser, IR, validator, runtime, or independent CI. Protected baseline unchanged. Private real captures are not included.