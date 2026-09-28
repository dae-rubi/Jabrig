import pytest

from jabrig_ai.core.domain import ModelRequest, ModelResponse
from jabrig_ai.providers.gateway import ModelGateway
from jabrig_ai.providers.registry import ProviderRegistry


class FailingProvider:
    name = "failing"
    supports_tools = True
    supports_vision = False
    supports_streaming = True
    supports_reasoning = True
    context_window = 32000
    max_output_tokens = 2048

    async def generate(self, request: ModelRequest) -> ModelResponse:
        raise RuntimeError("provider failed")


class SuccessProvider:
    name = "success"
    supports_tools = True
    supports_vision = False
    supports_streaming = True
    supports_reasoning = True
    context_window = 32000
    max_output_tokens = 2048

    async def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="ok",
            provider=self.name,
            model=request.model or "success-model",
            metadata={"status": "success"},
        )


@pytest.mark.asyncio
async def test_gateway_falls_back_when_primary_provider_fails():
    registry = ProviderRegistry()
    registry.register("failing", FailingProvider())
    registry.register("success", SuccessProvider())

    gateway = ModelGateway(registry)
    gateway.fallback_order = ["failing", "success"]

    response = await gateway.generate(
        ModelRequest(
            messages=[{"role": "user", "content": "hello"}],
            provider="failing",
            model="fallback-model",
        )
    )

    assert response.content == "ok"
    assert response.provider == "success"


def test_provider_registry_has_capability_metadata():
    registry = ProviderRegistry()
    provider = registry.get_provider("openai")
    assert provider is not None
    assert provider.supports_tools is True
    assert provider.supports_streaming is True
    assert provider.context_window > 0


@pytest.mark.asyncio
async def test_model_gateway_respects_requested_provider_and_model():
    gateway = ModelGateway()
    response = await gateway.generate(
        ModelRequest(
            messages=[{"role": "user", "content": "test"}],
            provider="9router",
            model="custom-router-model",
        )
    )

    assert response.provider == "9router"
    assert response.model == "custom-router-model"


@pytest.mark.asyncio
async def test_openai_provider_and_compat_providers_are_implemented():
    from jabrig_ai.providers.openai import OpenAIProvider
    from jabrig_ai.providers.ninerouter import NineRouterProvider
    from jabrig_ai.providers.openrouter import OpenRouterProvider

    request = ModelRequest(messages=[{"role": "user", "content": "hello"}], model="test-model")

    response = await OpenAIProvider().generate(request)
    assert response.provider == "openai"
    assert response.model == "test-model"

    nine = await NineRouterProvider().generate(request)
    assert nine.provider == "9router"

    router = await OpenRouterProvider().generate(request)
    assert router.provider == "openrouter"
