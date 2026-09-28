from __future__ import annotations

import os

import pytest

from jabrig_ai.storage.database import DatabaseAdapter


@pytest.mark.asyncio
async def test_database_adapter_persists_across_instances(tmp_path):
    db_path = tmp_path / "jabrig.sqlite3"
    os.environ["JABRIG_DB_PATH"] = str(db_path)

    first = DatabaseAdapter()
    await first.insert("tasks", {"id": "task-1", "status": "queued", "user_input": "hello"})

    second = DatabaseAdapter()
    rows = await second.fetch("tasks")

    assert len(rows) == 1
    assert rows[0]["id"] == "task-1"
    assert rows[0]["status"] == "queued"


@pytest.mark.asyncio
async def test_database_adapter_updates_and_filters_records(tmp_path):
    db_path = tmp_path / "jabrig.sqlite3"
    os.environ["JABRIG_DB_PATH"] = str(db_path)

    db = DatabaseAdapter()
    await db.insert("memory_items", {"id": "m-1", "namespace": "notes", "content": "alpha"})
    await db.insert("memory_items", {"id": "m-2", "namespace": "notes", "content": "beta"})

    await db.update("memory_items", {"id": "m-1"}, {"content": "updated"})
    rows = await db.fetch("memory_items", filters={"namespace": "notes"})

    assert any(row["id"] == "m-1" and row["content"] == "updated" for row in rows)
    assert any(row["id"] == "m-2" for row in rows)
