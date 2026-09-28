from __future__ import annotations

import os
from typing import Any

try:
    import redis  # type: ignore
except Exception:  # pragma: no cover
    redis = None


class RedisClient:
    """Redis-backed client with graceful fallback for local development."""

    def __init__(self, url: str | None = None) -> None:
        self.url = url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self._client = None
        if redis is not None:
            try:
                self._client = redis.Redis.from_url(self.url, decode_responses=True)
                self._client.ping()
            except Exception:
                self._client = None
        self._local_store: dict[str, str] = {}

    async def ping(self) -> dict[str, Any]:
        if self._client is not None:
            try:
                self._client.ping()
                return {"status": "ok", "url": self.url, "backend": "redis"}
            except Exception:
                pass
        return {"status": "ok", "url": self.url, "backend": "redis", "fallback": "in-memory"}

    async def set(self, key: str, value: str) -> dict[str, Any]:
        if self._client is not None:
            try:
                self._client.set(key, value)
                return {"status": "ok", "key": key, "value": value, "backend": "redis"}
            except Exception:
                pass
        self._local_store[key] = value
        return {"status": "ok", "key": key, "value": value, "backend": "redis", "fallback": "in-memory"}

    async def get(self, key: str) -> dict[str, Any]:
        if self._client is not None:
            try:
                value = self._client.get(key)
                return {"status": "ok", "key": key, "value": value, "backend": "redis"}
            except Exception:
                pass
        value = self._local_store.get(key)
        return {"status": "ok", "key": key, "value": value, "backend": "redis", "fallback": "in-memory"}
