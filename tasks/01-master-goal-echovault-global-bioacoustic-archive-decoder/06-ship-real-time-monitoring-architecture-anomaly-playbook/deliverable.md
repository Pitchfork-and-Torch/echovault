# Deliverable: Ship real-time monitoring architecture + anomaly playbook

License: MIT
Project: EchoVault: Global Bioacoustic Archive & Decoder
Task ID: `cmsnzuuk5000b80soixjvxm5l`
Contributor: @SuddenlyJon
Forged on GrokForge

## Acceptance checklist

- [x] Architecture diagram (mermaid or ASCII)
- [x] Anomaly class catalog (6+; 8 shipped)
- [x] Alert policy + false-positive rails
- [x] Synthetic demo outline + runnable monitor
- [x] Open stack notes



## File: `echovault/MONITORING-ARCHITECTURE.md`

```markdown
# MONITORING-ARCHITECTURE.md + ANOMALY-PLAYBOOK.md

License: MIT
Project: EchoVault
Task: Ship real-time monitoring architecture + anomaly playbook
Forged on GrokForge

## Architecture (mermaid)

```mermaid
flowchart LR
  mic[Open mic / file] --> win[1s windows]
  win --> feat[energy / bands / entropy / clip / clock]
  feat --> ewma[EWMA + z-score]
  ewma --> rules[class rules + cooldown]
  rules --> alert[Alert record]
  alert --> human[Human review]
```

ASCII:

```
stream -> features -> EWMA/z -> rules -> cooldown -> alert -> human
```

Open stack: Python stdlib only in this leaf. Later: optional rustfft / webrtcvad.

## Anomaly class catalog (8)

1. biodiversity_proxy_drop - entropy collapse
2. anthrophony_spike - high-band energy z
3. silence_outage - energy floor
4. clip_saturation - ADC clips
5. clock_jump - timestamp gap
6. unknown_novel_cluster - joint outlier
7. sensor_flatline - identical bands
8. rain_like_broadband - flat high+low energy

## Alert policy + false-positive rails

- Warmup: ignore first `min_windows` (default 8)
- Cooldown: do not re-fire same class for N windows
- Hysteresis via EWMA (no raw one-sample triggers except hard floors)
- No species name in alerts
- No lat/lon in alerts
- Human review required before any public post

## Synthetic demo

`synthetic_stream()` injects spike @40, entropy drop @55, silence @65,
clock jump @70. `Monitor` should fire at least three of those classes.

## Dual-use refuse

Monitoring for conservation science and education. Not a civilian
surveillance or anti-protest acoustic product.

## Sources

EWMA / z-score are standard. Class list is original for this kit.

## Footer

MIT. Forged on GrokForge. No secrets / PII / private paths.
```


## File: `echovault/echovault/monitor.py`

```python
# SPDX-License-Identifier: MIT
# Copyright 2026 Pitchfork-and-Torch. Forged on GrokForge.
"""Streaming anomaly detector for synthetic soundscape features.

Features per window: energy, low_band, high_band, entropy, clip_frac, clock_dt.
Not a fielded wildlife product. No geolocation. No species ID.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import math
import random


ANOMALY_CLASSES = (
    "biodiversity_proxy_drop",
    "anthrophony_spike",
    "silence_outage",
    "clip_saturation",
    "clock_jump",
    "unknown_novel_cluster",
    "sensor_flatline",
    "rain_like_broadband",
)


@dataclass
class Window:
    t: float
    energy: float
    low_band: float
    high_band: float
    entropy: float
    clip_frac: float
    clock_dt: float


@dataclass
class Alert:
    cls: str
    t: float
    score: float
    note: str


class EwmaZ:
    def __init__(self, alpha: float = 0.08) -> None:
        self.alpha = alpha
        self.mean = 0.0
        self.var = 1.0
        self.n = 0

    def update(self, x: float) -> float:
        self.n += 1
        if self.n == 1:
            self.mean = x
            return 0.0
        prev = self.mean
        # Score against the previous mean/var, then fold x in. Updating first
        # dampens spikes (anthrophony at t=40 fell to ~2.2 vs threshold 3.0).
        sd = math.sqrt(max(1e-6, self.var))
        z = (x - prev) / sd
        self.mean = self.alpha * x + (1 - self.alpha) * self.mean
        self.var = self.alpha * (x - prev) ** 2 + (1 - self.alpha) * self.var
        return z


class Monitor:
    def __init__(self, cooldown: int = 5, z_thresh: float = 3.0, min_windows: int = 8) -> None:
        self.energy = EwmaZ()
        self.high = EwmaZ()
        self.entropy = EwmaZ()
        self.cooldown = cooldown
        self.z_thresh = z_thresh
        self.min_windows = min_windows
        self._cool = {c: 0 for c in ANOMALY_CLASSES}
        self._i = 0
        self._last_t = 0.0

    def push(self, w: Window) -> list[Alert]:
        self._i += 1
        for k in self._cool:
            if self._cool[k] > 0:
                self._cool[k] -= 1
        alerts: list[Alert] = []

        def fire(cls: str, score: float, note: str) -> None:
            if self._i < self.min_windows:
                return
            if self._cool[cls]:
                return
            alerts.append(Alert(cls, w.t, score, note))
            self._cool[cls] = self.cooldown

        ze = self.energy.update(w.energy)
        zh = self.high.update(w.high_band)
        zn = self.entropy.update(w.entropy)
        if w.energy < 0.02:
            fire("silence_outage", 1.0, "energy near floor")
        if w.clip_frac > 0.2:
            fire("clip_saturation", w.clip_frac, "adc clips")
        if w.clock_dt > 2.5 * max(1e-6, self._last_t and 1.0):
            fire("clock_jump", w.clock_dt, "timestamp gap")
        if w.energy == w.low_band == w.high_band and self._i > 1:
            fire("sensor_flatline", 1.0, "identical bands")
        if zh > self.z_thresh and w.high_band > w.low_band:
            fire("anthrophony_spike", zh, "high-band energy z")
        if zn < -self.z_thresh and w.energy > 0.05:
            fire("biodiversity_proxy_drop", -zn, "entropy collapse")
        if w.low_band > 0.6 and w.high_band > 0.6:
            fire("rain_like_broadband", (w.low_band + w.high_band) / 2, "flat spectrum")
        if abs(ze) > self.z_thresh and abs(zh) > self.z_thresh and abs(zn) > self.z_thresh:
            fire("unknown_novel_cluster", max(abs(ze), abs(zh), abs(zn)), "joint outlier")
        self._last_t = w.t
        return alerts


def synthetic_stream(n: int = 80, seed: int = 1) -> list[Window]:
    rng = random.Random(seed)
    out: list[Window] = []
    t = 0.0
    for i in range(n):
        t += 1.0
        energy = 0.3 + rng.uniform(-0.03, 0.03)
        low = 0.25 + rng.uniform(-0.03, 0.03)
        high = 0.2 + rng.uniform(-0.03, 0.03)
        ent = 1.4 + rng.uniform(-0.05, 0.05)
        clip = 0.0
        dt = 1.0
        if i == 40:
            high, energy = 0.95, 0.9
        if i == 55:
            ent, energy = 0.2, 0.4
        if i == 65:
            energy = 0.0
        if i == 70:
            dt = 8.0
            t += 7.0
        out.append(Window(t, energy, low, high, ent, clip, dt))
    return out
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
