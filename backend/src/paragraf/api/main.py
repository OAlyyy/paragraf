"""HTTP API. For now only /health; /ask arrives in milestone 7."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from paragraf.db import connect

app = FastAPI(title="Paragraf", version="0.1.0")


@app.get("/health")
def health() -> JSONResponse:
    """Liveness + readiness: is the DB reachable and is pgvector installed?"""
    try:
        with connect(register_vector_type=False) as conn:
            row = conn.execute(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            ).fetchone()
    except Exception as exc:  # report, don't crash: health checks must always answer
        return JSONResponse({"status": "error", "db": f"unreachable: {type(exc).__name__}"}, 503)
    if row is None:
        return JSONResponse({"status": "error", "db": "ok", "pgvector": "missing"}, 503)
    return JSONResponse({"status": "ok", "db": "ok", "pgvector": row[0]})
