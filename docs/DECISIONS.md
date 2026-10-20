# Design decisions

One short entry per decision: what we chose, what else we considered, and why.
Newest decisions are added at the bottom.

---

## D1. Postgres + pgvector as the only datastore

**Chosen:** one Postgres instance holds raw documents, parsed legal units,
chunks, embeddings (pgvector), the full-text index (tsvector) and query logs.

**Alternatives:** a dedicated vector DB (Qdrant, Weaviate, Pinecone) next to
Postgres; Elasticsearch/OpenSearch for keyword search.

**Why:** hybrid search needs vector and keyword results over the *same* rows.
In one database that is one SQL query with a join, not two systems kept in
sync. The corpus is small (~130 §§, hundreds of chunks), far below where a
specialised vector DB pays off. Postgres also runs anywhere (Docker, Supabase).

**Cost:** Postgres full-text ranking (`ts_rank`) is not true BM25. If keyword
quality turns out to matter, ParadeDB's `pg_search` adds real BM25 to Postgres.

## D2. Plain SQL + psycopg 3, no ORM; numbered .sql migrations, no Alembic

**Why:** the important queries (vector distance, tsvector ranking, rank fusion)
are SQL anyway. Keeping them visible makes them easy to explain and tune. A
20-line runner that applies `migrations/*.sql` once each, in order, inside a
transaction, is enough for a schema this size.

## D3. uv for Python dependencies

**Why:** one fast tool for virtualenv + lockfile (`uv.lock`), so local, CI and
Docker builds all install exactly the same versions. Alternative: pip +
requirements.txt (no real lockfile) or Poetry (slower, more ceremony).

## D4. Typed settings (pydantic-settings), secrets as `SecretStr`

**Why:** every config knob lives in `config.py`, is validated at startup
(e.g. an unknown `LLM_PROVIDER` fails immediately), and API keys never show up
in `repr()`, logs or tracebacks. Secrets only ever come from `.env` / the
environment; `.env.example` documents them without values.
