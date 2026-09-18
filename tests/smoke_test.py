# SPDX-License-Identifier: MIT
# Copyright 2026 Pitchfork-and-Torch. Forged on GrokForge.
"""Smoke test for the EchoVault v0.1.0 kit. Python 3.10+, stdlib only.

The kit ships its code inside fenced blocks in tasks/**/deliverable.md.
This script pulls those blocks out, loads them, and checks the claims the
deliverables make about themselves:

  - every ```json block in every deliverable parses
  - both JSON Schema files parse and declare the documented required keys
  - schema.examples() returns 3 records that pass validate_record
  - validate_record fails closed on the documented rails
  - eval_harness.run_tracks() returns all 5 tracks with finite metrics
  - Monitor fires at least 3 of the 4 anomaly classes injected by
    synthetic_stream() and never fires during warmup

Run from the repo root:

    python3 tests/smoke_test.py

Exit code 0 means every check passed.
"""

from __future__ import annotations

import json
import math
import re
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "tasks" / "01-master-goal-echovault-global-bioacoustic-archive-decoder"
SCHEMA_LEAF = TASKS / "03-ship-open-bioacoustic-metadata-schema-v0-json-schema" / "deliverable.md"
EVAL_LEAF = TASKS / "05-design-open-model-eval-harness-recipes-no-closed-weights-require" / "deliverable.md"
MONITOR_LEAF = TASKS / "06-ship-real-time-monitoring-architecture-anomaly-playbook" / "deliverable.md"

FENCE = re.compile(r"^```(\w+)\n(.*?)^```$", re.S | re.M)

_failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    if cond:
        print(f"ok   {msg}")
    else:
        print(f"FAIL {msg}")
        _failures.append(msg)


def fenced_blocks(path: Path, lang: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [body for tag, body in FENCE.findall(text) if tag == lang]


def load_module(name: str, source: str) -> types.ModuleType:
    mod = types.ModuleType(name)
    mod.__file__ = f"<embedded:{name}>"
    # dataclasses resolves string annotations through sys.modules[cls.__module__]
    sys.modules[name] = mod
    exec(compile(source, mod.__file__, "exec"), mod.__dict__)
    return mod


def test_all_json_blocks_parse() -> None:
    count = 0
    for leaf in sorted(TASKS.rglob("deliverable.md")):
        for i, body in enumerate(fenced_blocks(leaf, "json")):
            try:
                json.loads(body)
                count += 1
            except json.JSONDecodeError as exc:
                check(False, f"json block {i} in {leaf.parent.name} parses ({exc})")
    check(count >= 13, f"all {count} json blocks across deliverables parse")


def test_json_schemas() -> None:
    meta = json.loads(fenced_blocks(SCHEMA_LEAF, "json")[0])
    check(meta.get("type") == "object", "metadata schema is an object schema")
    required = set(meta.get("required", []))
    documented = {
        "record_id", "captured_at", "device", "location", "taxa",
        "behavior_tags", "quality", "license", "consent", "checksums",
    }
    check(required == documented, "metadata schema required keys match SCHEMA.md")
    loc = meta["properties"]["location"]["properties"]
    check(loc["geohash_precision"].get("maximum") == 5, "metadata schema caps geohash_precision at 5")
    check(loc["geohash_precision"].get("minimum") == 0, "metadata schema floors geohash_precision at 0")
    check(set(loc["policy"]["enum"]) == {"coarse", "delayed", "redacted"}, "metadata schema location.policy enum")

    metrics = json.loads(fenced_blocks(EVAL_LEAF, "json")[0])
    check(
        set(metrics.get("required", [])) == {"track", "split", "metric", "value", "n", "domain_shift"},
        "metrics schema required keys match EVAL-HARNESS.md table",
    )
    check(set(metrics["properties"]["track"]["enum"]) == {"ssl", "supervised", "zeroshot"}, "metrics schema track enum")


def test_schema_module() -> None:
    schema = load_module("echovault_schema", fenced_blocks(SCHEMA_LEAF, "python")[0])
    meta = json.loads(fenced_blocks(SCHEMA_LEAF, "json")[0])

    check(tuple(schema.REQUIRED) == tuple(meta["required"]), "schema.REQUIRED matches JSON Schema required list")

    examples = schema.examples()
    check(len(examples) == 3, "schema.examples() returns 3 records")
    policies = [r["location"]["policy"] for r in examples]
    check(policies == ["coarse", "delayed", "redacted"], "examples cover coarse, delayed, redacted")
    for rec in examples:
        errs = schema.validate_record(rec)
        check(errs == [], f"example {rec['record_id']} passes validate_record ({errs})")
        check(set(meta["required"]) <= set(rec), f"example {rec['record_id']} has every schema-required key")

    dumped = json.loads(schema.dumps_examples())
    check(dumped == examples, "dumps_examples() round-trips through json")

    base = examples[0]

    def mutate(**overrides):
        rec = json.loads(json.dumps(base))
        for path, value in overrides.items():
            parts = path.split(".")
            cur = rec
            for p in parts[:-1]:
                cur = cur[p]
            cur[parts[-1]] = value
        return rec

    def rejects(rec, needle: str, label: str) -> None:
        errs = schema.validate_record(rec)
        check(any(needle in e for e in errs), f"validator rejects {label} ({errs})")

    empty_errs = schema.validate_record({})
    check(len([e for e in empty_errs if e.startswith("missing ")]) == len(schema.REQUIRED), "empty record reports every missing key")

    rejects(mutate(**{"location.geohash_precision": 6}), "geohash_precision > 5", "geohash_precision 6 (habitat leak)")
    rejects(mutate(**{"location.geohash_precision": -1}), "geohash_precision must be >= 0", "negative geohash_precision")
    check(
        not any("geohash_precision" in e for e in schema.validate_record(mutate(**{"location.geohash_precision": 0, "location.geohash": ""}))),
        "precision 0 with empty geohash still passes",
    )
    rejects(mutate(**{"location.geohash": "dn6k9"}), "longer than declared precision", "geohash finer than declared precision")
    rejects(mutate(**{"location.geohash": "dn6a"}), "invalid geohash", "geohash with non-base32 char")
    rejects(mutate(**{"location.policy": "exact"}), "location.policy", "unknown location.policy")
    rejects(mutate(captured_at="2026-04-01T12:00:00+02:00"), "captured_at", "non-UTC timestamp")
    rejects(mutate(record_id="short"), "record_id too short", "short record_id")
    rejects(mutate(**{"checksums.sha256": "abc"}), "sha256", "malformed sha256")
    rejects(
        mutate(taxa=[{"rank": "species", "name": "Turdus merula", "confidence": 0.99, "method": "unverified_model"}]),
        "overconfident",
        "overconfident unverified model taxon",
    )
    rejects(mutate(taxa=[{"rank": "class", "confidence": 0.5, "method": "human"}]), "taxon missing name", "taxon without name")
    rejects(mutate(**{"consent.indigenous_flag": True, "consent.community_ok": False}), "indigenous_flag", "indigenous_flag without community_ok or embargo")
    embargo_ok = mutate(**{"consent.indigenous_flag": True, "consent.community_ok": False, "consent.embargo_until": "2027-01-01T00:00:00Z"})
    check(not any("indigenous_flag" in e for e in schema.validate_record(embargo_ok)), "indigenous_flag + embargo_until passes without community_ok")
    rejects(
        mutate(**{"consent.indigenous_flag": True, "consent.community_ok": False, "consent.embargo_until": "not-a-date"}),
        "embargo_until must be UTC ISO-8601",
        "indigenous_flag with non-ISO embargo_until",
    )
    rejects(
        mutate(**{"consent.embargo_until": "later"}),
        "embargo_until must be UTC ISO-8601",
        "free-text embargo_until even when community_ok",
    )
    rejects(
        mutate(**{"location.geohash_precision": 0, "location.geohash": "dn6kqqqqqq"}),
        "geohash longer",
        "precision 0 must still reject overlong geohash",
    )
    check(
        not any("geohash longer" in e for e in schema.validate_record(mutate(**{"location.geohash_precision": 4, "location.geohash": "dn6k"}))),
        "precision 4 accepts matching-length geohash",
    )
    rejects(
        mutate(**{"location.policy": "redacted", "location.geohash": "dn6k"}),
        "redacted location must not carry",
        "redacted policy with geohash (habitat leak)",
    )
    check(
        not any("redacted" in e for e in schema.validate_record(mutate(**{"location.policy": "redacted", "location.geohash": ""}))),
        "redacted with empty geohash passes",
    )
    rejects(mutate(quality={"clip_score": 0.5}), "snr_db", "quality without snr_db")


def test_eval_harness() -> None:
    harness = load_module("echovault_eval_harness", fenced_blocks(EVAL_LEAF, "python")[0])
    metrics = json.loads(fenced_blocks(EVAL_LEAF, "json")[0])
    out = harness.run_tracks()
    expected = {"ssl", "supervised_id", "supervised_ood", "zeroshot_id", "zeroshot_ood"}
    check(set(out) == expected, "run_tracks() returns all 5 tracks")
    for track, vals in out.items():
        for metric, value in vals.items():
            check(isinstance(value, float) and math.isfinite(value), f"{track}.{metric} is a finite float ({value})")
    check(0.0 <= out["supervised_id"]["macro_f1"] <= 1.0, "supervised_id macro_f1 in [0, 1]")
    check(0.0 <= out["zeroshot_ood"]["acc"] <= 1.0, "zeroshot_ood acc in [0, 1]")
    check(out["supervised_id"]["n_test"] == 32.0, "supervised_id scores 32 in-distribution clips")
    check(out["ssl"]["mse"] >= 0.0, "ssl mse is non-negative")

    # The baseline table maps each run_tracks() key onto a metrics.schema.json row.
    rows = [
        {"track": "ssl", "split": "pooled", "metric": "mse", "value": out["ssl"]["mse"], "n": 64, "domain_shift": False},
        {"track": "supervised", "split": "id", "metric": "macro_f1", "value": out["supervised_id"]["macro_f1"], "n": 32, "domain_shift": False},
        {"track": "supervised", "split": "ood", "metric": "macro_f1", "value": out["supervised_ood"]["macro_f1"], "n": 32, "domain_shift": True},
        {"track": "zeroshot", "split": "id", "metric": "acc", "value": out["zeroshot_id"]["acc"], "n": 32, "domain_shift": False},
        {"track": "zeroshot", "split": "ood", "metric": "acc", "value": out["zeroshot_ood"]["acc"], "n": 32, "domain_shift": True},
    ]
    for row in rows:
        check(set(metrics["required"]) <= set(row), f"baseline row {row['track']}/{row['split']} has metrics schema required keys")
        check(row["track"] in metrics["properties"]["track"]["enum"], f"baseline row {row['track']}/{row['split']} track in enum")
        check(row["split"] in metrics["properties"]["split"]["enum"], f"baseline row {row['track']}/{row['split']} split in enum")

    same = harness.run_tracks(seed=0)
    check(same == out, "run_tracks() is deterministic for a fixed seed")


def test_monitor() -> None:
    monitor = load_module("echovault_monitor", fenced_blocks(MONITOR_LEAF, "python")[0])
    check(len(monitor.ANOMALY_CLASSES) == 8, "anomaly catalog has 8 classes")
    stream = monitor.synthetic_stream()
    check(len(stream) == 80, "synthetic_stream() yields 80 windows")

    mon = monitor.Monitor()
    alerts = []
    for w in stream:
        alerts.extend(mon.push(w))
    fired = {a.cls for a in alerts}
    injected = {"anthrophony_spike", "biodiversity_proxy_drop", "silence_outage", "clock_jump"}
    check(len(fired & injected) == 4, f"monitor fires all 4 injected classes ({sorted(fired)})")
    check(fired <= set(monitor.ANOMALY_CLASSES), "every alert class is in the catalog")
    check("anthrophony_spike" in fired, "anthrophony_spike fires on the high-band energy jump")
    check("silence_outage" in fired, "silence_outage fires on the energy floor")
    check("clock_jump" in fired, "clock_jump fires on the timestamp gap")
    check("biodiversity_proxy_drop" in fired, "biodiversity_proxy_drop fires on entropy collapse")
    for a in alerts:
        check(isinstance(a.note, str) and a.note, f"alert {a.cls}@{a.t:g} carries a note")

    def silent(i: int) -> "monitor.Window":
        return monitor.Window(t=float(i), energy=0.0, low_band=0.0, high_band=0.0, entropy=1.0, clip_frac=0.0, clock_dt=1.0)

    # Warmup: hard-floor rules are suppressed until min_windows have been seen.
    mon_warm = monitor.Monitor(min_windows=8)
    warm_alerts = [a for i in range(1, 8) for a in mon_warm.push(silent(i))]
    check(warm_alerts == [], f"no alert fires during the first min_windows-1 windows ({len(warm_alerts)})")
    check(any(a.cls == "silence_outage" for a in mon_warm.push(silent(8))), "silence_outage fires on window min_windows")

    # Cooldown: the same class cannot fire on consecutive windows.
    mon_cool = monitor.Monitor(cooldown=5, min_windows=1)
    silence_hits = [a for i in range(1, 8) for a in mon_cool.push(silent(i)) if a.cls == "silence_outage"]
    check(len(silence_hits) == 2, f"cooldown of 5 allows silence_outage twice in 7 windows ({len(silence_hits)})")

    # Non-positive clock_dt must not poison the prior interval.
    mon_dt = monitor.Monitor(cooldown=0, min_windows=0)
    for i in range(10):
        mon_dt.push(monitor.Window(t=float(i), energy=1.0, low_band=0.5, high_band=0.5, entropy=1.0, clip_frac=0.0, clock_dt=1.0))
    mon_dt.push(monitor.Window(t=10.0, energy=1.0, low_band=0.5, high_band=0.5, entropy=1.0, clip_frac=0.0, clock_dt=-2.0))
    after = mon_dt.push(monitor.Window(t=11.0, energy=1.0, low_band=0.5, high_band=0.5, entropy=1.0, clip_frac=0.0, clock_dt=1.0))
    check(not any(a.cls == "clock_jump" for a in after), "non-positive clock_dt must not false-fire next clock_jump")
    check(mon_dt._last_dt == 1.0, "prior dt stays last positive interval after non-positive sample")


def main() -> int:
    test_all_json_blocks_parse()
    test_json_schemas()
    test_schema_module()
    test_eval_harness()
    test_monitor()
    print()
    if _failures:
        print(f"{len(_failures)} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
