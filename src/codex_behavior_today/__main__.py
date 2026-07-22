from __future__ import annotations

import argparse
import json
import os
import statistics
from collections import Counter
from datetime import date
from pathlib import Path

from .metrics import jsd, status_for, weighted_drift
from .probes import PROBES, PROBE_BATTERY_VERSION
from .sampler import configured_oauth_cli, sample_probe
from .site import build_site
from .storage import connect


ROOT = Path(__file__).resolve().parents[2]
DAILY_DIR = ROOT / "data" / "daily"
RUNTIME_DB = ROOT / "runtime" / "behavior.sqlite3"


def load_days() -> list[dict]:
    return [json.loads(path.read_text()) for path in sorted(DAILY_DIR.glob("*.json"))]


def run_daily(target_per_cell: int) -> dict:
    run_date = date.today().isoformat()
    model = os.environ.get("CODEX_BEHAVIOR_MODEL", "gpt-5.6-sol")
    connection = connect(RUNTIME_DB)
    cells = {}
    for probe in PROBES:
        samples = sample_probe(
            probe,
            model=model,
            oauth_cli=configured_oauth_cli(),
            attempts=target_per_cell,
            connection=connection,
            run_date=run_date,
        )
        counts = Counter(sample["canonical_answer"] for sample in samples if sample["canonical_answer"])
        latencies = [sample["latency_ms"] for sample in samples]
        cells[probe.slug] = {
            "attempts": len(samples),
            "valid": sum(counts.values()),
            "invalid": len(samples) - sum(counts.values()),
            "counts": dict(sorted(counts.items())),
            "latency_ms": {"median": round(statistics.median(latencies), 2), "min": round(min(latencies), 2), "max": round(max(latencies), 2)},
        }
    connection.close()
    current = {
        "schema_version": 1,
        "date": run_date,
        "measurement": {"model": model, "transport": "chatgpt-codex-subscription-compatibility", "probe_battery": PROBE_BATTERY_VERSION, "request_protocol": "v1"},
        "cells": cells,
        "total_attempts": sum(cell["attempts"] for cell in cells.values()),
        "total_valid": sum(cell["valid"] for cell in cells.values()),
        "total_invalid": sum(cell["invalid"] for cell in cells.values()),
    }
    previous = load_days()
    if previous:
        previous_day_drift, _ = weighted_drift(current, [previous[-1]])
    else:
        previous_day_drift = None
    baseline_drift, cell_drift = weighted_drift(current, previous[-14:]) if previous else (None, {})
    status, threshold = status_for(current, previous)
    current["metrics"] = {"previous_day_jsd": previous_day_drift, "baseline_jsd": baseline_drift, "cell_baseline_jsd": cell_drift, "status": status, "threshold_99": threshold}
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    (DAILY_DIR / f"{run_date}.json").write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n")
    build_site(load_days(), ROOT / "site")
    return current


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor whether Codex behavior changed today.")
    subcommands = parser.add_subparsers(dest="command", required=True)
    run_parser = subcommands.add_parser("run", help="Collect a daily sample and build the static site.")
    run_parser.add_argument("--per-cell", type=int, default=20)
    subcommands.add_parser("build-site", help="Build the static site from public aggregate JSON.")
    args = parser.parse_args()
    if args.command == "run":
        print(json.dumps(run_daily(args.per_cell), ensure_ascii=False, indent=2))
        return 0
    if args.command == "build-site":
        build_site(load_days(), ROOT / "site")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
