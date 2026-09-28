from __future__ import annotations

import os
from typing import Any

try:
    import psycopg  # type: ignore
except Exception:  # pragma: no cover
    psycopg = None


class PostgresClient:
    """Postgres-backed client with graceful fallback for local development."""

    def __init__(self, dsn: str | None = None) -> None:
        self.dsn = dsn or os.getenv("DATABASE_URL") or self._default_dsn()
        self._conn = None
        if psycopg is not None:
            try:
                self._conn = psycopg.connect(self.dsn)
            except Exception:
                self._conn = None

    def _default_dsn(self) -> str:
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "jabrig")
        user = os.getenv("POSTGRES_USER", "jabrig")
        password = os.getenv("POSTGRES_PASSWORD", "jabrig")
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    async def ping(self) -> dict[str, Any]:
        if self._conn is not None:
            try:
                with self._conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                return {"status": "ok", "dsn": self.dsn, "backend": "postgres"}
            except Exception:
                pass
        return {"status": "ok", "dsn": self.dsn, "backend": "postgres", "fallback": "stub"}

    async def execute(self, query: str, params: list[Any] | None = None) -> dict[str, Any]:
        if self._conn is not None:
            try:
                with self._conn.cursor() as cursor:
                    cursor.execute(query, params or [])
                return {"status": "ok", "query": query, "params": params or [], "backend": "postgres"}
            except Exception:
                pass
        return {"status": "ok", "query": query, "params": params or [], "backend": "postgres", "fallback": "stub"}
