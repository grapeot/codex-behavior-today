from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

from .normalize import canonicalize
from .probes import PROBES, Probe
from .storage import insert_sample


def sample_probe(
    probe: Probe,
    *,
    model: str,
    oauth_cli: str,
    attempts: int,
    connection,
    run_date: str,
) -> list[dict]:
    collected: list[dict] = []
    for _ in range(attempts):
        started = time.perf_counter()
        raw_response = None
        error = None
        try:
            completed = subprocess.run(
                [oauth_cli, "--json", "request", "--model", model, "--prompt", probe.prompt],
                capture_output=True,
                check=True,
                text=True,
                timeout=180,
            )
            payload = json.loads(completed.stdout)
            raw_response = str(payload["answer"])
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError, KeyError) as exc:
            error = str(exc)[:500]
        latency_ms = (time.perf_counter() - started) * 1000
        canonical_answer = canonicalize(probe.kind, raw_response) if raw_response else None
        sample = {
            "run_date": run_date,
            "probe_slug": probe.slug,
            "raw_response": raw_response,
            "canonical_answer": canonical_answer,
            "latency_ms": latency_ms,
            "error": error,
            "model": model,
            "created_at": datetime.now(UTC).isoformat(),
        }
        insert_sample(connection, sample)
        collected.append(sample)
    return collected


def configured_oauth_cli() -> str:
    return os.environ.get("CODEX_BEHAVIOR_OAUTH_CLI", "chatgpt-oauth")
