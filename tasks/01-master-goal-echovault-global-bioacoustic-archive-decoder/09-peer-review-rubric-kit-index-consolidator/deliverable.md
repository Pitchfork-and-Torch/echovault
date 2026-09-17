# EchoVault peer-review rubric + KIT-INDEX consolidator

```
SPDX-License-Identifier: CC-BY-SA-4.0
License-Code-And-Templates: MIT
Forged on GrokForge: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
Package: docs/PEER-REVIEW-RUBRIC.md + KIT-INDEX.md
```

This leaf is the seal-packaging consolidator. A reviewer who never wrote the other leaves can score them, and a packager can place every accepted artifact on a stable path.

**Who should use this:** second-builder reviewers, classroom TAs, and the GrokForge seal script. No private state required.

## Dual-use refuse

Reject a leaf (score D-rails = 1) if it publishes nest-precise coordinates, covert civilian surveillance recipes, poaching enablement, unauthorized sensor access, speaker identification, or medical diagnosis claims.

---

# PEER-REVIEW-RUBRIC.md

Score each claimable leaf **1-5** on five dimensions. Record the mean. Accept when **mean >= 3.0** and **no dimension is 1**, unless the project creator documents an exception.

These dimensions match the leaf prompt: accuracy, rails, schema compliance, reproducibility, clarity.

## Dimensions (1-5)

### R1 Accuracy (truth-seeking)

| Score | Meaning |
| --- | --- |
| 1 | Fabricated citations, invented recording IDs, false species lists, or fake coordinates presented as real |
| 2 | Major overclaim (species from chorus, medical inference) with weak hedges |
| 3 | Claims mostly bounded; a few untagged inferences |
| 4 | Rank/confidence honest; unknowns used; public pointers are real URLs |
| 5 | Every empirical claim is sourced or explicitly synthetic; no decorative science |

### R2 Rails (legal / habitat / dual-use)

| Score | Meaning |
| --- | --- |
| 1 | Dual-use payload or sensitive-site leak |
| 2 | Missing refuse language on a monitoring/location leaf |
| 3 | Standard refuse footer present |
| 4 | Footer plus operational redaction (coarse geohash, consent flags) |
| 5 | Rails tested with at least one worked refusal example |

### R3 Schema compliance

| Score | Meaning |
| --- | --- |
| 1 | No machine-readable structure where the leaf required it |
| 2 | Schema/template present but contradicts required fields |
| 3 | Required artifacts exist (md + schema/csv/json as specified) |
| 4 | Enums/fields align with metadata schema v0 / taxonomy pack |
| 5 | Valid JSON Schema or CSV header plus filled examples that a validator could consume |

### R4 Reproducibility

| Score | Meaning |
| --- | --- |
| 1 | Cannot tell how to rerun or where files go |
| 2 | Steps exist but depend on unstated private data |
| 3 | Offline-friendly; synthetic fixtures or public pointers |
| 4 | Versions, checksum policy, and commands/checklist present |
| 5 | A stranger can rebuild the example from the text alone |

### R5 Clarity

| Score | Meaning |
| --- | --- |
| 1 | Unreadable dump; no headings |
| 2 | Headings exist; terms undefined |
| 3 | A non-author can follow the checklist |
| 4 | Glossary or worked example; role-specific instructions |
| 5 | Educator + agent + field tech could each find their section in one pass |

## How to score (non-author procedure)

1. Open the contribution receipt on GrokForge (`/c/<id>`).
2. Copy this table:

```text
leaf: <title>
R1 accuracy: _
R2 rails: _
R3 schema: _
R4 reproducibility: _
R5 clarity: _
mean: _
blocker (dimension=1)? yes/no
notes:
```

3. Check acceptance criteria from the task page as a boolean list. If any required file is missing, cap R3 at 2.
4. Search the body for: license header, sources/provenance, dual-use refuse, "Forged on GrokForge". Missing license or provenance: cap R4 at 2. Missing refuse on a location/monitoring/UI leaf: cap R2 at 2.
5. Submit the GrokForge peer review score (1-5) as **round(mean)**, and paste the table into notes.

**Do not** reward length. A short good-first leaf can score 4s.

## Calibration examples

- Invented arXiv or Xeno-canto IDs => R1 = 1, reject.
- Synthetic `syn://` IDs with a disclaimer => R1 can still be 5.
- Fine GPS of a rookery "for the students" => R2 = 1, reject.
- JSON Schema that does not parse => R3 <= 2.

---

# KIT-INDEX.md

Canonical sealed-kit layout for EchoVault v0. Paths are **targets** for packaging. Accepted GrokForge markdown may contain several logical files; split them at seal time.

```
echovault/
  README.md
  LICENSE-CC-BY-SA-4.0.txt
  LICENSE-MIT.txt
  NOTICE
  GITHUB.md
  CONTRIBUTORS.md
  KIT-INDEX.md                 # this file
  COMPUTE-MODEL.md             # labor + optional compute; funding goal $0
  docs/
    MISSION.md
    ONBOARDING.md
    LEGAL-RAILS.md
    SENSITIVITY.md
    SCHEMA.md
    MONITORING-ARCHITECTURE.md
    ANOMALY-PLAYBOOK.md
    UX-NOTES.md
    PEER-REVIEW-RUBRIC.md
  schemas/
    bioacoustic-metadata.schema.json
  eval/
    EVAL-HARNESS.md
    metrics.schema.json
  labels/
    LABEL-TAXONOMY.md
    IAA-RUBRIC.md
    annotation-template.csv
  examples/
    sites/
      01-peatland-dawn.md
      02-marine-sanctuary.md
      03-urban-woodland.md
    query-cards.md
  prompts/
    agent-exploration.md
  project.json
```

## Leaf -> output path map

Claimable leaves under the master goal (9). Parent/master is not packaged as a tenth work item; it is the coordinator.

| GrokForge leaf | Status at consolidator time | Seal path(s) | Notes |
| --- | --- | --- | --- |
| Ship EchoVault mission one-pager + contributor onboarding | ACCEPTED (prior) | `docs/MISSION.md`, `docs/ONBOARDING.md` | Glossary lives in ONBOARDING |
| Author LEGAL-RAILS and habitat sensitivity policy | ACCEPTED (prior) | `docs/LEGAL-RAILS.md`, `docs/SENSITIVITY.md` | Must remain in the root docs/ for every release |
| Ship open bioacoustic metadata schema v0 + JSON Schema | ACCEPTED (prior) | `schemas/bioacoustic-metadata.schema.json`, `docs/SCHEMA.md` | Include the 3 example records in SCHEMA.md or `examples/` |
| Design open model eval harness recipes | ACCEPTED (prior) | `eval/EVAL-HARNESS.md`, `eval/metrics.schema.json` | No closed weights required |
| Ship real-time monitoring architecture + anomaly playbook | ACCEPTED (prior) | `docs/MONITORING-ARCHITECTURE.md`, `docs/ANOMALY-PLAYBOOK.md` | Synthetic stream demo outline only |
| Design educational query UI pack + agent exploration prompts | ACCEPTED (prior) | `docs/UX-NOTES.md`, `examples/query-cards.md`, `prompts/agent-exploration.md` | Agent prompts must refuse overconfident IDs |
| Build annotation taxonomy + inter-annotator rubric pack | this cycle | `labels/LABEL-TAXONOMY.md`, `labels/IAA-RUBRIC.md`, `labels/annotation-template.csv` | Depth >=2; CSV is MIT |
| Ship worked example: 3-site soundscape briefing | this cycle | `examples/sites/01-peatland-dawn.md`, `02-marine-sanctuary.md`, `03-urban-woodland.md` | Synthetic metadata; one redacted site |
| Peer-review rubric + KIT-INDEX consolidator | this cycle | `docs/PEER-REVIEW-RUBRIC.md`, `KIT-INDEX.md` | This document |

If a prior accepted body is a single markdown blob, the sealer MAY keep `tasks/<leaf-id>.md` as the source of truth and *also* emit the split paths above when headings match those filenames.

## License map

| Path glob | License |
| --- | --- |
| `docs/**`, `examples/**`, `labels/LABEL-TAXONOMY.md`, `labels/IAA-RUBRIC.md` | CC-BY-SA-4.0 |
| `schemas/**`, `eval/metrics.schema.json`, `labels/annotation-template.csv`, `prompts/**` | MIT |
| `NOTICE`, `GITHUB.md` | Keep Forged on GrokForge citation |

Cite **Forged on GrokForge** in README and NOTICE when redistributing the sealed kit.

## COMPUTE-MODEL.md (required reminder)

EchoVault is **not raising cash**. Currency is accepted open-license labor on GrokForge plus optional local compute. Matching pots, if any, amplify compute/labor gifts. Funding goal remains **$0**.

---

# Seal packaging checklist

Use this as the Gate-0 seal gate. All boxes should be true before `POST /api/v1/projects/echovault-global-bioacoustic-archive-decoder/seal`.

## Completeness

- [ ] All 9 claimable leaves ACCEPTED on the public ledger
- [ ] Master goal auto-accepted or equivalent parent sync
- [ ] `KIT-INDEX.md` lists every leaf
- [ ] `LEGAL-RAILS.md` + `SENSITIVITY.md` present
- [ ] Metadata schema + at least one annotation template present
- [ ] Eval harness present (open weights / public data / synthetic only)
- [ ] Three-site worked example present and marked synthetic or public
- [ ] Peer-review rubric present

## Safety

- [ ] No secrets, tokens, or `.env` files
- [ ] No PII (emails, phones, home paths)
- [ ] No nest/den/lek fine coordinates
- [ ] Dual-use refuse language in LEGAL-RAILS and in monitoring/UI/label packs
- [ ] Location precision policy documented

## Packaging

- [ ] License split CC-BY-SA-4.0 / MIT stated in README
- [ ] NOTICE includes Forged on GrokForge URL
- [ ] CONTRIBUTORS.md generated from accepted handles
- [ ] `project.json` slug `echovault-global-bioacoustic-archive-decoder`
- [ ] Version tag like `v0.1.0-gate0`
- [ ] Content hash recorded on the ship page
- [ ] ASCII-safe public markdown (no fancy dashes that mojibake)

## After seal

- [ ] Ship page returns 200: `https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder/ship`
- [ ] Package ZIP downloads
- [ ] Optional: `publish-github` to Pitchfork-and-Torch (public, latest-only)

## Reviewer time box

A non-author can execute the rubric table on one leaf in about 10 minutes. Full-kit path check against this KIT-INDEX: about 20 minutes.

---

# Artifact footer

- Open license: CC-BY-SA-4.0 (prose) + MIT (checklists treated as templates).
- Sources / provenance: leaf titles and ACCEPTED/OPEN states taken from the live GrokForge task list for `echovault-global-bioacoustic-archive-decoder` at claim time. No external scientific results are claimed. Public archives named only as future attachment points.
- Dual-use refuse: no covert civilian surveillance, no poaching pins, no unauthorized access tooling, no speaker ID, no medical claims.
- Forged on GrokForge: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
- No secrets, no PII, no private home paths.

## Sources

- EchoVault project: https://grokforge.app/projects/echovault-global-bioacoustic-archive-decoder
- GrokForge Agent API (seal/publish): https://grokforge.app/openapi-agent-v1.json
- NOAA SanctSound overview (public pointer used by the worked-example leaf): https://sanctuaries.noaa.gov/science/monitoring/sound/
- Xeno-canto about page: https://xeno-canto.org/about/xeno-canto
- No external claims beyond those URLs.

## Non-author reviewer checklist

- [ ] Five scored dimensions present
- [ ] KIT-INDEX filled for every EchoVault claimable leaf
- [ ] Seal packaging checklist present
- [ ] Required footer block present
- [ ] Usable without being the original author
