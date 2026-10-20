# Bridge-0 Executable Source Semantics v0.8

> Status: Experimental / first executable source-language layer  
> v0.8 adds no new glyphs.

## Purpose

Earlier rounds proved that Bridge can preserve semantic state, authority,
provenance, disagreement, and finality.

v0.8 asks a different question:

> Can a Bridge file itself become the source program for a real backend?

The tested path is:

```text
Bridge source
→ deterministic parser
→ canonical IR
→ deterministic validator
→ compiler
→ GitHub Actions YAML
→ GitHub runner
→ real execution
```

## Source example

```text
⊙ [W1] workflow
  name=bridge0_v08_generated
  runner=ubuntu-latest
  trigger=push
  branch=experiment/human-ai-bridge-v0.1

→ [T1] task kind=checkout
→ [T2] task kind=setup_python version=3.12
→ [T3] task
  kind=python_module
  module=unittest
  cwd=experiments/human-ai-bridge-language/prototype
  args=-v,test_parser_v0_2.py
```

The real source file is:

```text
executable_v0.8.bridge
```

## Compiler target

The compiler emits:

```text
.github/workflows/bridge0-generated-v08.yml
```

The generated file is an active GitHub Actions workflow.

CI also recompiles the Bridge source and requires byte-for-byte equality with
the checked-in generated artifact.

So the test now checks both:

```text
source → expected backend artifact
```

and:

```text
backend artifact → actual platform execution
```

## Restricted task set

v0.8 deliberately supports only:

```text
checkout
setup_python
python_module
```

There is no raw-shell task.

The validator rejects:

- arbitrary shell commands;
- shell metacharacters in arguments;
- path traversal;
- unsupported runners;
- unsupported triggers;
- arbitrary action injection;
- invalid Python versions.

This keeps the first compiler target small and auditable.

## Important real-world failure found

The first generated workflow failed on GitHub.

The compiler originally emitted a command like:

```text
run: 'python' '-m' 'unittest' ...
```

The internal compiler tests had not yet executed that generated workflow on the
real GitHub Actions parser.

GitHub rejected the workflow.

The compiler was then corrected to emit:

```text
run: python -m unittest ...
```

The generated workflow subsequently executed successfully.

This is a useful result:

> Compiler correctness cannot be inferred only from internal structure tests.
> The actual backend must remain part of the verification loop.

## Source language status

v0.8 demonstrates a narrow but real form of:

```text
Bridge source
→ executable backend
```

It does not mean Bridge is already a general replacement for Python, Rust, or
all YAML.

Current role:

```text
Bridge
= canonical semantic / workflow source language

GitHub Actions / Python / future backends
= execution targets
```

## Human layer

A human-readable Chinese/English explanation is optional for execution.

The machine path does not require a human to reinterpret the Bridge source.

However, human renderings remain useful for:

- review;
- teaching;
- debugging;
- audit;
- authoring assistance.

The execution path should depend on parser/compiler semantics, not a human or
LLM improvising an interpretation.

## New validator rules

```text
V065 workflow declaration / target policy
V066 task allowlist
V067 task field and argument safety
```

## Next frontier

The compiler is now part of the trusted computing base.

The next high-value test is:

```text
one Bridge program
→ multiple backends
→ equivalent observable result
```

For example:

```text
Bridge
├→ GitHub Actions
└→ local deterministic runner
```

If both execute the same canonical IR but produce different outcomes, backend
drift must become explicit rather than being hidden by the compiler.
