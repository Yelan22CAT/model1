# Public Safety Companion Notes

This directory adds public-safe safety primitives around Model 1 v1.0 without replacing the canonical judgment core.

The purpose is narrow: preserve human control when AI or agentic systems can move, generate, or iterate faster than humans can reliably understand, verify, and supervise.

## Included

- [`HUMAN_CATCHUP_GATE.md`](HUMAN_CATCHUP_GATE.md) — a minimal external pause / freeze / review pattern;
- [`DUAL_KEY_RESUME_LOCK.md`](DUAL_KEY_RESUME_LOCK.md) — a second lock that prevents self-resume after a freeze;
- [`COMPREHENSION_DEBT.md`](COMPREHENSION_DEBT.md) — a qualitative way to describe unresolved human-understanding debt;
- [`THREAT_MODEL.md`](THREAT_MODEL.md) — what these primitives can and cannot protect against;
- [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) — compact design rules.

## Scope

These notes are design patterns, not a production AI-safety system, not a complete alignment solution, and not a claim that any specific catastrophic-risk probability is correct.

They intentionally avoid publishing private thresholds, observer packs, calibration chains, anti-poisoning internals, hidden runtime packs, or autonomous execution logic.

## Core public pattern

```text
AI / Agent runtime
        |
        v
Human Catch-up Gate
        |
        +--> CONTINUE
        |
        +--> PRE-STOP
                |
                v
              FREEZE
                |
                v
        Snapshot + Trace
                |
                v
          Human Review
                |
                v
      Dual-Key Resume Lock
         /            \
Human approval   External invariant check
         \            /
              BOTH PASS
                 |
                 v
       Resume / Modify / Rollback
```

The important authority rule is simple:

```text
The model may recommend stopping.
The model must not own the authority to override the stop or resume itself.
```

## Relationship to Model 1 v1.0

The canonical public core remains a human judgment framework:

```text
Scope Lock
→ Source-State Check
→ Evidence Direction
→ Boundary / Consequence / Reversibility
→ Risk Signal
→ Human Final Gate
```

The safety companion adds a public design question around that core:

```text
If the system is moving faster than humans can understand or supervise,
what external mechanism preserves the human right to pause and re-enter?
```
