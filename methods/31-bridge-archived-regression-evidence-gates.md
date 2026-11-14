# 31 — Archived Bridge Regression and Evidence-Bounded Integration

**Status:** User-authorized method-level Full-Push / Not Frozen (2026-11-14). Public-safe assurance pattern; *not* a released Bridge grammar, production runtime, certified security system, or live execution authority.

## Problem

Well-formed AI reasoning statements, even when parsed and type-checked, do not guarantee the underlying claims are authentic or that a proposed physical or operational plan actually worked. Regression test results can also be misrepresented if archived source identity, historical test expectations, negative attack results, or intermittent timeouts are erased.

The method keeps these layers separate:

```text
Source/archive identity
  -> pinned candidate parser and test oracle
  -> typed assertion and contradiction checks
  -> provenance and authorization checks
  -> independently observed effect
  -> separate human release/production approval
```

**Normative invariants:** `Typed statement != true claim`; `inferred hidden constraint != verified fact`; `user preference != authority`; `actionable recipe != executed outcome`; `signed receipt != independently trusted signer`; `method Full-Push != software release`.

## Bounded reproducible regression protocol

1. **Pin the source:** preserve original archived bytes, version identifiers, hashes, manifests, parser/gate versions and source family; a historical report alone is not a test rerun.
2. **Isolate execution:** use a fresh directory and synthetic/test-only trust fixtures; capture command, seed, status, outputs and timeouts per run.
3. **Keep suites distinct:** report directed tests, fixed-seed synthetic tests, adversarial negatives, historical reconstructed examples, and independent field evidence separately.
4. **Maintain typed evidence states:** hypothesis, human-reported claim, verified-within-scope, unresolved contradiction, authorization, and execution receipts must never silently promote one another.
5. **Exercise negative boundaries:** deny malformed statements; conflicting entity/time/epoch bindings; unsupported verified flags; repeated-source evidence inflation; habit-to-permission escalation; and a claimed successful outcome with no actual effect evidence.
6. **Preserve failures:** successful clean re-runs do not nullify an intermittent timeout or a known forgery. A candidate may pass a local functional suite and still fail production security admission.
7. **Require independent acceptance:** more accurate sparse-input discovery, executable recipes, independently authenticated evidence and safe actual outcomes need their own blinded and real-world validation.

## Local regression evidence (bounded)

A private archived-candidate rerun on 2026-11-14 reported **221/221 directed checks** across separate Stage 3/8/9/10/11 candidate suites and 24 new sparse-input boundary checks. It reported **59,200** fixed-seed synthetic/grammar trials with zero authored unexpected outcomes in completed runs, plus 72 concurrent synthetic operations and 13 rebuilt historical fixtures. These are scoped test counts, **not** a unified released version's pass certification. New typed assertions were supplied by test authors, not autonomously inferred from unseen human instructions.

**Open blockers were retained:** a local witness forgery negative remains accepted by the old candidate; independent witness admission/effect authenticity is not demonstrated; repeated concurrent-suite attempts experienced timeouts even though fresh-extraction reruns passed. **Training Hold / Production FAIL** therefore stays active.

## Integration and boundaries

This is an incremental method within Historical-Case Regression, TAPEG, SREG, HCRS-G, LCR-G, MISA-G, Reality Gate, and Human Final. It does not replace any permission gate or the existing Bridge-0 grammar. Security-hold remediation, cross-domain zero-hint inference, model-weight training and verified real-world recipes remain separate tasks.

**Publication:** no individual/private case, raw dialogue, unredacted incident log, keys, production token material, exploitable attack replay instructions, source archive, or privileged runtime implementation. Exact private source manifests and logs are preserved in the private audit library.
