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
            "status": payload.get("status", "accepted"),
            "user_input": user_input,
            "metadata": {"source": "api"},
            "name": payload.get("name", "api-task"),
        },
    )
    return {"task_id": task_id, "status": "accepted"}


@app.get("/v1/tasks")
async def list_tasks(x_api_key: str | None = Header(default=None, alias="x-api-key")) -> dict[str, Any]:
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="API key required")

    db = get_db()
    rows = await db.fetch("tasks", limit=100)
    return {"items": rows}


@app.get("/v1/tasks/{task_id}")
async def get_task(task_id: str, x_api_key: str | None = Header(default=None, alias="x-api-key")) -> dict[str, Any]:
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="API key required")

    db = get_db()
    rows = await db.fetch("tasks", filters={"id": task_id})
    if not rows:
        raise HTTPException(status_code=404, detail="Task not found")
    return rows[0]


@app.patch("/v1/tasks/{task_id}")
async def update_task(task_id: str, payload: dict[str, Any], x_api_key: str | None = Header(default=None, alias="x-api-key")) -> dict[str, Any]:
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="API key required")

    db = get_db()
    rows = await db.fetch("tasks", filters={"id": task_id})
    if not rows:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = {k: v for k, v in payload.items() if k in {"status", "user_input", "name", "metadata"}}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid updates supplied")

    await db.update("tasks", {"id": task_id}, updates)
    refreshed = await db.fetch("tasks", filters={"id": task_id})
    return refreshed[0]


@app.delete("/v1/tasks/{task_id}")
async def delete_task(task_id: str, x_api_key: str | None = Header(default=None, alias="x-api-key")) -> dict[str, Any]:
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="API key required")

    db = get_db()
    rows = await db.fetch("tasks", filters={"id": task_id})
    if not rows:
        raise HTTPException(status_code=404, detail="Task not found")

    with db._connect() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

    return {"deleted": True, "task_id": task_id}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok"}
