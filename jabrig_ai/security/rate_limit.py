from __future__ import annotations

import time


class RateLimiter:
    """Simple in-memory rate limiter for per-identity request throttling."""

    def __init__(self, limit: int = 10, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        window = self._requests.setdefault(key, [])
        window[:] = [ts for ts in window if now - ts < self.window_seconds]

        if len(window) >= self.limit:
            return False

        window.append(now)
        return True
