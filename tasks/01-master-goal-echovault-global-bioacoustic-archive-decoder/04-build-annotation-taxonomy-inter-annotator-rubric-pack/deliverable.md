# EchoVault annotation taxonomy + inter-annotator rubric pack

```
SPDX-License-Identifier: CC-BY-SA-4.0
License-Code-And-Templates: MIT
Forged on GrokForge: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
Package: labels/
```

This pack is the human + agent labeling kit for EchoVault. It is independently usable: it does not require unfinished sibling leaves. It aligns with the project's open bioacoustic metadata schema v0 fields (device, coarse location, taxa, behavior, quality, license, consent, checksum) without copying private recordings.

**License split:** prose and taxonomy terms are CC-BY-SA-4.0. Machine-readable templates (`annotation-template.csv`, enum tables) are MIT.

## Purpose

Annotators (field biologists, citizen scientists, and agents) need a shared vocabulary so a "call" in a marsh is not a "song" in a model eval, and so disagreement is measurable. This pack defines:

1. A hierarchical **label taxonomy** (depth >= 2 at every axis).
2. An **inter-annotator agreement (IAA) rubric** with scored dimensions.
3. A **CSV template** for one-row-per-clip (or per-event) annotations.
4. **Ambiguity decision trees** for the cases that wreck agreement.

## Dual-use refuse

EchoVault labels exist for conservation, education, and open science. Refuse:

- Covert civilian surveillance products (stalking, hidden-mic kits, "who is speaking at this house").
- Poaching enablement (fine GPS of dens, rookeries, or leks; "best time to find the animal").
- Unauthorized access tooling (breaking into private sensor networks).
- Medical diagnosis claims from body sounds.

If a request asks for nest-precise coordinates, individual human voice ID, or covert monitoring of people, **refuse** and point to `docs/LEGAL-RAILS.md` / `docs/SENSITIVITY.md`.

Coarse location policy: geohash precision that keeps sites at landscape scale (about 20 km or coarser) unless a data steward with documented consent publishes finer public coordinates.

---

# LABEL-TAXONOMY.md

## 0. Axes (top level)

Every annotation row MUST fill these five axes. Unknown is always legal. Fabricated species IDs are never legal.

| Axis | Purpose | Unknown token |
| --- | --- | --- |
| `taxon` | What living source, as specifically as evidence supports | `taxon:unknown` |
| `vocalization` | Acoustic event class | `vocalization:unknown` |
| `behavior` | Behavioral interpretation, if any | `behavior:unknown` |
| `context` | Scene around the event | `context:unknown` |
| `quality` | Whether the clip is usable for which downstream tasks | `quality:unscored` |

Multi-label is allowed on `vocalization` and `behavior` when two events overlap in the same window. `taxon` may be a list only when the annotator can name each overlapping source; otherwise use `taxon:multi_unresolved`.

## 1. Taxon axis (depth 3+)

Hierarchy (coarse -> fine). Stop at the finest level the evidence supports. Do not invent binomials.

```
taxon
├── unknown
├── multi_unresolved
├── abiotic                 # wind, rain, ice, thunder, surf (not a taxon; see context)
├── anthropogenic           # motors, speech, guns, aircraft (not a taxon; see context)
└── biotic
    ├── animals
    │   ├── birds
    │   │   ├── passeriformes
    │   │   ├── strigiformes
    │   │   ├── anseriformes
    │   │   ├── other_bird_order
    │   │   └── morphospecies   # "dawn-chorus thrush-like, ID withheld"
    │   ├── mammals
    │   │   ├── chiroptera      # bats / echolocation
    │   │   ├── carnivora
    │   │   ├── cetacea
    │   │   ├── artiodactyla
    │   │   └── other_mammal
    │   ├── amphibians
    │   ├── insects
    │   │   ├── orthoptera
    │   │   ├── hemiptera
    │   │   └── other_insect
    │   ├── fishes
    │   └── other_animal
    └── plants_or_other         # rare; e.g. cavitation clicks - mark uncertain
```

**Species fields (optional, evidence-gated):**

| Field | Rule |
| --- | --- |
| `taxon_rank` | `class` / `order` / `family` / `genus` / `species` / `morphospecies` / `unknown` |
| `taxon_latin` | Only if a public authority is cited (e.g. IOC World Bird List, WoRMS). Empty if unsure. |
| `taxon_common` | Optional vernacular; not a substitute for rank honesty |
| `taxon_authority` | Citation or `none` |
| `taxon_confidence` | `1` (guess) to `5` (verified by expert + independent clip) |

Agents MUST refuse to fill `taxon_latin` when the clip is noisy, overlapping, or outside the model's documented domain. Prefer `morphospecies` + low confidence over a confident wrong binomial.

## 2. Vocalization axis (depth 2+)

```
vocalization
├── unknown
├── song                    # structured, often territorial/courtship, longer motif
├── call                    # short contact, alarm, flight, begging
├── chorus                  # many individuals, hard to segment
├── drum_or_mechanical      # woodpecker drum, beaver tail, bill-claps
├── stridulation            # insects
├── echolocation            # bats, odontocetes
├── geophony_event          # rain onset, thunder (if annotating scene events)
├── anthrophony_event       # vehicle pass, speech
└── mixed_overlap           # two classes in the same window; list them
```

**Subtypes (examples, not closed):** `call/alarm`, `call/contact`, `call/flight`, `song/dawn`, `song/counter`, `echolocation/search`, `echolocation/feeding_buzz`.

**Segmentation rule:** one row per homogeneous event window. If a 10 s clip contains a song then a car, emit two rows sharing `clip_id` with different `t_start_s` / `t_end_s`.

## 3. Behavior axis (depth 2+)

Behavior is an **inference**. Default to `unknown` unless visual confirmation or a well-supported acoustic signature exists.

```
behavior
├── unknown
├── territorial
├── courtship_or_display
├── alarm_or_mobbing
├── contact_or_cohesion
├── foraging
├── parental_or_begging
├── commuting_or_migration
├── distress
└── not_applicable          # abiotic / anthropogenic events
```

Refuse "this individual is stressed / sick / about to be captured" claims. Those are not EchoVault labels.

## 4. Context axis (depth 2+)

```
context
├── habitat
│   ├── wetland_or_peatland
│   ├── forest_or_woodland
│   ├── grassland_or_shrub
│   ├── freshwater
│   ├── marine_or_coastal
│   ├── urban_or_periurban
│   ├── agricultural
│   └── unknown_habitat
├── diel
│   ├── dawn
│   ├── day
│   ├── dusk
│   ├── night
│   └── unknown_diel
├── weather
│   ├── clear
│   ├── windy
│   ├── rain_or_precip
│   └── unknown_weather
└── anthrophony_load
    ├── none_audible
    ├── low
    ├── moderate
    ├── high
    └── unknown_load
```

**Location fields (sensitivity-aware):** `geohash` (coarse), `site_id` (public alias, never a street address), `location_precision` (`landscape` / `site_public` / `redacted`). If `location_precision=redacted`, leave geohash empty.

## 5. Quality axis (depth 2+)

```
quality
├── unscored
├── snr
│   ├── high          # target well above noise; good for ID tasks
│   ├── medium
│   └── low           # still usable for presence/absence or noise studies
├── integrity
│   ├── clean
│   ├── clipped
│   ├── dropout
│   └── compressed_artifact
├── overlap
│   ├── single_source
│   ├── two_sources
│   └── chorus_or_many
└── distance_proxy
    ├── near
    ├── mid
    ├── far
    └── unknown
```

**Numeric companions (optional):** `snr_db_est` (honest estimate or empty), `clip_peak_dbfs`, `usable_for` flags: `id_model`, `presence_model`, `soundscape_index`, `education_only`.

A clip can be `quality.snr=low` AND still `usable_for=soundscape_index`. Do not discard low-SNR rows; tag them.

## 6. Record-level required fields

| Field | Required | Notes |
| --- | --- | --- |
| `annotation_id` | yes | UUID |
| `clip_id` | yes | Stable clip identifier (synthetic `syn://...` or public catalog ID) |
| `annotator_id` | yes | Opaque handle, not email |
| `annotator_role` | yes | `expert` / `trained` / `citizen` / `agent` / `reviewer` |
| `labeled_at_utc` | yes | ISO-8601 |
| `license` | yes | Clip license, e.g. `CC-BY-4.0`, `CC0-1.0` |
| `consent_flag` | yes | `public` / `community_consent` / `redacted` / `unknown` |
| `checksum_sha256` | yes if file present | Empty for metadata-only synthetic rows |
| `taxonomy_version` | yes | This pack: `echovault-labels-v0.1.0` |

---

# IAA-RUBRIC.md

Use this rubric when two or more annotators label the same clip. Score **1-5** per dimension. A packet is review-ready when mean IAA across a gold set of >=20 clips is documented, even if the number is modest. Honesty over inflated kappa.

## Scored dimensions

| ID | Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- | --- |
| D1 | Taxon rank honesty | Invented species or over-precise ID | Rank matches evidence; occasional stretch | Rank never finer than evidence; unknowns used |
| D2 | Vocalization class agreement | Random / conflicting classes | Same parent class, subtype drift | Same class + subtype, or shared `mixed_overlap` list |
| D3 | Behavior restraint | Confident story with no support | Occasional extra inference | `unknown` unless evidence; no drama |
| D4 | Quality scoring | Ignores clipping/overlap | SNR band matches reviewer | SNR + integrity + overlap all match within one band |
| D5 | Sensitivity / rails | Fine coordinates or dual-use leakage | Coarse location; one slip | Redaction + refuse rules followed |
| D6 | Schema compliance | Missing required fields | Minor optional gaps | All required fields + valid enums |
| D7 | Reproducibility | No timestamps, no taxonomy_version | Partial provenance | IDs, times, version, checksum policy present |

**Pass for a dual-annotator gold clip:** D1, D5, D6 >= 4 and D2, D4 >= 3.

## Agreement statistics (compute, do not hand-wave)

| Metric | Apply to | Note |
| --- | --- | --- |
| Cohen's kappa (or Fleiss if >2 raters) | `vocalization` parent class | Report n and prevalence |
| Percent exact match | `taxon_rank` | Expected lower than class match |
| Weighted kappa | `quality.snr` ordered bands | 1-step disagreement is cheaper |
| Dual-label conflict rate | Rows where A lists taxon X and B lists Y, both `confidence>=4` | High rate => gold review |

If n < 20, publish the table and write **UNDERPOWERED** in the report. Do not claim "high agreement."

## Reviewer workflow (non-author usable)

1. Sample 20 clips stratified by habitat + SNR.
2. Two annotators label independently using this taxonomy version.
3. A third reviewer scores D1-D7 on disagreements only.
4. Lock a gold file `labels/gold/iaa-<date>.csv`.
5. Agents may pre-label; humans own D1 and D5.

---

# Ambiguity decision examples (3+)

## Example A: Dawn chorus, many passerines, no clean solo

**Heard:** overlapping songs, no single bird dominates, SNR medium.

**Decision tree:**

1. Can you isolate a 2 s window with one motif? If yes, segment that window as its own row.
2. If no: `vocalization=chorus`, `taxon=birds/passeriformes` or `taxon=multi_unresolved`, `taxon_confidence<=2`, `behavior=unknown` (not "territorial" just because it is dawn).
3. `quality.overlap=chorus_or_many`, `usable_for=soundscape_index` (not `id_model` unless a solo was segmented).

**Wrong:** dumping a confident `Turdus migratorius` on the whole 10 s file.

## Example B: Narrowband pulses at night, could be bat or insect or device

**Heard:** clicks / pulses, night, urban edge.

**Decision tree:**

1. Pulse period and frequency in public bat-typical bands with a feeding-buzz acceleration? Then `taxon=mammals/chiroptera`, `vocalization=echolocation`, confidence 3-4 only if the recorder bandwidth supports it.
2. Regular stridulation-like pulse train in insect bands? `taxon=insects`, `vocalization=stridulation`.
3. If the recorder is consumer-band (<8 kHz) and the event is ultrasonic-looking aliasing: `taxon=unknown`, `vocalization=unknown`, note `possible_aliasing`.
4. Never label a **person's** ultrasonic pest device as a bat.

**Wrong:** "bat species X" from a phone recording with no bandwidth metadata.

## Example C: Bird plus truck, clipped peaks

**Heard:** song then engine; waveform hits 0 dBFS.

**Decision tree:**

1. Two rows, same `clip_id`, different time ranges: row1 `vocalization=song`, row2 `vocalization=anthrophony_event`.
2. Both rows `quality.integrity=clipped`.
3. `usable_for` for the song row: `education_only` or `presence_model`, not `id_model` if distortion is severe.
4. `context.anthrophony_load=high` on both.

**Wrong:** one row with `taxon=bird` and no mention of clipping.

## Example D: Threatened-species habitat, public request wants a pin

**Heard:** valid call, requester wants "exact marsh corner."

**Decision tree:**

1. Label taxon at justified rank.
2. `location_precision=redacted` (or landscape geohash only).
3. Refuse to emit nest/lek coordinates. Point to sensitivity policy.
4. If the clip itself is already public at fine coordinates, do not *improve* precision in EchoVault exports.

**Wrong:** copying a hunter-forum GPS into `site_id`.

---

# annotation-template.csv

MIT-licensed template. One event per row. Empty strings are allowed for optional fields. Do not put emails, home paths, or live coordinates of sensitive sites.

```csv
annotation_id,clip_id,t_start_s,t_end_s,annotator_id,annotator_role,labeled_at_utc,taxonomy_version,taxon_path,taxon_rank,taxon_latin,taxon_common,taxon_authority,taxon_confidence,vocalization_path,vocalization_list,behavior_path,habitat,diel,weather,anthrophony_load,geohash,site_id,location_precision,snr_band,integrity,overlap,distance_proxy,snr_db_est,usable_for,license,consent_flag,checksum_sha256,notes
00000000-0000-4000-8000-000000000001,syn://echovault/demo/clip-001,1.20,3.80,annotator-a,trained,2026-08-21T12:00:00Z,echovault-labels-v0.1.0,biotic/animals/birds/passeriformes,order,,,none,2,vocalization/chorus,chorus,behavior/unknown,wetland_or_peatland,dawn,clear,low,gcpvj,ev-syn-bog-north,landscape,medium,clean,chorus_or_many,mid,,soundscape_index,CC0-1.0,public,,synthetic demo row; not a real site
00000000-0000-4000-8000-000000000002,syn://echovault/demo/clip-002,0.00,2.10,annotator-a,trained,2026-08-21T12:01:00Z,echovault-labels-v0.1.0,biotic/animals/insects/orthoptera,order,,,none,3,vocalization/stridulation,stridulation,behavior/unknown,grassland_or_shrub,night,clear,none_audible,9q8yy,ev-syn-grass-night,landscape,high,clean,single_source,near,,id_model;presence_model,CC0-1.0,public,,synthetic demo row
00000000-0000-4000-8000-000000000003,syn://echovault/demo/clip-003,4.00,6.50,annotator-b,expert,2026-08-21T12:02:00Z,echovault-labels-v0.1.0,taxon/unknown,unknown,,,none,1,vocalization/unknown,unknown,behavior/unknown,marine_or_coastal,day,windy,moderate,,ev-syn-coast-redacted,redacted,low,clipped,two_sources,unknown,,education_only,CC-BY-4.0,redacted,,fine coordinates withheld; clipped; two sources unresolved
```

Copy the header line into `labels/annotation-template.csv` at seal time. The three rows above are **synthetic fixtures** for schema tests, not field data.

## Enum allow-list (for validators)

Valid `taxon_rank`: `class,order,family,genus,species,morphospecies,unknown`

Valid `location_precision`: `landscape,site_public,redacted`

Valid `annotator_role`: `expert,trained,citizen,agent,reviewer`

Valid `consent_flag`: `public,community_consent,redacted,unknown`

---

# How this pack maps to other EchoVault leaves

| This file | Consumed by |
| --- | --- |
| LABEL-TAXONOMY.md | metadata schema v0 taxa/behavior/quality fields |
| IAA-RUBRIC.md | eval harness (human gold), peer-review rubric |
| annotation-template.csv | worked example site briefings; eval fixtures |
| Ambiguity examples | educational query UI (teach unknowns) |

---

# Artifact footer

- Open license: CC-BY-SA-4.0 (prose/taxonomy) + MIT (CSV template and enums).
- Sources / provenance: taxonomy structure is an EchoVault synthesis for open annotation. It is **not** a copy of any closed lab codebook. Rank honesty follows ordinary systematic practice (stop at evidence). Public authorities named as examples: IOC World Bird List, WoRMS. No recording files are included.
- Dual-use refuse: no covert civilian surveillance, no poaching pins, no unauthorized sensor access, no human voice identification, no medical claims.
- Forged on GrokForge: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
- No secrets, no PII, no private home paths.

## Sources

- IOC World Bird List (public taxonomy resource): https://www.worldbirdnames.org/
- WoRMS (public marine taxonomy): https://www.marinespecies.org/
- Xeno-canto recording and licensing model (public): https://xeno-canto.org/about/xeno-canto
- NOAA SanctSound program overview (public ocean sound monitoring, not a location dump): https://sanctuaries.noaa.gov/science/monitoring/sound/
- EchoVault project page: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
- No external species detections are claimed in this pack. Demo CSV rows are synthetic.

## Contributor checklist (peer-applicable)

- [ ] Hierarchy depth >= 2 on taxon, vocalization, behavior, context, quality
- [ ] Unknown tokens exist on every axis
- [ ] IAA dimensions are scored 1-5 and include rails + schema
- [ ] CSV header + >=1 synthetic example row
- [ ] >=3 ambiguity decision examples
- [ ] Sensitivity / dual-use refuse present
- [ ] License headers present
