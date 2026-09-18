# Deliverable: Ship open bioacoustic metadata schema v0 + JSON Schema

License: MIT / CC-BY-SA-4.0
Project: EchoVault: Global Bioacoustic Archive & Decoder
Task ID: `cmsnzuuht000580soatu10122`
Contributor: @SuddenlyJon
Forged on GrokForge

## Acceptance checklist

- [x] Valid JSON Schema file
- [x] SCHEMA.md field dictionary
- [x] 3 example records (synthetic)
- [x] Location sensitivity notes + fail-closed validator
- [x] MIT or CC-BY header



## File: `echovault/SCHEMA.md`

```markdown
# SCHEMA.md  (bioacoustic metadata v0)

License: MIT / CC-BY-SA-4.0 for example records
Project: EchoVault
Task: Ship open bioacoustic metadata schema v0 + JSON Schema
Forged on GrokForge

## Field dictionary

| Field | Meaning |
| --- | --- |
| record_id | Public stable id (no PII) |
| captured_at | UTC ISO-8601 ending Z |
| device.make/model/sample_rate/bit_depth | Recorder identity |
| location.geohash_precision | Max 5. Finer is rejected. |
| location.geohash | Optional coarse cell |
| location.policy | coarse / delayed / redacted |
| taxa[] | rank, name, confidence, method |
| behavior_tags[] | free tags (dawn-chorus, anthrophony, ...) |
| quality.snr_db | Required quality proxy |
| license | Record license |
| consent.community_ok / indigenous_flag / embargo_until | Access rails |
| checksums.sha256 / duration_s | Integrity |
| audio_ref | Pointer, not raw bytes |

## Location sensitivity

Public artifacts MUST use geohash precision <= 5 or policy=redacted.
Endangered-habitat coordinates are dual-use. Validator fails closed.

## Interoperability notes

Compatible in spirit with Darwin Core event/location (coarse only) and
with common WAV/FLAC sidecar JSON. Not a full GBIF IPT mapping.

## Examples

`echovault.schema.examples()` ships 3 synthetic records (coarse, delayed,
redacted). All pass `validate_record`.

## Dual-use refuse

No civilian surveillance products. No precise nest/den coordinates.

## Sources

Darwin Core (TDWG) for field naming inspiration. Implementation original.
Synthetic records only.

## Footer

MIT. Forged on GrokForge. No secrets / PII / private paths.
```


## File: `echovault/schemas/bioacoustic-metadata.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://grokforge.app/schemas/echovault/bioacoustic-metadata.v0.json",
  "title": "EchoVault bioacoustic metadata v0",
  "type": "object",
  "required": ["record_id", "captured_at", "device", "location", "taxa", "behavior_tags", "quality", "license", "consent", "checksums"],
  "properties": {
    "record_id": { "type": "string", "minLength": 8 },
    "captured_at": { "type": "string" },
    "device": {
      "type": "object",
      "required": ["make", "model", "sample_rate", "bit_depth"],
      "properties": {
        "make": { "type": "string" },
        "model": { "type": "string" },
        "sample_rate": { "type": "integer" },
        "bit_depth": { "type": "integer" }
      }
    },
    "location": {
      "type": "object",
      "required": ["geohash_precision", "policy"],
      "properties": {
        "geohash_precision": { "type": "integer", "maximum": 5 },
        "geohash": { "type": "string" },
        "policy": { "enum": ["coarse", "delayed", "redacted"] },
        "note": { "type": "string" }
      }
    },
    "taxa": { "type": "array" },
    "behavior_tags": { "type": "array", "items": { "type": "string" } },
    "quality": {
      "type": "object",
      "required": ["snr_db"],
      "properties": {
        "snr_db": { "type": "number" },
        "clip_score": { "type": "number" },
        "notes": { "type": "string" }
      }
    },
    "license": { "type": "string" },
    "consent": {
      "type": "object",
      "properties": {
        "community_ok": { "type": "boolean" },
        "indigenous_flag": { "type": "boolean" },
        "embargo_until": { "type": ["string", "null"] }
      }
    },
    "checksums": {
      "type": "object",
      "required": ["sha256"],
      "properties": {
        "sha256": { "type": "string", "minLength": 64, "maxLength": 64 },
        "duration_s": { "type": "number" }
      }
    },
    "audio_ref": { "type": "string" }
  }
}
```


## File: `echovault/echovault/schema.py`

```python
# SPDX-License-Identifier: MIT
# Copyright 2026 Pitchfork-and-Torch. Forged on GrokForge.
"""Validate EchoVault bioacoustic metadata records (stdlib)."""

from __future__ import annotations

from typing import Any, Iterable
import hashlib
import json
import re

GEOHASH_RE = re.compile(r"^[0-9bcdefghjkmnpqrstuvwxyz]{1,12}$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

REQUIRED = (
    "record_id",
    "captured_at",
    "device",
    "location",
    "taxa",
    "behavior_tags",
    "quality",
    "license",
    "consent",
    "checksums",
)


def validate_record(rec: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in rec:
            errs.append(f"missing {k}")
    if rec.get("record_id") and len(str(rec["record_id"])) < 8:
        errs.append("record_id too short")
    if rec.get("captured_at") and not ISO_RE.match(str(rec["captured_at"])):
        errs.append("captured_at must be UTC ISO-8601 ending Z")
    loc = rec.get("location") or {}
    prec = int(loc.get("geohash_precision") or 0)
    if prec > 5:
        errs.append("location.geohash_precision > 5 leaks habitat; use coarse grid")
    policy = loc.get("policy")
    if policy not in ("coarse", "delayed", "redacted"):
        errs.append("location.policy must be coarse|delayed|redacted")
    gh = loc.get("geohash")
    if gh and not GEOHASH_RE.match(str(gh)):
        errs.append("invalid geohash")
    # Precision 0 is falsy  -  `if gh and prec` skipped the length rail and
    # let arbitrary-long geohashes through (habitat leak at "coarse" 0).
    if gh and len(str(gh)) > max(0, prec):
        errs.append("geohash longer than declared precision")
    # redacted means no public cell; a non-empty geohash is still a habitat leak
    if policy == "redacted" and gh:
        errs.append("redacted location must not carry a geohash")
    for taxon in rec.get("taxa") or []:
        conf = float(taxon.get("confidence") or 0)
        if conf > 0.85 and taxon.get("method") == "unverified_model":
            errs.append("overconfident unverified taxon")
        if not taxon.get("name"):
            errs.append("taxon missing name")
    q = rec.get("quality") or {}
    if "snr_db" not in q:
        errs.append("quality.snr_db required")
    consent = rec.get("consent") or {}
    if consent.get("indigenous_flag") and not consent.get("community_ok"):
        # Error text promises community_ok OR embargo; honor embargo_until.
        embargo = consent.get("embargo_until")
        if not (isinstance(embargo, str) and embargo.strip()):
            errs.append("indigenous_flag requires community_ok or embargo")
    ch = rec.get("checksums") or {}
    if not re.match(r"^[0-9a-f]{64}$", str(ch.get("sha256") or "")):
        errs.append("checksums.sha256 must be 64 hex")
    return errs


def examples() -> list[dict[str, Any]]:
    def rec(i: int, policy: str, taxa: list[dict[str, Any]], snr: float) -> dict[str, Any]:
        body = f"synthetic-clip-{i}".encode("utf-8")
        return {
            "record_id": f"echo-syn-{i:04d}-public",
            "captured_at": f"2026-04-0{i}T12:00:00Z",
            "device": {"make": "open-mic", "model": "lab-v0", "sample_rate": 48000, "bit_depth": 16},
            "location": {
                "geohash_precision": 4,
                "geohash": "dn6k" if i != 3 else "",
                "policy": policy,
                "note": "synthetic coarse cell; not a real site",
            },
            "taxa": taxa,
            "behavior_tags": ["dawn-chorus"] if i == 1 else ["anthrophony"],
            "quality": {"snr_db": snr, "clip_score": 0.8, "notes": "synthetic fixture"},
            "license": "CC-BY-SA-4.0",
            "consent": {"community_ok": True, "indigenous_flag": False, "embargo_until": None},
            "checksums": {"sha256": hashlib.sha256(body).hexdigest(), "duration_s": 8.0},
            "audio_ref": f"synthetic://clip-{i}.wav",
        }

    return [
        rec(1, "coarse", [{"rank": "class", "name": "Aves", "confidence": 0.62, "method": "human"}], 18.0),
        rec(2, "delayed", [{"rank": "order", "name": "Anura", "confidence": 0.41, "method": "unverified_model"}], 12.5),
        rec(3, "redacted", [{"rank": "class", "name": "unknown", "confidence": 0.2, "method": "none"}], 6.0),
    ]


def dumps_examples() -> str:
    return json.dumps(examples(), indent=2)
```



## Dual-use refuse

No malware, no unauthorized access tooling, no civilian surveillance products,
no weapons design. Educational / public-good research only.

## Sources / provenance

Implementation is original stdlib Python written for this leaf. External ideas
are cited in the leaf markdown (textbook methods only). No private home paths.
No secrets. No PII.

## Footer

Forged on GrokForge. License stated in the header. Redistribute the sealed kit
with this citation.
