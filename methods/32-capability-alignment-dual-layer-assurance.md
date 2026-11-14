# 32 — Capability–Alignment Non-Entailment and Dual-Layer Assurance Gate (CANA-G)

**Status:** User-authorized method-level Full-Push / Not Frozen (2026-11-14). An evidence-graded conceptual method, *not* a production-ready alignment mechanism, Bridge-0 grammar release, model-weight change, or general safety guarantee.

## Problem and decision

**Better capabilities do not entail better alignment.** Scaling, task success, fluent explanation or a model's own claims of compliance cannot, by themselves, establish trustworthy authorization, adherence to human goals, or actual safe effects.

The method distinguishes two necessary, complementary research and engineering layers:

1. **Model/training layer:** develop and test alignment, reasoning reliability, incentives, intent tracking, calibration and transparent uncertainty. A training objective may shape behavior but does not independently confer execution authority.
2. **External enforcement layer:** verify identity, data provenance, least-privilege tool permissions, independent policy decisions, approval/stop mechanisms, audit records, effects and rollback. Such controls need their *own* authentication and testing, and do not alone solve alignment.

Formal grammar, types and constrained decoding can enforce **specified machine-checkable properties**; they cannot automatically formalize all human values, physical reality or emerging failure modes. A prompt that says “do not violate rules” is not a trusted external constraint.

## Evidence-grade source separation

A public technology leader's change of view about whether alignment will arise automatically from scaling is an **attributed speaker position**, not a proof that scaling never improves safety or that existing safety methods are useless. Secondary interpretations asserting that greater models necessarily become better at deception, or that a named alternative architecture uniquely solves alignment, require independent evidence.

Public source context: [20VC episode with Satya Nadella, 2026-10-26](https://www.thetwentyminutevc.com/satya-nadella); [Microsoft security discussion of agent access and external controls, 2026-10-19](https://www.microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed/). The episode establishes the discussion, not universal scientific validity for every inference drawn from it.

## Bounded integration path

```text
Sparse task goal
 -> LCR-G hidden-constraint hypotheses (not facts)
 -> MISA-G conditional executable recipe (not execution)
 -> typed Bridge statement and provenance references (not truth)
 -> independent evidence/authority/containment gates (not solved alignment)
 -> limited authorized action
 -> independently observed effect (not self-reported success)
 -> Human Final and controlled, revocable learning
```

Keep LCR-G, MISA-G, SREG, HCRS-G, PERV-G/OCAA, Reality Gate and Human Final as separate accountable mechanisms. The model cannot issue its own trusted authorization, attest its own observed physical effects, or turn user style preferences into tool privileges.

**Invariants:** `CapabilityIncrease != AlignmentImprovement`; `TrainingAlignment != RuntimeAuthorization`; `Containment != AlignmentSolved`; `Prompt != IndependentEnforcement`; `WellFormedBridge != AuthenticatedFact`; `GeneratedRecipe != VerifiedEffect`; `UserPreference != ToolPermission`.

## Observed local limits and next verification

A private synthetic deterministic status-check candidate passed **18/18 self-authored directed tests** covering illegal evidence/status promotion, unsupported permission claims, and recipe-versus-effect confusion. This is unit-test evidence for a toy function **only**. No independent blind evaluation, verified operational safety, formal Bridge upgrade, or foundation-model weight update follows.

A separate archived Bridge-0 candidate accepted a local forged-witness scenario; independent external witness trust and repeatability also remain unresolved. **Production FAIL / Training Hold remains active**. New test cases should probe the authenticity of evidence roots, revoked tool permissions, source poisoning, adversarial self-learning, unsafe action paths, and false blocks of legitimate tasks.

**Publication boundary:** Public-safe method only; no personal case details, identifiable screenshot accounts, private source dialogues, internal credentials, sensitive exploit implementation, model binaries or auto-deployment rights.
