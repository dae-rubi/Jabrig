from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from jabrig_ai.storage.database import DatabaseAdapter

app = FastAPI(title="JABRIG API", version="0.1.0")

VALID_API_KEYS = {os.getenv("JABRIG_API_KEY", "test-key")}


def get_db() -> DatabaseAdapter:
    return DatabaseAdapter(db_path=os.getenv("JABRIG_DB_PATH") or "jabrig.sqlite3")


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

    user_input = str(payload.get("user_input") or payload.get("prompt") or "")
    task_id = f"task-{abs(hash(user_input + os.urandom(4).hex()) % 1000000)}"
    db = get_db()
    await db.insert(
        "tasks",
        {
            "id": task_id,
            "status": "accepted",
            "user_input": user_input,
            "metadata": {"source": "api"},
            "name": "api-task",
        },
    )
    return {"task_id": task_id, "status": "accepted"}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok"}
