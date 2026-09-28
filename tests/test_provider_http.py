import pytest

from jabrig_ai.providers.gateway import ModelGateway
from jabrig_ai.core.domain import ModelRequest
from jabrig_ai.providers.openai import OpenAIProvider


@pytest.mark.asyncio
async def test_gateway_uses_provider_metadata_for_model_selection():
    gateway = ModelGateway()
    request = ModelRequest(messages=[{"role": "user", "content": "hello"}], provider="openai", model="gpt-4o-mini")

    response = await gateway.generate(request)
    assert response.provider == "openai"
    assert response.model == "gpt-4o-mini"


@pytest.mark.asyncio
async def test_gateway_handles_missing_provider_gracefully():
    gateway = ModelGateway()
    request = ModelRequest(messages=[{"role": "user", "content": "hello"}], provider="ghost-provider")

    with pytest.raises(ValueError):
        await gateway.generate(request)


@pytest.mark.asyncio
async def test_openai_provider_uses_http_api_when_api_key_is_present(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "choices": [{"message": {"content": "hello from openai"}}],
                "usage": {"total_tokens": 12},
            }

    class FakeClient:
        def __init__(self, *args, **kwargs):
            self.headers = kwargs.get("headers", {})

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url, json=None, headers=None):
            assert url.endswith("/chat/completions")
            assert headers["Authorization"] == "Bearer test-key"
            assert json["model"] == "gpt-4o-mini"
            return FakeResponse()

    monkeypatch.setattr("httpx.AsyncClient", FakeClient)

    response = await OpenAIProvider().generate(
        ModelRequest(messages=[{"role": "user", "content": "hello"}], model="gpt-4o-mini")
    )

    assert response.provider == "openai"
    assert response.model == "gpt-4o-mini"
    assert response.content == "hello from openai"
