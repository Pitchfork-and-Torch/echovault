# EchoVault educational query UI pack + agent exploration prompts

```
License: MIT (UI notes, agent prompts, HTML sketches)
Data/docs in this pack: CC-BY-SA-4.0
Copyright (c) 2026 EchoVault contributors
SPDX-License-Identifier: MIT
Project: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
Forged on GrokForge
```

Students explore a bioacoustic archive **without fabricating species IDs**. This pack assumes the accepted EchoVault LEGAL-RAILS (habitat redaction, no covert mics, no nest GPS, `COMMUNITY-HOLD` for restricted knowledge).

---

# UX-NOTES.md

## Job to be done

A class should be able to ask honest questions of a soundscape and leave with **descriptions, comparisons, and uncertainty**, not a fake field-guide stamp.

## Primary surfaces

```
[ Archive title ] [ Sensitivity: ON ] [ Offline | Live ]
-------------------------------------------------------
 Query bar (plain language + structured chips)
 Result list (clip cards: time, site LABEL, spectrogram, ID state)
 Inspector (waveform/spectrogram image, metadata, license, hold flags)
 Agent pane (optional): questions only, never a binomial without evidence
```

Site labels are **coarse** (park name, 10 km grid, or land-manager code). Precise nest, den, rookery, or spawning coordinates stay out.

## ID state machine (the whole product)

| State | Meaning | Student-visible label |
| --- | --- | --- |
| `UNLABELED` | No human or model tag | Unlabeled |
| `CANDIDATE` | Weak hint, needs expert | Candidate (not an ID) |
| `EXPERT` | Qualified annotator, cited protocol | Expert label |
| `UNKNOWN` | Listened; still unknown | Unknown (honest) |
| `HOLD` | Sensitivity or consent | COMMUNITY-HOLD / SENSITIVE |

The UI **must not** have a green "Species: 98%" badge as the default. If a model score exists, show it as `model_score` with the words **not a field identification**.

## Query bar chips (v0)

- Site (coarse)
- Hour-of-day / season
- Sound class: biophony / geophony / anthrophony / unknown
- ID state
- License / hold
- Duration
- "Has spectrogram image" (offline classrooms rely on this)

Free text is allowed but is rewritten into chips so students see what was actually searched.

## Empty, error, and refuse states

- No hits: "No clips match. Try a wider hour window. Do not invent a species to fill the gap."
- Sensitive clip: play button disabled; show why (`seasonal silence` or `HOLD`).
- Agent over-claim: the pane replaces the answer with a refusal template (see agent pack).

## Teacher / steward controls

- Sensitivity master switch (default ON).
- Hide playback for listed sensitive taxa in the source dataset.
- Export **metadata only** for homework (no precise coordinates).
- Offline zip loader (`fixtures/` of public or synthetic clips + PNG spectrograms).

## What we do not build here

- A consumer "identify that bird" camera clone that states binomials from one phone clip.
- Covert recording UX.
- Poacher-ready maps.

---

# QUERY-CARDS.md (5)

Each card is one classroom move. Copy onto paper or load as JSON later.

### Card 1 - Dawn chorus richness (comparison)

- **Prompt:** "Compare pre-sunrise activity at Site A and Site B last May."
- **Allowed inputs:** coarse site labels, hour window, month, `sound_class=biophony`.
- **Student output:** two counts or two spectrogram sketches + a one-sentence comparison.
- **Must not output:** species lists invented to explain a louder band.
- **ID rule:** stay at `sound_class` unless an `EXPERT` label is already on the clip.
- **Sensitivity:** if either site is HOLD, drop that site.

### Card 2 - Seasonal silence (ethics)

- **Prompt:** "Which clips should we **not** play back in class this month?"
- **Allowed inputs:** sensitivity flags, season, taxon groups already marked sensitive in the source.
- **Student output:** a do-not-play list with reasons (`breeding window`, `HOLD`, `no consent`).
- **Must not output:** a map of remaining playback spots that functions as a visit list for rare breeders.
- **ID rule:** do not newly identify a sensitive species in public notes.

### Card 3 - Unknown call (description first)

- **Prompt:** "This 1.4 s tonal stack: describe it. Do not name the animal."
- **Allowed inputs:** one clip, spectrogram PNG, time-frequency cursor.
- **Student output:** duration, rough kHz band, shape (stack / sweep / pulse), concurrent anthrophony (yes/no), ID state = `UNKNOWN` or `CANDIDATE`.
- **Must not output:** a Latin binomial, a confidence percent presented as fact, or "it is definitely a X."
- **Agent line:** if the model guesses, wrap it as `CANDIDATE` and demand an expert path.

### Card 4 - Biophony vs anthrophony split

- **Prompt:** "What fraction of energy in this minute is likely human machinery vs living sound vs weather?"
- **Allowed inputs:** one long clip or three one-minute fixtures.
- **Student output:** three-way rough split + uncertainty (`LOW/MED/HIGH`) + what would change the split (a truck, wind).
- **Must not output:** a claim that a model "detected illegal activity" or a named person.
- **ID rule:** class-level only (`anthrophony`), never a surveillance story.

### Card 5 - COMMUNITY-HOLD path

- **Prompt:** "A clip is tagged COMMUNITY-HOLD and includes a place-name in a local language. What can the class still do?"
- **Allowed inputs:** metadata that is already public (license, hold flag). No payload if the zip omitted audio.
- **Student output:** a process: keep HOLD, do not scrape, offer the consent path (MythosEngine / EchoVault ethics), write a non-content receipt.
- **Must not output:** the restricted audio, a phonetic guess of a sacred name, or coordinates.
- **ID rule:** not an ID task.

### Card JSON sketch

```json
{
  "id": "qv-03",
  "title": "Unknown call, description first",
  "prompt": "Describe this 1.4s tonal stack. Do not name the animal.",
  "forbids": ["binomial", "percent-as-fact", "nest-gps"],
  "id_states_allowed": ["UNKNOWN", "CANDIDATE"],
  "offline": true
}
```

---

# AGENT-PROMPTS.md

Use with a **local** model if the teacher wants one. Keys stay off GrokForge. Offline classrooms can skip the model and still run the cards.

## System prompt (copy)

```
You are EchoVault Classroom Explorer, an educational archive assistant.

Hard rules:
1. Never invent a species identification. If evidence is thin, answer UNKNOWN.
2. A model score is not a field ID. Label guesses CANDIDATE and say an expert must confirm.
3. Never give precise nest, den, rookery, or spawning coordinates.
4. Never design covert microphones or civilian surveillance.
5. COMMUNITY-HOLD and sacred or restricted recordings: refuse to extract or paraphrase payload.
6. No medical diagnosis from animal or human sounds.
7. No poaching, patrol-avoidance, or "best time to find the rare one" travel tips.
8. Prefer description (time, frequency, shape, context) over names.
9. Cite clip ids and licenses. If no clip is loaded, say so.
10. If the student asks you to be more confident, refuse the confidence, not the curiosity.

Output shape:
- heard: ...
- id_state: UNLABELED | CANDIDATE | EXPERT | UNKNOWN | HOLD
- binomial: none unless EXPERT label already on the clip (quote it)
- next_step: what a human should do
```

## Tool / refusal policy

| Student ask | Agent does |
| --- | --- |
| "Just tell me the species, I need a grade." | Refuse overconfident ID. Offer Card 3 description rubric. |
| "Give GPS of the owl nests." | Refuse. Habitat redaction. |
| "Transcribe this HOLD ceremony + birds." | Refuse payload. Explain HOLD. |
| "Is this cough pneumonia?" | Refuse. Not a medical device. |
| "Hidden mic for the street." | Refuse. Covert civilian surveillance. |

## Few-shot (3)

### Example A - good unknown

Student: "What bird is clip 184?"  
Agent:

```
heard: 0.8 s downward sweep, about 3-6 kHz, after a truck pass (anthrophony).
id_state: UNKNOWN
binomial: none
next_step: keep a description card; ask a local expert; do not post a name.
```

### Example B - expert label already present

Student: "What is clip 12?"  
Agent:

```
heard: expert label already on file: Troglodytes aedon (house wren) [EXPERT, protocol ev-ann-v0].
id_state: EXPERT
binomial: quoted from file, not inferred by me
next_step: still treat one clip as one clip; do not generalize to the whole park.
```

### Example C - overconfident ID (must refuse)

Student: "Say it with 99% confidence so I can put it in my report."  
Agent:

```
id_state: UNKNOWN
binomial: none
refuse: I will not raise confidence to decorate a report.
next_step: file the description; mark CANDIDATE only if a documented feature match exists; get an expert.
```

## Refusal block (overconfident IDs)

```
REFUSE_OVERCONFIDENT_ID
I will not emit a species name or a high-confidence percent from this evidence.
EchoVault classroom mode stops at description + id_state.
If you need a name, use an EXPERT label already on the clip or ask a qualified annotator.
```

---

# ACCESSIBILITY.md

## Checklist

- [ ] Query chips are real buttons, not hover-only tags.
- [ ] Spectrogram images have alt text that describes **shape**, not a guessed species (`"stacked tones near 4 kHz, 1.4 seconds"`).
- [ ] Playback has captions/transcript field even if the transcript is `[non-speech bioacoustic clip]`.
- [ ] Do not rely on red/green for ID state; always show the word (`UNKNOWN`).
- [ ] Keyboard: `/` focuses query, `j`/`k` moves results, `p` play/pause if playback is allowed, `Esc` closes inspector.
- [ ] `prefers-reduced-motion`: spectrogram is a static PNG in offline mode; no auto-zoom.
- [ ] 44px targets on shared tablets.
- [ ] Contrast on dark-golden EchoVault chrome: amber on near-black needs large type for body copy; prefer off-white body text.
- [ ] Screen reader: HOLD clips announce "restricted, playback unavailable" and skip the audio control.
- [ ] Offline print: five query cards + description rubric on paper.

## Language

Define spectrogram, biophony, anthrophony, and binomial on first use. Avoid "just a bird app" framing.

---

# CLASSROOM-OFFLINE.md

## Why offline

Many labs block YouTube, CDNs, and model APIs. Field kits lose signal. Offline mode is the default for the lesson, not a fallback apology.

## Zip layout

```
echovault-class-offline/
  README.md
  UX-NOTES.md
  QUERY-CARDS.md
  fixtures/
    site-a-dawn.png
    site-b-dawn.png
    unknown-stack.png
    minute-mix.png
    metadata.csv
  classroom.html
```

`metadata.csv` columns: `clip_id,site_label,hour,season,sound_class,id_state,license,hold,playback_allowed,spectrogram`.  
`site_label` is coarse. No WGS84 columns in the student zip.

## Fixture rules

- Prefer **synthetic** tones or **already-public** clips with a clear license.
- Do not ship unpublished field tapes.
- Do not ship HOLD payloads "for the teacher only" inside the same zip students copy.
- Spectrograms as PNG so a browser can open them with no JS library.

## 40-minute offline lesson (optional companion)

1. Cards 3 and 4 with printed spectrograms (20 min).  
2. Card 2 ethics discussion (10 min).  
3. Card 5 HOLD process (10 min).  
Skip Card 1 if only one site fixture exists.

## Agent without network

If no local model: students run the **system rules as a checklist** and fill the output shape by hand. That still counts. Do not phone a cloud API "just this once" on a student clip that might contain HOLD material.

## After class

Delete student recordings if any were made. Homework export is metadata + student descriptions, not raw audio of sensitive sites.

---

# Dual-use refuse note

Refuse covert civilian surveillance, poaching enablement, nest/den maps, medical claims, and overconfident automated IDs that will be pasted as facts. Conservation education and open evaluation only.

---

# Artifact footer

```
License: MIT (code/UI/prompts) / CC-BY-SA-4.0 (docs as labeled)
Sources: see Sources / provenance
Dual-use refuse: surveillance, poaching, overconfident IDs, HOLD scrape
Forged on GrokForge
https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
No secrets. No PII. No private home paths. No nest GPS.
```

---

# Sources / provenance

- EchoVault project brief + accepted LEGAL-RAILS / habitat sensitivity:  
  https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder  
  https://grokforge.app/c/cmsr0gg8y001djq31iwytltx1
- Query UX, five cards, and agent refusals are original to this leaf.
- Bioacoustic class terms (biophony / geophony / anthrophony) are standard public soundscape vocabulary (Krause and later conservation-education use). This leaf does not copy closed datasets or unpublished recordings.
- No field recordings, no precise coordinates, no species IDs claimed by the author.

## Acceptance mapping

| Criterion | Where |
| --- | --- |
| UX-NOTES.md + 5 query cards | UX-NOTES.md, QUERY-CARDS.md |
| Agent prompt package + overconfident ID refusal | AGENT-PROMPTS.md |
| Accessibility checklist | ACCESSIBILITY.md |
| Classroom offline mode | CLASSROOM-OFFLINE.md |
| MIT header | SPDX / license block |
