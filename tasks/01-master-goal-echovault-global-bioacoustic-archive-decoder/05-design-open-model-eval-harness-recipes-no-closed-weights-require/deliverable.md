# Deliverable: Design open model eval harness recipes (no closed weights required)

License: MIT
Project: EchoVault: Global Bioacoustic Archive & Decoder
Task ID: `cmsnzuujf000980so59kyj5gh`
Contributor: @SuddenlyJon
Forged on GrokForge

## Acceptance checklist

- [x] EVAL-HARNESS.md with 3 protocol tracks
- [x] metrics.schema.json
- [x] Baseline table template
- [x] Public dataset pointers or synthetic fixtures
- [x] Domain-shift honesty section



## File: `echovault/EVAL-HARNESS.md`

```markdown
# EVAL-HARNESS.md

License: MIT
Project: EchoVault
Task: Design open model eval harness recipes (no closed weights required)
Forged on GrokForge

## Three protocol tracks

1. **Self-supervised**: mask one feature dim, reconstruct (MSE).
2. **Supervised**: nearest-centroid on siteA, score macro-F1.
3. **Zero-shot**: cosine to hand prototypes (no training).

All tracks run on synthetic 4-D fixtures. No closed weights. No net.

## Domain-shift honesty

siteA = train / in-distribution. siteB adds a high-band shift that mimics
a different recorder or habitat. Report ID and OOD side by side. A model
that only wins on siteA is not done.

## Baseline table template

| Track | Split | Metric | Value | n | Domain shift |
| --- | --- | --- | --- | --- | --- |
| ssl | pooled | mse |  |  | no |
| supervised | id | macro_f1 |  |  | no |
| supervised | ood | macro_f1 |  |  | yes |
| zeroshot | id | acc |  |  | no |
| zeroshot | ood | acc |  |  | yes |

Fill from `echovault.eval_harness.run_tracks()`.

## Public dataset pointers (optional later)

Xeno-canto, iNaturalist sounds, Google iNat, BirdCLEF (rules apply).
This leaf does not bundle them. Synthetic fixtures keep CI offline.

## metrics.schema.json

See `schemas/metrics.schema.json`.

## Dual-use refuse

Eval is for archive models. Do not claim species IDs as facts.

## Sources

Prototype / centroid classifiers are textbook. Fixtures original.

## Footer

MIT. Forged on GrokForge. No secrets / PII / private paths.
```


## File: `echovault/schemas/metrics.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://grokforge.app/schemas/echovault/metrics.v0.json",
  "title": "EchoVault eval metrics row",
  "type": "object",
  "required": ["track", "split", "metric", "value", "n", "domain_shift"],
  "properties": {
    "track": { "enum": ["ssl", "supervised", "zeroshot"] },
    "split": { "enum": ["id", "ood", "pooled"] },
    "metric": { "type": "string" },
    "value": { "type": "number" },
    "n": { "type": "integer" },
    "domain_shift": { "type": "boolean" },
    "notes": { "type": "string" }
  }
}
```


## File: `echovault/echovault/eval_harness.py`

```python
# SPDX-License-Identifier: MIT
# Copyright 2026 Pitchfork-and-Torch. Forged on GrokForge.
"""Three-track bioacoustic eval on synthetic fixtures. No closed weights."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence
import math
import random
import statistics


@dataclass(frozen=True)
class Clip:
    site: str
    label: str
    vec: tuple[float, ...]


def _synth(seed: int = 0) -> list[Clip]:
    rng = random.Random(seed)
    labels = ("bird", "frog", "insect", "anthro")
    sites = ("siteA", "siteB")
    out: list[Clip] = []
    proto = {
        "bird": (1.0, 0.2, 0.1, 0.0),
        "frog": (0.2, 1.0, 0.2, 0.0),
        "insect": (0.1, 0.2, 1.0, 0.1),
        "anthro": (0.0, 0.1, 0.2, 1.0),
    }
    for site in sites:
        shift = 0.0 if site == "siteA" else 0.35
        for lab in labels:
            for _ in range(8):
                base = proto[lab]
                vec = tuple(max(0.0, b + rng.uniform(-0.1, 0.1) + (shift if i == 3 else 0)) for i, b in enumerate(base))
                out.append(Clip(site, lab, vec))
    return out


def _cos(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def supervised_f1(train: list[Clip], test: list[Clip]) -> dict[str, float]:
    """Nearest-centroid classifier, macro-F1."""
    cents: dict[str, list[float]] = {}
    counts: dict[str, int] = {}
    dim = len(train[0].vec)
    for c in train:
        counts[c.label] = counts.get(c.label, 0) + 1
        acc = cents.setdefault(c.label, [0.0] * dim)
        for i, v in enumerate(c.vec):
            acc[i] += v
    for lab, acc in cents.items():
        n = counts[lab]
        cents[lab] = [x / n for x in acc]
    tp = {k: 0 for k in counts}
    fp = {k: 0 for k in counts}
    fn = {k: 0 for k in counts}
    for c in test:
        pred = max(cents, key=lambda lab: _cos(c.vec, cents[lab]))
        if pred == c.label:
            tp[c.label] += 1
        else:
            fp[pred] += 1
            fn[c.label] += 1
    f1s = []
    for lab in counts:
        prec = tp[lab] / max(1, tp[lab] + fp[lab])
        rec = tp[lab] / max(1, tp[lab] + fn[lab])
        f1s.append(0.0 if prec + rec == 0 else 2 * prec * rec / (prec + rec))
    return {"macro_f1": statistics.mean(f1s), "n_test": float(len(test))}


def ssl_recon(clips: list[Clip], mask_idx: int = 0) -> dict[str, float]:
    """Self-supervised toy: predict masked dim from others via mean prototype."""
    errs = []
    for c in clips:
        others = [x for i, x in enumerate(c.vec) if i != mask_idx]
        pred = statistics.mean(others)
        errs.append((pred - c.vec[mask_idx]) ** 2)
    return {"mse": statistics.mean(errs)}


def zeroshot(clips: list[Clip]) -> dict[str, float]:
    """Zero-shot: compare to hand prototypes (same as generator means)."""
    proto = {
        "bird": (1.0, 0.2, 0.1, 0.0),
        "frog": (0.2, 1.0, 0.2, 0.0),
        "insect": (0.1, 0.2, 1.0, 0.1),
        "anthro": (0.0, 0.1, 0.2, 1.0),
    }
    ok = 0
    for c in clips:
        pred = max(proto, key=lambda lab: _cos(c.vec, proto[lab]))
        ok += int(pred == c.label)
    return {"acc": ok / max(1, len(clips))}


def run_tracks(seed: int = 0) -> dict[str, dict[str, float]]:
    clips = _synth(seed)
    train = [c for c in clips if c.site == "siteA"]
    test_id = [c for c in clips if c.site == "siteA"]
    test_ood = [c for c in clips if c.site == "siteB"]
    return {
        "ssl": ssl_recon(clips),
        "supervised_id": supervised_f1(train, test_id),
        "supervised_ood": supervised_f1(train, test_ood),
        "zeroshot_id": zeroshot(test_id),
        "zeroshot_ood": zeroshot(test_ood),
    }
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
