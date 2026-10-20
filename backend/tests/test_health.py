import pytest
from fastapi.testclient import TestClient

from paragraf.api.main import app
from paragraf.config import get_settings


@pytest.mark.integration
def test_health_reports_pgvector():
    response = TestClient(app).get("/health")
    assert response.status_code == 200, response.json()
    assert response.json()["pgvector"]


def test_health_returns_503_when_db_is_down(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://nobody:x@127.0.0.1:1/none")
    get_settings.cache_clear()
    try:
        response = TestClient(app).get("/health")
    finally:
        get_settings.cache_clear()
    assert response.status_code == 503
    assert response.json()["status"] == "error"
