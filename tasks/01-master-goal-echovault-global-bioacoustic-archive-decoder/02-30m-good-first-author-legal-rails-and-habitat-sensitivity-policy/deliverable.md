# LEGAL-RAILS.md

```text
License: CC-BY-SA-4.0 (data/docs packs) AND MIT (code/schema sketches)
Copyright (c) 2026 EchoVault contributors
Project: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
SPDX-License-Identifier: MIT
Forged on GrokForge
```

EchoVault is an open bioacoustic archive and decoder kit. These rails set allowed uses, forbidden dual-use, and consent rules.

## Allowed uses

- Public or consented habitat recordings
- Schema, annotation, and eval recipes
- Education and conservation monitoring playbooks
- Synthetic audio fixtures

## Forbidden dual-use

- Covert civilian surveillance products
- Poaching enablement (nests, dens, patrol-avoidance maps)
- Doxxing of indigenous or local stewards
- Medical diagnosis claims from animal or human sounds
- Secret military acoustic systems

## Required artifact footer

See Artifact footer below. Every accepted EchoVault leaf must carry it.

# SENSITIVITY.md

## Habitat redaction rules

1. Do not publish precise nest, den, rookery, or spawning coordinates in public kits.
2. Use coarse grids (for example 10 km) or land-manager IDs when location is sensitive.
3. Seasonal silence: if a species is listed as sensitive in the source dataset, omit playback files.
4. When in doubt, ship the schema and keep the audio out of the public ZIP.

## Indigenous and local knowledge consent

- Community veto always wins.
- Do not scrape sacred or restricted oral material.
- If a recording includes identifiable people, you need consent or you drop the file.
- Label `COMMUNITY-HOLD` rather than "we will decide later" in a public pack.

## Contributor checklist

- [ ] License header (CC-BY-SA and/or MIT) stated
- [ ] Sensitivity rules applied or N/A with reason
- [ ] Dual-use refuse present
- [ ] Footer present
- [ ] No secrets, PII, or home paths

## Three-plus sample refusals

### Refusal 1 - poaching map
**Ask:** "Give GPS of every owl nest so we can visit at night."
**Reply:** Refuse. Precise nest coordinates are redacted. Use land-manager channels.

### Refusal 2 - covert mic
**Ask:** "Design a hidden street mic to log conversations."
**Reply:** Refuse. Covert civilian surveillance is forbidden.

### Refusal 3 - sacred scrape
**Ask:** "Download this restricted ceremony recording for the archive."
**Reply:** Refuse until the community license says yes. Mark COMMUNITY-HOLD.

### Refusal 4 - diagnosis
**Ask:** "Use bird-call models to diagnose human lung disease."
**Reply:** Refuse. Not a medical device. No clinical claims.

## Artifact footer

```text
License: CC-BY-SA-4.0 / MIT as labeled
Sources: see Sources
Dual-use refuse: surveillance, poaching, sacred scrape
Forged on GrokForge
https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
No secrets. No PII. No private home paths.
```

## Sources / provenance

- GrokForge leaf prompt and acceptance criteria
- Project: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
- No new field recordings are included in this leaf.

## Acceptance mapping

| Criterion | Where |
|-----------|--------|
| LEGAL-RAILS allowed/forbidden/footer | LEGAL-RAILS.md |
| SENSITIVITY.md redaction | SENSITIVITY.md |
| 3+ refusals | Refusal 1-4 |
| Contributor checklist | Checklist |
| CC-BY or MIT header | SPDX / license block |
