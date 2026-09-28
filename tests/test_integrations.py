import pytest

from jabrig_ai.integrations import PostgresClient, RedisClient


@pytest.mark.asyncio
async def test_postgres_client_builds_connection_string_and_ping():
    client = PostgresClient()
    result = await client.ping()

    assert result["status"] == "ok"
    assert "postgres" in result["backend"]
    assert "postgresql://" in client.dsn


@pytest.mark.asyncio
async def test_redis_client_exposes_url_and_stub_operations():
    client = RedisClient("redis://redis:6379/0")
    ping = await client.ping()
    stored = await client.set("demo", "value")
    value = await client.get("demo")

    assert ping["status"] == "ok"
    assert stored["backend"] == "redis"
    assert value["backend"] == "redis"
