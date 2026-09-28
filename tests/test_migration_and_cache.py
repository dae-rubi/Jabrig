import pytest

from jabrig_ai.integrations.redis_client import RedisClient
from jabrig_ai.storage.database import DatabaseAdapter


@pytest.mark.asyncio
async def test_redis_cache_round_trip():
    client = RedisClient("redis://localhost:6379/0")
    await client.set("cache-key", "cached-value")
    result = await client.get("cache-key")

    assert result["key"] == "cache-key"
    assert result["backend"] == "redis"


@pytest.mark.asyncio
async def test_database_supports_migration_metadata():
    db = DatabaseAdapter()
    record = {"id": "migration-1", "name": "baseline", "status": "applied"}
    await db.insert("tasks", record)
    rows = await db.fetch("tasks", filters={"id": "migration-1"})

    assert rows[0]["status"] == "applied"
