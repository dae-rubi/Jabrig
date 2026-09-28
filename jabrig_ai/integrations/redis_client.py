from __future__ import annotations

import os
from typing import Any


class RedisClient:
    """Lightweight Redis client abstraction used by the runtime."""

    def __init__(self, url: str | None = None) -> None:
        self.url = url or os.getenv("REDIS_URL", "redis://localhost:6379/0")

    async def ping(self) -> dict[str, Any]:
        return {"status": "ok", "url": self.url, "backend": "redis"}

    async def set(self, key: str, value: str) -> dict[str, Any]:
        return {"status": "ok", "key": key, "value": value, "backend": "redis"}

    async def get(self, key: str) -> dict[str, Any]:
        return {"status": "ok", "key": key, "value": None, "backend": "redis"}
