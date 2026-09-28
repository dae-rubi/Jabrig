from fastapi.testclient import TestClient

from jabrig_ai.core.app import app
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


def test_model_gateway_has_provider_registry():
    gateway = ModelGateway()
    registry = gateway.registry
    assert isinstance(registry, ProviderRegistry)
    assert registry.providers


def test_provider_registry_has_expected_providers():
    registry = ProviderRegistry()
    names = {p.name for p in registry.providers.values()}
    assert {"openai", "9router", "openrouter"}.issubset(names)
