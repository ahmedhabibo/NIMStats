#!/usr/bin/env python3
"""One-time schema migration: add benchmark_type column to existing history.db.

Safe to run multiple times — uses ALTER TABLE which fails gracefully if column exists.
Existing runs default to 'main' (their actual benchmark type).
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from db_utils import HISTORY_DB, init_schema


def main():
    if not HISTORY_DB.exists():
        print(f"Error: {HISTORY_DB} not found", file=sys.stderr)
        return 1

    conn = sqlite3.connect(str(HISTORY_DB))
    try:
        # Check current schema
        cols = [row[1] for row in conn.execute("PRAGMA table_info(runs)").fetchall()]
        if 'benchmark_type' in cols:
            print("OK benchmark_type column already exists — nothing to migrate")
            return 0

        print(f"Migrating {HISTORY_DB}...")
        print(f"  Existing columns: {cols}")

        # Add the column with default 'main' (existing runs are main chain)
        conn.execute("ALTER TABLE runs ADD COLUMN benchmark_type TEXT NOT NULL DEFAULT 'main'")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_type      ON runs(benchmark_type)")

        # Verify
        new_cols = [row[1] for row in conn.execute("PRAGMA table_info(runs)").fetchall()]
        print(f"  New columns: {new_cols}")

        row_count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        type_count = conn.execute("SELECT benchmark_type, COUNT(*) FROM runs GROUP BY benchmark_type").fetchall()
        conn.commit()

        print(f"OK Migration complete: {row_count} runs")
        for t, c in type_count:
            print(f"   {t}: {c}")

    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
