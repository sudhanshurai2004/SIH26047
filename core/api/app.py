"""Stage 1 FastAPI application shell.

Only a health endpoint is exposed until session and scoring APIs arrive in later
stages. The service makes no outbound network calls.
"""

from fastapi import FastAPI

app = FastAPI(
    title="SIH26047 Offline Trainer API",
    version="0.1.0",
    description="Local-only training service. No telemetry or external service calls.",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str | bool]:
    """Report the local service readiness without exposing operational data."""
    return {"status": "ok", "stage": "1", "offline_only": True}
