# 24 — Speaker–Identity–Context–Meaning Gate (SICM-G)

**Status:** Public-safe method-level Full-Push / Not Frozen (2026-11-08). **Implementation:** Research and test design; no production voice system certified.

## The failure mode

A low-latency speech translation demo is not evidence that a system can track overlapping participants, bind speech to the correct people, and preserve culturally appropriate meaning. Treat these as separate states rather than a single “understood” label.

`Captured signal → acoustic speaker segment → person/account binding → conversational context → literal and pragmatic meaning → translation option → human correction`

| State | Required provenance and uncertainty |
| --- | --- |
| Capture | Track/channel, lost packets, clock, isolation versus mixed audio, overlap. |
| Diarization | Acoustic speaker labels, turns, overlapping utterances; VAD is *not* speaker identity. |
| Entity binding | Distinguish platform claim, user-confirmed person, candidate and **Unknown**. |
| Pragmatics | Addressee, sarcasm, politeness, refusal, ambiguity, cultural and historical context. |
| Translation | Literal accuracy, terminology, tone and social appropriateness are separately evaluated. |

**Rules:** never fabricate a participant when signal or identity evidence is missing; conversational state is time-varying, not immutable identity; provide competing readings when necessary; sensitive interpersonal translation should support clarification, back-translation and participant correction. Honor consent and data retention limits.

## Risk-proportional evaluation

With informed consent or synthetic fixtures, compare 2 / 5 / 9 participants; isolated versus mixed tracks; interruption, noise, overlap and code-switching. Keep independent human-reviewed timestamps and labels. Report capture loss, diarization error, speaker attribution errors, ASR WER/CER/MER, translation meaning and politeness errors, clarification burden, p95 latency and cost **separately**.

A low-resource-language or specialist glossary is useful only when its dataset license, regional dialect coverage, overlap behavior and actual effect are known. A terminology list does not resolve implied intent. JEPA-style latent-state prediction may be explored as a candidate context interface, **not** treated as a verified diarization engine or factual identity oracle.

**Provenance:** Motivated by practitioner questions at a 2026 developer-event demonstration; the specific nine-participant report is anecdotal, not a reproduced Google-product benchmark. Vendor claims about language count or voice quality remain unverified.

Extends existing entity binding, dynamic state, human reality calibration, task-authentic validation and human final authority. No person records, recorded voices, private transcripts or model training data published.