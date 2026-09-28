import pytest

from jabrig_ai.providers.gateway import ModelGateway
from jabrig_ai.core.domain import ModelRequest


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
