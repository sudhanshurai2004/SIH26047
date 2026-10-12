"""Smoke test for the local API shell used by the one-command dev workflow."""

from fastapi.testclient import TestClient

from core.api.app import app


def test_health_endpoint_reports_local_stage_one_service() -> None:
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "stage": "2", "offline_only": True}
