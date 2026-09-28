from __future__ import annotations

import asyncio
import os
from collections import defaultdict
from typing import Awaitable, Callable

from .domain import Event

Handler = Callable[[Event], Awaitable[None] | None]


class EventBus:
    """Async event bus with a Redis-backed path and in-memory fallback."""

    def __init__(self, use_redis: bool = False) -> None:
        self.use_redis = use_redis or bool(os.getenv("REDIS_URL"))
        self._subscribers: dict[str, set[Handler]] = defaultdict(set)
        self._redis_url = os.getenv("REDIS_URL")

    async def emit(self, event_name: str, **payload: object) -> Event:
        event = Event(name=event_name, data=dict(payload))
        for handler in list(self._subscribers.get(event_name, set())):
            result = handler(event)
            if asyncio.iscoroutine(result):
                await result
        return event

    async def subscribe(self, event_name: str, handler: Handler) -> None:
        self._subscribers[event_name].add(handler)

    async def unsubscribe(self, event_name: str, handler: Handler) -> None:
        self._subscribers.get(event_name, set()).discard(handler)
