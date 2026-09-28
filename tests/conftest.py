import pytest


@pytest.fixture(autouse=True)
def isolate_database_env(monkeypatch):
    monkeypatch.delenv("JABRIG_DB_PATH", raising=False)
    yield
    monkeypatch.delenv("JABRIG_DB_PATH", raising=False)
