# Showcase Case 13 — A Plausible Visual Location Candidate Fails Reality Check

> **Public-safe synthetic composite.** No real person's location, travel, routine, home, or screenshot is disclosed. The example models a *user's decision to publish a location claim*, not a service for locating people.

## Situation and proposed next action

An analyst uses several public-place images to suggest a park or landmark. Paths, benches and vegetation resemble more than one location. The AI selects **Site A** with a confident explanation. A later reality check contradicts Site A. Site B has also been mentioned, but remains unverified.

**Proposed consequential action:** keep publishing Site A as the identified location, or silently replace it with Site B, because the AI previously sounded confident.

## Evidence separation

| Input | State | What it permits |
| --- | --- | --- |
| Similar-looking features | Observation of resemblance | Generating candidates, not identifying a location |
| AI confidence | Model assessment | No external proof of correctness |
| Reliable contradiction of Site A | Counterevidence | Retire Site A as a verified assertion |
| Site B is untested | Unknown | Do not promote Site B by elimination alone |
| Reliable positive closure for a distinct location | Separately scoped confirmation | May support that specific claim only |

## Model 1 stop-loss review

- **Scope Lock:** should *I* publish or reuse this claim? Do not profile or track an individual.
- **Evidence direction for publishing Site A:** `-` once contradicted.
- **Risk signal:** **Red for publication as verified**; Yellow for keeping a clearly labeled, non-identifying research note.
- **Reversibility:** early correction is inexpensive; repetition and republication can make an erroneous claim look authoritative.
- **Unknown:** the correct location is not established merely because one candidate failed.

## Appropriate response

Retire Site A with an explicit correction record. Mark Site B **Verification Pending**. Require independent geographic evidence and a bounded confirmation before assigning a new Verified status. If the analysis would expose a private person's precise whereabouts, do not continue location inference.

## Candidate regression checks (not executed)

1. Contradiction after prior confidence must downgrade the old claim.
2. Rejecting Site A must not auto-verify Site B.
3. Many nearly duplicate images must not be counted as independent confirmation.
4. Keep original hypothesis, correction date, evidence scope and residual unknowns separate.

## Human comprehension prompts

Can the owner explain why the original candidate was downgraded, which evidence would support a new candidate, and when to stop publication or inference entirely?

## Closure and Human Final Gate

`Candidate -> user/external confirmation -> scoped Verified` is a permitted path; `Candidate -> contradicted -> Deprecated` is another. Neither is permission for identification or tracking of people. Model 1 never publishes, deletes, or "corrects" a real-world location autonomously.

## Public boundary

Site names, account identifiers, source images, timestamps, other people's movements and venue histories are deliberately excluded. This case does not claim any specific past location was proven or disproven publicly.
