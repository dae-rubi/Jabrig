import pytest
from fastapi.testclient import TestClient

from jabrig_ai.api.app import app
from jabrig_ai.security.audit import AuditLogger
from jabrig_ai.security.redaction import redact_secret
from jabrig_ai.storage.database import DatabaseAdapter


def test_task_endpoint_requires_auth_header():
    client = TestClient(app)
    response = client.post("/v1/tasks", json={"user_input": "hello"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_task_endpoint_accepts_valid_key_and_returns_task_id(monkeypatch):
    monkeypatch.setenv("JABRIG_DB_PATH", "jabrig.sqlite3")

    client = TestClient(app)
    response = client.post(
        "/v1/tasks",
        json={"user_input": "hello"},
        headers={"x-api-key": "test-key"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert "task_id" in payload

    db = DatabaseAdapter("jabrig.sqlite3")
    rows = await db.fetch("tasks", filters={"id": payload["task_id"]})
    assert rows and rows[0]["user_input"] == "hello"


def test_secret_redaction_masks_sensitive_values():
    masked = redact_secret({"password": "abc123", "token": "secret-token"})
    assert masked["password"] != "abc123"
    assert masked["token"] != "secret-token"


def test_audit_logger_records_event_without_raw_secret():
    logger = AuditLogger()
    entry = logger.record(task_id="t-1", action="tool.execute", provider="openai", model="gpt-4o-mini", secret="super-secret")
    assert entry["task_id"] == "t-1"
    assert "super-secret" not in str(entry)
