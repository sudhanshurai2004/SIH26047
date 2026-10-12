"""Stage 2 FastAPI application shell.

Session and scoring core services are local Python modules in this stage; their
HTTP routes arrive with the Stage 3 vertical slice. The service makes no
outbound network calls.
"""

from fastapi import FastAPI

app = FastAPI(
    title="SIH26047 Offline Trainer API",
    version="0.2.0",
    description="Local-only training service. No telemetry or external service calls.",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str | bool]:
    """Report the local service readiness without exposing operational data."""
    return {"status": "ok", "stage": "2", "offline_only": True}
