# Paragraf

**Ask a question about your rental situation in Germany, in English or German, and
get a short plain-language answer with exact citations to the German Civil Code
(BGB §§ 535–580a, *Mietrecht*).** If the law text doesn't contain the answer,
Paragraf says so.

> ⚠️ Paragraf gives general information, not legal advice. For your individual
> situation, contact a tenants' association (*Mieterverein*) or a lawyer.

🚧 Work in progress. Built milestone by milestone; see [docs/DECISIONS.md](docs/DECISIONS.md).

## Run locally

Requirements: Docker, [uv](https://docs.astral.sh/uv/), make.

```bash
cp .env.example .env
make install      # backend deps
make db-up        # Postgres + pgvector in Docker
make migrate      # create the schema
make test         # unit + integration tests
make api          # http://localhost:8000/health
```

Or everything in Docker: `docker compose up --build`.

## Repository layout

```
backend/            FastAPI app, ingestion, retrieval, generation (Python)
  src/paragraf/
  migrations/       numbered SQL migrations
  tests/
frontend/           Next.js chat UI (milestone 8)
data/               golden set and parsed corpus snapshots
docs/DECISIONS.md   one entry per design decision
```

## Data sources

Law texts from [gesetze-im-internet.de](https://www.gesetze-im-internet.de/),
published by the German Federal Ministry of Justice.
