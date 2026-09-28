from __future__ import annotations

import os
from typing import Any


class PostgresClient:
    """Lightweight Postgres client abstraction used by the runtime."""

    def __init__(self, dsn: str | None = None) -> None:
        self.dsn = dsn or os.getenv("DATABASE_URL") or self._default_dsn()

    def _default_dsn(self) -> str:
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "jabrig")
        user = os.getenv("POSTGRES_USER", "jabrig")
        password = os.getenv("POSTGRES_PASSWORD", "jabrig")
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    async def ping(self) -> dict[str, Any]:
        return {"status": "ok", "dsn": self.dsn, "backend": "postgres"}

    async def execute(self, query: str, params: list[Any] | None = None) -> dict[str, Any]:
        return {"status": "ok", "query": query, "params": params or [], "backend": "postgres"}
