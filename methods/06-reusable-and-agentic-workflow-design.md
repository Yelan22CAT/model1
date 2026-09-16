# Method 6 — Reusable Workflows + Bounded Agentic Proposals

> Public-safe architecture for reducing repetitive script edits. Documentation only: no GitHub Actions workflow, AI agent, scheduling, credentials, or runtime controls are installed by this file.

## Problem

Repeatedly copying and editing scripts across repositories or documentation tasks creates drift. Purely fixed scripts are also a poor fit for context-sensitive changes such as identifying outdated references or proposing prose edits. These are different problems, so use two different mechanisms.

## Two documented GitHub mechanisms

**Reusable workflows:** Put a YAML workflow in `.github/workflows/` with `on: workflow_call`. Call it from another job with `uses` and explicit typed inputs. This centralizes repeatable checks. Prefer a same-repository reference at the caller commit or a reviewed commit SHA for cross-repository calls. Review permissions, secret passing and changes to shared dependencies. [GitHub: Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

**GitHub Agentic Workflows:** In public preview as of 2026-09-16. A Markdown workflow has frontmatter specifying trigger, permissions, engine and safe outputs, plus natural-language instructions. The `gh aw` tooling compiles it into a `.lock.yml` Actions workflow; a runnable setup requires both source and compiled files, Actions, supported engine/authentication and testing. Agents use read-only permissions by default; explicitly defined safe outputs constrain proposed write operations. Read the [GitHub overview](https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows), [creation requirements](https://docs.github.com/en/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows), and [security architecture](https://github.github.com/gh-aw/introduction/architecture/).

These are official product descriptions, not evidence that a workflow has been deployed or that its security claims are independently verified in this repository.

## Recommended division of labor

| Layer | Example use | Decision boundary |
| --- | --- | --- |
| Reusable, deterministic workflow | Check Markdown links, required filenames, schemas, version consistency and test results | Pass/fail applies only to checks actually executed; never promotes claims to Verified |
| Bounded agentic workflow | Suggest document edits, identify inconsistencies, prepare a traceable report or draft PR | AI output is a candidate; no self-approval or self-merge |
| Independent verification | Examine diffs, source citations, privacy and acceptance criteria | Contradictions stay unresolved until checked |
| Human Final | Decide factual promotion, privacy clearance, publication and merge | Final authority stays with the accountable person |

## Architecture

```text
Human goal + scope
  → Data and permission review
  → Reusable deterministic checks
  → Optional read-only agentic review / draft
  → Source trace + independent validation
  → Human review
  → Explicitly authorized merge or rejection
  → Reassess when workflow or dependencies change
```

## Controls before using this pattern

1. Begin with report-only/manual execution. Do not switch on a schedule merely because a sample contains one.
2. Specify the allowed repository, branch, paths, input types and outputs. Keep default permissions minimal; pass only necessary secrets, never blanket-inherit secrets by habit.
3. Review *both* source Markdown and compiler-generated Actions YAML for agentic workflows. Treat issue text, PR comments and external documents as untrusted data.
4. For private and public repos, establish a separate publication gate. No private content, logs, diffs, artifacts, caches or credentials may move into public output merely because an automation has access to both.
5. Prefer reviewable reports or draft PRs over direct commits or auto-merge. The model cannot declare its own claims Verified or override a failed test.
6. Test failure cases, such as a missing link, a false positive, secret exposure in a generated diff, unexpected permissions and stale approvals, before claiming effectiveness.
7. Pause if the agent requests broader permissions, outputs an unexplained diff or outruns human review; only a deployed external control can enforce an actual stop.

## Example: documentation maintenance (design, not executable workflow)

```text
Trigger: human requests a documentation consistency review
Reusable check: index links + required files + Markdown syntax
Agentic proposal: identify obsolete descriptions; cite changed source files
Output: report or draft PR, not auto-merge
Review: validate every substantive claim and privacy boundary
Decision: human accepts, modifies or rejects
```

A passing link checker does not establish that a regulatory interpretation is correct. A merged documentation PR proves an artifact was merged, not that an AI runtime is safe or an automation has been tested.

## Implementation status

- Design and public documentation: available.
- Executable reusable workflow: **not installed in this release**.
- Agentic workflow or engine/secret configuration: **not installed or enabled**.
- CI runs, regression tests, security effectiveness and maintenance-time savings: **not measured**.

**Summary:** Reuse deterministic plumbing; let agents prepare context-sensitive proposals; independently verify results; keep human publication and execution authority separate.
