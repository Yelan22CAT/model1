# Bridge-0 v0.2 Prototype

This directory contains the first deterministic implementation of the restricted Bridge-0 grammar.

## Files

- `parser_v0_2.py` — Bridge text → canonical IR.
- `validator_v0_2.py` — deterministic structural/semantic checks.
- `bridge_check_v0_2.py` — parse + validate CLI.
- `test_parser_v0_2.py` — parser unit tests.
- `test_validator_v0_2.py` — validator unit tests.

No external Python package is required.

## Run

From this directory:

```bash
python bridge_check_v0_2.py < ../demo_v0.2.bridge
```

The command returns both:

1. canonical IR;
2. deterministic validation output.

## Deliberate limitation

The prototype does **not** parse natural language.

If syntax is outside the restricted grammar, it must fail rather than ask an LLM to guess the intended semantics.

That behavior is part of the experiment.

## Example invalid input

```text
■ [C1] delivery_date = ?
```

This is rejected because the proposition mixes FACT and UNKNOWN.

Use:

```text
? [C1] delivery_date
```

## Current test status

The experimental branch uses a GitHub Actions check for:

- Python syntax compilation;
- parser tests;
- validator tests;
- end-to-end demo parse + validation.

Passing tests show only that the prototype obeys the encoded rules. They do not establish that Bridge-0 prevents every hallucination or is production-ready.
