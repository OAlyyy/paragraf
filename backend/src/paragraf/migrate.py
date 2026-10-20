"""Minimal migration runner: applies backend/migrations/*.sql in order, once each.

Why not Alembic? Our schema is small and mostly hand-written SQL (vector
indexes, tsvector columns), which Alembic would only wrap. A numbered folder of
.sql files plus a table remembering what ran is enough and fully transparent.
"""

import logging
from pathlib import Path

from paragraf.db import connect

MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"
log = logging.getLogger(__name__)


def pending(applied: set[str]) -> list[Path]:
    return [p for p in sorted(MIGRATIONS_DIR.glob("*.sql")) if p.name not in applied]


def migrate() -> list[str]:
    # The vector type doesn't exist until the first migration creates the extension.
    with connect(register_vector_type=False) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            " name text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())"
        )
        applied = {r[0] for r in conn.execute("SELECT name FROM schema_migrations")}
        done = []
        for path in pending(applied):
            # Each file runs in its own transaction: all of it applies, or none.
            with conn.transaction():
                conn.execute(path.read_text())
                conn.execute("INSERT INTO schema_migrations (name) VALUES (%s)", (path.name,))
            log.info("applied %s", path.name)
            done.append(path.name)
        return done


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    applied = migrate()
    print(f"applied {len(applied)} migration(s): {applied}" if applied else "up to date")
