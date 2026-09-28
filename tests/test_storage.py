import pytest

from jabrig_ai.storage.database import DatabaseAdapter


@pytest.mark.asyncio
async def test_database_adapter_can_store_and_fetch_records():
    db = DatabaseAdapter()
    await db.insert("tasks", {"id": "t-1", "status": "queued"})
    rows = await db.fetch("tasks")
    assert rows[0]["id"] == "t-1"
