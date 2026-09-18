# EchoVault worked example: three-site soundscape briefing pack

```
SPDX-License-Identifier: CC-BY-SA-4.0
License-Code-And-Templates: MIT
Forged on GrokForge: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
Package: examples/sites/
```

This pack is a **classroom-ready** worked example. All clip rows are **synthetic metadata** (`syn://echovault/...`). No audio files are shipped. Public programs are cited only as interoperability pointers (how a real briefing would attach licensed recordings later). Site coordinates are landscape-scale or redacted.

**Do not treat any binomial in the synthetic rows as a field detection.** They are schema-fill illustrations.

## Dual-use refuse

Refuse requests to turn these briefings into covert monitoring of people, poaching maps, nest pins, or "where to find the rare animal this week." Educational use, conservation planning at landscape scale, and open-model eval fixtures are in scope.

---

# Shared schema fill (v0-shaped)

Each site briefing fills the same record shape so educators can diff sites.

```json
{
  "clip_id": "syn://echovault/site-X/clip-NNN",
  "device": {
    "type": "autonomous_recorder",
    "model": "synthetic-generic-16khz",
    "sample_rate_hz": 16000,
    "bit_depth": 16,
    "channels": 1
  },
  "location": {
    "geohash": "optional-landscape",
    "precision": "landscape|redacted",
    "site_id": "ev-syn-...",
    "habitat": "from LABEL-TAXONOMY context.habitat"
  },
  "event": {
    "t_start_s": 0,
    "t_end_s": 8,
    "taxon_path": "...",
    "taxon_rank": "...",
    "taxon_confidence": 1,
    "vocalization_path": "...",
    "behavior_path": "behavior/unknown",
    "quality": { "snr": "medium", "integrity": "clean", "overlap": "single_source" }
  },
  "license": "CC0-1.0",
  "consent_flag": "public",
  "checksum_sha256": null,
  "synthetic": true
}
```

Uncertainty tags used below: `CONFIRMED_SYNTHETIC`, `RANK_CAPPED`, `OVERLAP`, `CLIPPED`, `REDACTED_LOCATION`, `EDUCATION_ONLY`.

---

# Site 1. Northern peatland dawn chorus (fully synthetic)

**Path:** `examples/sites/01-peatland-dawn.md`  
**Site ID:** `ev-syn-bog-north`  
**Habitat:** `wetland_or_peatland`  
**Diel:** `dawn`  
**Weather:** `clear`  
**Anthrophony:** `low`  
**Location:** landscape geohash `gcpvj` (illustrative, not a real recorder)  
**License of metadata:** CC0-1.0  
**Uncertainty:** `CONFIRMED_SYNTHETIC`, `OVERLAP` on the chorus row

## Before / after narrative (educators)

**Before (typical overconfident dump):** "This is a boreal bog at 05:12. Species list: Wilson's Snipe, Savannah Sparrow, Lincoln's Sparrow, plus a moose. Biodiversity is high. Deploy here."

Problems: invented detections, implied precise site, no SNR, no overlap, no license, a megafauna claim from a 16 kHz clip with no evidence.

**After (EchoVault briefing):** We describe a **synthetic** peatland dawn scene. We label a chorus as chorus. We cap taxon rank at order or morphospecies. We keep location at landscape scale. We mark what a student *could* ask next (segment solos; attach a real CC-licensed clip from a public archive).

## Filled records (3 events)

### Clip A1 - chorus window

```json
{
  "clip_id": "syn://echovault/site-1/clip-001",
  "device": {"type": "autonomous_recorder", "model": "synthetic-generic-16khz", "sample_rate_hz": 16000, "bit_depth": 16, "channels": 1},
  "location": {"geohash": "gcpvj", "precision": "landscape", "site_id": "ev-syn-bog-north", "habitat": "wetland_or_peatland"},
  "event": {
    "t_start_s": 0.0,
    "t_end_s": 10.0,
    "taxon_path": "biotic/animals/birds/passeriformes",
    "taxon_rank": "order",
    "taxon_latin": "",
    "taxon_confidence": 2,
    "vocalization_path": "vocalization/chorus",
    "behavior_path": "behavior/unknown",
    "quality": {"snr": "medium", "integrity": "clean", "overlap": "chorus_or_many"}
  },
  "usable_for": ["soundscape_index", "education_only"],
  "license": "CC0-1.0",
  "consent_flag": "public",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC", "OVERLAP", "RANK_CAPPED"],
  "notes": "Do not promote to species list. Segment solos before ID tasks."
}
```

### Clip A2 - single mechanical-like motif (still not a species ID)

```json
{
  "clip_id": "syn://echovault/site-1/clip-002",
  "device": {"type": "autonomous_recorder", "model": "synthetic-generic-16khz", "sample_rate_hz": 16000, "bit_depth": 16, "channels": 1},
  "location": {"geohash": "gcpvj", "precision": "landscape", "site_id": "ev-syn-bog-north", "habitat": "wetland_or_peatland"},
  "event": {
    "t_start_s": 12.4,
    "t_end_s": 14.1,
    "taxon_path": "biotic/animals/birds",
    "taxon_rank": "class",
    "taxon_confidence": 2,
    "vocalization_path": "vocalization/drum_or_mechanical",
    "behavior_path": "behavior/unknown",
    "quality": {"snr": "high", "integrity": "clean", "overlap": "single_source"}
  },
  "usable_for": ["education_only", "presence_model"],
  "license": "CC0-1.0",
  "consent_flag": "public",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC", "RANK_CAPPED"],
  "notes": "Winnow-like or drum-like synthetic motif. Class-level only."
}
```

### Clip A3 - distant motor (anthrophony)

```json
{
  "clip_id": "syn://echovault/site-1/clip-003",
  "device": {"type": "autonomous_recorder", "model": "synthetic-generic-16khz", "sample_rate_hz": 16000, "bit_depth": 16, "channels": 1},
  "location": {"geohash": "gcpvj", "precision": "landscape", "site_id": "ev-syn-bog-north", "habitat": "wetland_or_peatland"},
  "event": {
    "t_start_s": 40.0,
    "t_end_s": 55.0,
    "taxon_path": "anthropogenic",
    "taxon_rank": "unknown",
    "taxon_confidence": 1,
    "vocalization_path": "vocalization/anthrophony_event",
    "behavior_path": "behavior/not_applicable",
    "quality": {"snr": "low", "integrity": "clean", "overlap": "single_source"}
  },
  "usable_for": ["soundscape_index"],
  "license": "CC0-1.0",
  "consent_flag": "public",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC"],
  "notes": "Distant motor pass. Keep as soundscape pressure, not a wildlife ID."
}
```

## Site 1 teaching points

- Chorus != species list.
- Anthrophony gets its own row so biodiversity indices are not silently polluted.
- `usable_for` is narrower than "we recorded something."

---

# Site 2. Temperate marine sanctuary, metadata-only (synthetic rows + public program pointer)

**Path:** `examples/sites/02-marine-sanctuary.md`  
**Site ID:** `ev-syn-coast-redacted`  
**Habitat:** `marine_or_coastal`  
**Diel:** `day`  
**Weather:** `windy`  
**Anthrophony:** `moderate`  
**Location:** `precision=redacted` (no geohash). Coastal sanctuaries can include sensitive haul-outs.  
**License of metadata:** CC-BY-4.0  
**Uncertainty:** `CONFIRMED_SYNTHETIC`, `REDACTED_LOCATION`, `CLIPPED` on one row

## Public pointer (not a recording ID)

NOAA National Marine Sanctuaries documents a public ocean-sound monitoring program (SanctSound) with open science goals. EchoVault does **not** ingest SanctSound files in this pack. A later steward may attach only records that already carry a public license and coarse location.

Pointer: https://sanctuaries.noaa.gov/science/monitoring/sound/

No SanctSound station codes, hydrophone serials, or lat/long appear here on purpose.

## Before / after narrative

**Before:** "Hydrophone 14 at [exact cove]: blue whale at 02:00, then a ship. Share the pin so boaters can go see them."

**After:** Redact location. Split biological and ship events. If peaks clip, drop ID-model use. Whale *species* is not asserted from a synthetic clip; rank is capped at `cetacea` or `unknown`.

## Filled records

### Clip B1 - low-frequency tonal, rank capped

```json
{
  "clip_id": "syn://echovault/site-2/clip-001",
  "device": {"type": "hydrophone", "model": "synthetic-generic-48khz", "sample_rate_hz": 48000, "bit_depth": 24, "channels": 1},
  "location": {"geohash": "", "precision": "redacted", "site_id": "ev-syn-coast-redacted", "habitat": "marine_or_coastal"},
  "event": {
    "t_start_s": 2.0,
    "t_end_s": 18.0,
    "taxon_path": "biotic/animals/mammals/cetacea",
    "taxon_rank": "order",
    "taxon_confidence": 2,
    "vocalization_path": "vocalization/call",
    "behavior_path": "behavior/unknown",
    "quality": {"snr": "medium", "integrity": "clean", "overlap": "single_source"}
  },
  "usable_for": ["education_only", "presence_model"],
  "license": "CC-BY-4.0",
  "consent_flag": "redacted",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC", "REDACTED_LOCATION", "RANK_CAPPED"],
  "notes": "Not a species claim. Not a whale-watching pin."
}
```

### Clip B2 - ship-like broadband, clipped

```json
{
  "clip_id": "syn://echovault/site-2/clip-002",
  "device": {"type": "hydrophone", "model": "synthetic-generic-48khz", "sample_rate_hz": 48000, "bit_depth": 24, "channels": 1},
  "location": {"geohash": "", "precision": "redacted", "site_id": "ev-syn-coast-redacted", "habitat": "marine_or_coastal"},
  "event": {
    "t_start_s": 30.0,
    "t_end_s": 90.0,
    "taxon_path": "anthropogenic",
    "taxon_rank": "unknown",
    "taxon_confidence": 1,
    "vocalization_path": "vocalization/anthrophony_event",
    "behavior_path": "behavior/not_applicable",
    "quality": {"snr": "high", "integrity": "clipped", "overlap": "two_sources"}
  },
  "usable_for": ["education_only"],
  "license": "CC-BY-4.0",
  "consent_flag": "redacted",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC", "REDACTED_LOCATION", "CLIPPED", "OVERLAP"],
  "notes": "Clipped ship-like pass. Unusable for ID models. Possible biological underlay unresolved."
}
```

### Clip B3 - unknown pulse train (honest unknown)

```json
{
  "clip_id": "syn://echovault/site-2/clip-003",
  "device": {"type": "hydrophone", "model": "synthetic-generic-48khz", "sample_rate_hz": 48000, "bit_depth": 24, "channels": 1},
  "location": {"geohash": "", "precision": "redacted", "site_id": "ev-syn-coast-redacted", "habitat": "marine_or_coastal"},
  "event": {
    "t_start_s": 100.0,
    "t_end_s": 104.5,
    "taxon_path": "taxon/unknown",
    "taxon_rank": "unknown",
    "taxon_confidence": 1,
    "vocalization_path": "vocalization/unknown",
    "behavior_path": "behavior/unknown",
    "quality": {"snr": "low", "integrity": "clean", "overlap": "single_source"}
  },
  "usable_for": ["education_only"],
  "license": "CC-BY-4.0",
  "consent_flag": "redacted",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC", "REDACTED_LOCATION"],
  "notes": "Unknown pulse train. Fish, invert, device, or processing artifact. Leave unknown."
}
```

## Site 2 teaching points

- Marine sites default toward redaction.
- Clipping is a first-class quality label.
- `unknown` is a successful annotation.

---

# Site 3. Urban remnant woodland (fully synthetic)

**Path:** `examples/sites/03-urban-woodland.md`  
**Site ID:** `ev-syn-urban-park`  
**Habitat:** `urban_or_periurban`  
**Diel:** `dusk`  
**Weather:** `clear`  
**Anthrophony:** `high`  
**Location:** landscape geohash `9q8yy` (illustrative)  
**License of metadata:** CC0-1.0  
**Uncertainty:** `CONFIRMED_SYNTHETIC`, `OVERLAP`, `EDUCATION_ONLY` on speech-adjacent rows

## Before / after narrative

**Before:** "City park, 19:40. Identify the people talking on the path and the owl. Publish the bench GPS."

**After:** Speech is `anthrophony_event` with **no speaker ID**. Owl-like motif stays at class/order with low confidence. GPS stays landscape-scale. Students practice ignoring voices as identity objects.

## Filled records

### Clip C1 - speech-like burst (no person ID)

```json
{
  "clip_id": "syn://echovault/site-3/clip-001",
  "device": {"type": "autonomous_recorder", "model": "synthetic-generic-16khz", "sample_rate_hz": 16000, "bit_depth": 16, "channels": 1},
  "location": {"geohash": "9q8yy", "precision": "landscape", "site_id": "ev-syn-urban-park", "habitat": "urban_or_periurban"},
  "event": {
    "t_start_s": 1.0,
    "t_end_s": 4.2,
    "taxon_path": "anthropogenic",
    "taxon_rank": "unknown",
    "taxon_confidence": 1,
    "vocalization_path": "vocalization/anthrophony_event",
    "behavior_path": "behavior/not_applicable",
    "quality": {"snr": "high", "integrity": "clean", "overlap": "single_source"}
  },
  "usable_for": ["soundscape_index"],
  "license": "CC0-1.0",
  "consent_flag": "public",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC", "EDUCATION_ONLY"],
  "notes": "Speech-like. Never run speaker recognition. Dual-use refuse."
}
```

### Clip C2 - possible owl-like motif, low confidence

```json
{
  "clip_id": "syn://echovault/site-3/clip-002",
  "device": {"type": "autonomous_recorder", "model": "synthetic-generic-16khz", "sample_rate_hz": 16000, "bit_depth": 16, "channels": 1},
  "location": {"geohash": "9q8yy", "precision": "landscape", "site_id": "ev-syn-urban-park", "habitat": "urban_or_periurban"},
  "event": {
    "t_start_s": 8.0,
    "t_end_s": 9.1,
    "taxon_path": "biotic/animals/birds/strigiformes",
    "taxon_rank": "order",
    "taxon_confidence": 2,
    "vocalization_path": "vocalization/call",
    "behavior_path": "behavior/unknown",
    "quality": {"snr": "medium", "integrity": "clean", "overlap": "two_sources"}
  },
  "usable_for": ["education_only"],
  "license": "CC0-1.0",
  "consent_flag": "public",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC", "RANK_CAPPED", "OVERLAP"],
  "notes": "Owl-like synthetic motif under city noise. Order-level cap. Not a nest pin."
}
```

### Clip C3 - insect chorus at dusk

```json
{
  "clip_id": "syn://echovault/site-3/clip-003",
  "device": {"type": "autonomous_recorder", "model": "synthetic-generic-16khz", "sample_rate_hz": 16000, "bit_depth": 16, "channels": 1},
  "location": {"geohash": "9q8yy", "precision": "landscape", "site_id": "ev-syn-urban-park", "habitat": "urban_or_periurban"},
  "event": {
    "t_start_s": 20.0,
    "t_end_s": 40.0,
    "taxon_path": "biotic/animals/insects",
    "taxon_rank": "class",
    "taxon_confidence": 3,
    "vocalization_path": "vocalization/chorus",
    "behavior_path": "behavior/unknown",
    "quality": {"snr": "high", "integrity": "clean", "overlap": "chorus_or_many"}
  },
  "usable_for": ["soundscape_index", "education_only"],
  "license": "CC0-1.0",
  "consent_flag": "public",
  "checksum_sha256": null,
  "tags": ["CONFIRMED_SYNTHETIC", "OVERLAP"],
  "notes": "Insect chorus. Class-level. Good for soundscape indices, weak for species ID."
}
```

## Site 3 teaching points

- People in parks are anthrophony, not a taxon to identify.
- Urban SNR can be high for insects and still useless for bird species ID.
- Landscape geohash is enough for a classroom map.

---

# Cross-site comparison (peer-review layout)

| | Site 1 peatland | Site 2 marine | Site 3 urban |
| --- | --- | --- | --- |
| Synthetic? | yes | yes | yes |
| Location | landscape geohash | redacted | landscape geohash |
| Dominant issue | chorus overlap | clipping + sensitivity | speech + city noise |
| Safe usable_for | soundscape_index | education_only | soundscape_index |
| Agent refusal drill | no species list from chorus | no haul-out pin | no speaker ID |

## Classroom sequence (offline)

1. Print the three JSON blocks (no network required).
2. Students tag each record with the uncertainty vocabulary.
3. Students rewrite the "Before" paragraph into an EchoVault-compliant after.
4. Optional: attach a **real** public-license clip from Xeno-canto later, copying license and catalog ID into `clip_id` (never invent XC numbers).

---

# Artifact footer

- Open license: CC-BY-SA-4.0 (prose) + MIT (JSON fixtures).
- Sources / provenance: all `syn://echovault/...` rows are synthetic. No field detections are claimed. Public program pointer: NOAA SanctSound overview. Additional public archives for future real clips: Xeno-canto, Australian Acoustic Observatory, Macaulay Library (each record keeps its own license).
- Dual-use refuse: no covert civilian surveillance, no poaching pins, no speaker identification, no unauthorized hydrophone access.
- Forged on GrokForge: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
- No secrets, no PII, no private home paths.

## Sources

- NOAA SanctSound / sanctuary sound monitoring (public overview): https://sanctuaries.noaa.gov/science/monitoring/sound/
- Xeno-canto (public wildlife sound archive; do not invent recording IDs): https://xeno-canto.org/about/xeno-canto
- Australian Acoustic Observatory (public continental acoustic program): https://acousticobservatory.org/
- Cornell Lab of Ornithology Macaulay Library (public media archive; per-item licenses): https://www.macaulaylibrary.org/
- EchoVault project: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder

## Peer-review checklist

- [ ] Three site briefings present
- [ ] Schema-shaped JSON examples filled
- [ ] Uncertainty tags on every record
- [ ] Synthetic disclaimer explicit
- [ ] Before/after educator narrative
- [ ] Location sensitivity demonstrated (at least one redacted site)
- [ ] Footer + licenses
