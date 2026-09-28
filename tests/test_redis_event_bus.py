import pytest

from jabrig_ai.core.event_bus import EventBus


@pytest.mark.asyncio
async def test_event_bus_supports_redis_fallback(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")

    seen = {}

    async def handler(event):
        seen["value"] = event.data["value"]

    bus = EventBus(use_redis=True)
    await bus.subscribe("demo.event", handler)
    event = await bus.emit("demo.event", value="hello")

    assert event.data["value"] == "hello"
    assert seen["value"] == "hello"


@pytest.mark.asyncio
async def test_event_bus_uses_memory_path_when_redis_unavailable(monkeypatch):
    monkeypatch.delenv("REDIS_URL", raising=False)

    seen = {}

    async def handler(event):
        seen["value"] = event.data["value"]

    bus = EventBus(use_redis=True)
    await bus.subscribe("demo.event", handler)
    await bus.emit("demo.event", value="fallback")

    assert seen["value"] == "fallback"
