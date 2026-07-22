from __future__ import annotations

import sqlite3
from pathlib import Path


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute(
        """CREATE TABLE IF NOT EXISTS samples (
        run_date TEXT NOT NULL,
        probe_slug TEXT NOT NULL,
        raw_response TEXT,
        canonical_answer TEXT,
        latency_ms REAL NOT NULL,
        error TEXT,
        model TEXT NOT NULL,
        created_at TEXT NOT NULL
        )"""
    )
    return connection


def insert_sample(connection: sqlite3.Connection, sample: dict) -> None:
    connection.execute(
        """INSERT INTO samples
        (run_date, probe_slug, raw_response, canonical_answer, latency_ms, error, model, created_at)
        VALUES (:run_date, :probe_slug, :raw_response, :canonical_answer, :latency_ms, :error, :model, :created_at)""",
        sample,
    )
    connection.commit()
