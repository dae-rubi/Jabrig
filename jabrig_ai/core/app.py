from __future__ import annotations

from typing import Any

from fastapi import FastAPI

from jabrig_ai.core.event_bus import EventBus
from jabrig_ai.core.logging import get_logger
from jabrig_ai.observability.health import collect_health_snapshot
from jabrig_ai.providers.gateway import ModelGateway

logger = get_logger("jabrig.app")

app = FastAPI(title="JABRIG AI", version="0.1.0")
app.state.event_bus = EventBus()
app.state.model_gateway = ModelGateway()


@app.get("/health")
async def health() -> dict[str, Any]:
    logger.info("health.check", extra={"event": "health.check", "component": "api"})
    return {"status": "ok", "service": "jabrig-ai"}


@app.get("/ready")
async def ready() -> dict[str, Any]:
    gateway = app.state.model_gateway
    snapshot = collect_health_snapshot()
    status = "healthy" if gateway and snapshot["status"] == "healthy" else "degraded"
    return {
        "status": status,
        "service": "jabrig-ai",
        "components": {
            "core": "healthy",
            "model_gateway": "healthy" if gateway else "offline",
        },
        "checks": snapshot["checks"],
    }


@app.get("/version")
async def version() -> dict[str, Any]:
    return {"version": "0.1.0", "name": "JABRIG AI"}
