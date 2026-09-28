from fastapi.testclient import TestClient

from jabrig_ai.core.app import app
from jabrig_ai.observability.health import collect_health_snapshot
from jabrig_ai.providers.gateway import ModelGateway
from jabrig_ai.providers.registry import ProviderRegistry


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_endpoint():
    client = TestClient(app)
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in {"healthy", "degraded"}


def test_collect_health_snapshot_reports_healthy_when_services_are_reachable(monkeypatch):
    monkeypatch.setenv("POSTGRES_HOST", "localhost")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")

    class DummySocket:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

        def close(self):
            pass

    def fake_create_connection(address, timeout=..., source_address=None):
        return DummySocket()

    monkeypatch.setattr("socket.create_connection", fake_create_connection)

    snapshot = collect_health_snapshot()
    assert snapshot["status"] == "healthy"


def test_model_gateway_has_provider_registry():
    gateway = ModelGateway()
    registry = gateway.registry
    assert isinstance(registry, ProviderRegistry)
    assert registry.providers


def test_provider_registry_has_expected_providers():
    registry = ProviderRegistry()
    names = {p.name for p in registry.providers.values()}
    assert {"openai", "9router", "openrouter"}.issubset(names)
