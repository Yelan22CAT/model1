# Judgment Language and Interface

This document adds a public-safe language layer to **Model 1 v1.0**.

Its purpose is to express uncertainty, evidence direction, and action risk without forcing every situation into a binary yes/no answer or transferring judgment authority to AI.

---

## 1. Start with the next consequential action

Write the proposed action in plain language.

Examples:

- approve the change;
- send the message;
- place the order;
- release the system;
- continue the commitment;
- pause and verify.

The framework evaluates the next action, not the entire person, organization, or future.

---

## 2. Separate fact, inference, and unknown

Before assigning a direction or risk signal, separate:

- **fact:** directly observed or verified;
- **inference:** a bounded interpretation supported by some evidence;
- **unknown:** information that is missing, mixed, stale, or not yet verified.

A polished explanation does not convert an inference into a fact.

---

## 3. Evidence direction: `+ / 0 / -`

Model 1 may use a balanced ternary direction for the proposed action:

| Direction | Meaning |
| --- | --- |
| `+` | Current evidence supports the proposed path. |
| `0` | Evidence is insufficient, mixed, or unresolved. Preserve judgment. |
| `-` | Current evidence opposes the proposed path. |

`0` is a valid result. It does not mean hidden approval, concealed rejection, indecision, or failure.

The direction must remain limited by scope and time. Current evidence is not permanent truth.

---

## 4. Direction is not the same as the risk signal

Model 1 uses two different public outputs:

1. **Evidence direction:** `+ / 0 / -`
2. **Action-risk signal:** 🟢 Green / 🟡 Yellow / 🔴 Red

They answer different questions:

- Direction asks: **What does the present evidence say about the proposed path?**
- Signal asks: **How strongly should the person pause before acting?**

Examples:

- A path may have some supporting evidence (`+`) but still receive 🟡 Yellow because the action is difficult to reverse.
- Evidence may remain unresolved (`0`) while a release receives 🔴 Red because a mandatory validation step is missing.
- Evidence may oppose a path (`-`) without requiring dramatic language; the correct response may simply be to stop or choose another reversible option.

A direction does not authorize action. A signal does not replace evidence.

---

## 5. Use gray where evidence is gray

Do not compress:

- partial support into complete approval;
- caution into opposition;
- one defect into a total judgment;
- one successful result into repeatable operation;
- current evidence into permanent certainty;
- minor and fatal risk into the same label.

A conclusion should be no more precise than its evidence.

---

## 6. Gray analysis stops at a hard boundary

Nuance must not be used to wash away a rule that clearly controls the action.

Examples of hard boundaries include:

- a safety stop;
- a legal or authorization requirement;
- a payment, contract, or specification fact;
- a privacy or consent boundary;
- a required validation step;
- a non-negotiable personal limit.

When a hard boundary controls, the framework should state it directly.

---

## 7. Canonical public states

The same state may be expressed formally or in plain language, but the meaning must remain stable.

| Canonical state | Plain-language meaning |
| --- | --- |
| **Observation** | What is actually visible or verified now. |
| **Hypothesis** | One bounded explanation that may fit the evidence. |
| **Verification Pending** | Important information is still unverified. |
| **Verified** | The claim has been checked and supported. |
| **Frozen** | Do not continue consequential movement while the issue is reviewed. |
| **Deprecated** | This earlier judgment or wording is no longer used. |

Simplification must preserve the distinction between these states.

---

## 8. Compact decision-support output

A useful public Model 1 response should normally show:

1. **Conclusion** — the bounded current judgment;
2. **Decisive evidence** — the facts that matter most;
3. **Unknowns** — what remains unresolved;
4. **Reversal condition** — what evidence would change the conclusion;
5. **One safe next action** — a reversible step for human review.

It should not create false depth through repetition or present unstructured internal scratch work as evidence.

---

## 9. Closure awareness

Before treating an idea or output as complete, remember:

- an idea is not yet a usable product;
- a successful demonstration is not repeatable operation;
- fluent AI text is not verified reality;
- a workflow needs an owner for exceptions, maintenance, rollback, and responsibility;
- the Human Final Gate remains required.

---

## 10. Minimal public sequence

```text
Proposed consequential action
→ Fact / inference / unknown
→ Evidence direction: + / 0 / -
→ Scope and time limit
→ Consequence and reversibility
→ Risk signal: Green / Yellow / Red
→ Human Final Gate
```

---

## 11. Public boundary

This document does not publish:

- private observer packs or thresholds;
- private cases or identifiable narratives;
- detailed market or interaction models;
- anti-poisoning implementation internals;
- autonomous execution logic;
- complete private-engine structure.

It is a public judgment-language interface, not a complete operating system or decision authority.
