# 17 — Task-Authentic Evaluation and Risk-Proportional Validation

**Method:** Full-Push / Not Frozen (2026-10-23). **Status:** conceptual evaluation method, not a production authorization or change to Bridge-0 grammar.

## Purpose before proxy

An examination score, synthetic benchmark, grammatical reference answer or generated artifact is a *proxy*, not the whole competence or actual external effect. Define what the human actually needs before designing the evaluation.

1. **Real purpose:** What does a person need to understand, communicate or accomplish?
2. **Construct:** Which capability is genuinely relevant (e.g. communication rather than exam-specific pattern recall)?
3. **Proxy audit:** What does the test directly measure? What does it omit or confound?
4. **Outcome contract:** Which observable postconditions count as satisfactory?
5. **Plural-path equivalence:** Accept different authorized solutions that preserve meaning, outcome and context.
6. **Means contract:** Preserve privacy, legality, provenance, safety, scope and approvals regardless of final result.
7. **Reality gate:** Distinguish model response, runtime execution, actual effects and user confirmation.
8. **Recalibration:** Update tests when real cases reveal a proxy mismatch.

`Test Score != Complete Capability`
`Reference Answer != Sole Acceptable Implementation` (only when equivalence is valid).
`Finished-looking Response != Verified External Effect`.

The analogy motivating this method is language learning: usable communication is not identical to proficiency at a particular multiple-choice exam. This does not imply that grammar, exact answers, standards, or written-language proficiency are irrelevant; validity depends on the test's stated purpose and population.

## Validate in proportion to risk, not branding

Private, low-risk, reversible experiments do **not** automatically need commercial-product review. Review depth increases with actual consequences, external exposure, irreversibility, uncertain inputs, privileges, and affected parties.

| Example | Appropriate evidence/handling |
|---|---|
| Private explanatory note or sandbox draft | Lightweight author check and feedback; no external authority |
| Reversible personal scripting | Local tests, explicit scope and recovery |
| Advisory information affecting another person | Check factual sources, material uncertainty, person retains choice; no fabricated effect receipt |
| Irreversible deletion, financial/identity/security changes or physical equipment | Strict preconditions, backup/recovery and authorization; HOLD when missing |
| Public software/service | Representative scenarios, negative tests, change control and accountability scaled to impact |

**Private use is not a universal safety exemption; public use is not an automatic instruction to impose maximum ceremony on every edit.** Review follows *risk*, not the label.

## Bounded, read-only research

An isolated candidate `BRIDGE-TAPEG-RPV/0.23-CANDIDATE` was locally tested on synthetic examples: 36 directed tests; 10,000 risk-escalation and 4,000 malformed-input cases with no unexpected allowances; inherited v0.21/v0.22 review tests 21/21 and 14/14. These checks test an authored rubric, **not** accurate real-world risk classification, formal Bridge grammar, independent security assurance, or execution permission.

**Human Final** applies at all stages. This note does not grant an agent permissions, authorize deployment, waive product standards, or claim that a personal observation proves efficacy/causation.
