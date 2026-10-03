# Bridge-0 v0.2 — Adversarial Syntax Corpus

> Purpose: force deterministic rejection of inputs that invite semantic guessing.

| Case | Input | Expected |
|---|---|---|
| A01 | `■ [C1] delivery_date = ?` | reject: mixed epistemic state |
| A02 | `? [C1] delivery_date = 2026-10-10` | reject: unknown carries value |
| A03 | `■ delivery_date = tomorrow` | reject: missing semantic ID |
| A04 | `■ [C1] X probably_means Y` | reject: unregistered relation |
| A05 | `→ [A1] agent deploy target extra` | reject: trailing tokens |
| A06 | `★ [C1] a = true` | reject: unknown marker |
| A07 | `◆ [V1] log supports [C 1]` | reject: malformed reference |
| A08 | `■ [C1] a = true # maybe` | reject: inline comment unsupported |
| A09 | `◆ [V1] log supports [C404]` | parse, then validator rejects missing target |
| A10 | `✓ [K1] [C404] verified_by check` | parse, then validator rejects missing target |

## Why rejection is desirable

The language is intended to constrain a specific failure mode:

```text
underspecified expression
→ probable interpretation
→ silent completion
→ later treated as fact
```

Bridge-0 v0.2 instead uses:

```text
underspecified expression
→ explicit parser or validator error
```

This is a deliberate loss of convenience in exchange for lower semantic drift.
