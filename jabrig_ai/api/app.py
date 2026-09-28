from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="JABRIG API", version="0.1.0")

VALID_API_KEYS = {"test-key"}


@app.middleware("http")
async def require_api_key(request, call_next):
    if request.url.path.startswith("/health") or request.url.path.startswith("/ready"):
        return await call_next(request)
    if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
        return await call_next(request)
    api_key = request.headers.get("x-api-key")
    if api_key not in VALID_API_KEYS:
        return JSONResponse(status_code=401, content={"detail": "API key required"})
    return await call_next(request)


@app.post("/v1/tasks")
async def create_task(payload: dict[str, Any], x_api_key: str | None = Header(default=None, alias="x-api-key")) -> dict[str, Any]:
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="API key required")
    task_id = f"task-{abs(hash(payload.get('user_input', 'hello')) % 100000)}"
    return {"task_id": task_id, "status": "accepted"}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok"}
