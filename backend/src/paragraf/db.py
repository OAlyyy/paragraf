"""Postgres access. Plain psycopg 3 + SQL, no ORM.

Retrieval is the heart of this project and it is written in SQL (pgvector
operators, tsvector ranking, fusion). Keeping SQL visible instead of hiding it
behind an ORM makes those queries easy to read, explain and tune.
"""

from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from pgvector.psycopg import register_vector

from paragraf.config import get_settings


@contextmanager
def connect(register_vector_type: bool = True) -> Iterator[psycopg.Connection]:
    """Open a connection; commits on success, rolls back on exception."""
    with psycopg.connect(get_settings().database_url) as conn:
        if register_vector_type:
            register_vector(conn)
        yield conn
