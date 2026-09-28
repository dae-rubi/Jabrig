from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from typing import Any

from jabrig_ai.core.domain import ModelRequest, ModelResponse
from jabrig_ai.providers.registry import ProviderRegistry


class ModelGateway:
    """Model gateway with provider selection, retry, timeout, and fallback."""

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        self.registry = registry or ProviderRegistry()
        self.fallback_order = list(self.registry.fallback_order)

    async def _invoke_provider(self, provider_name: str, request: ModelRequest) -> ModelResponse:
        provider = self.registry.get_provider(provider_name)
        if provider is None:
            raise ValueError(f"Unknown provider: {provider_name}")

        timeout_seconds = float((request.metadata or {}).get("timeout", 30))
        retries = int((request.metadata or {}).get("retries", 1))

        last_error: Exception | None = None
        for attempt in range(max(1, retries + 1)):
            try:
                response = await asyncio.wait_for(provider.generate(request), timeout=timeout_seconds)
                if response.model is None:
                    response.model = request.model or getattr(provider, "default_model", None)
                if response.provider is None:
                    response.provider = provider_name
                return response
            except Exception as exc:  # pragma: no cover - exercised via fallback path
                last_error = exc
                if attempt < retries:
                    continue
                raise

        raise last_error or RuntimeError(f"Provider {provider_name} failed")

    async def generate(self, request: ModelRequest) -> ModelResponse:
        preferred = request.provider or self.registry.default_provider_name
        if request.provider and self.registry.get_provider(request.provider) is None:
            raise ValueError(f"Unknown provider: {request.provider}")

        custom_chain = list(self.fallback_order)
        if custom_chain:
            if preferred in custom_chain:
                chain = [preferred] + [item for item in custom_chain if item != preferred]
            else:
                chain = [preferred] + [item for item in custom_chain if item != preferred]
        else:
            chain = self.registry.get_fallback_chain(preferred)

        last_error: Exception | None = None
        for provider_name in chain:
            try:
                return await self._invoke_provider(provider_name, request)
            except Exception as exc:
                last_error = exc
                continue

        if last_error is not None:
            raise last_error
        raise ValueError(f"No valid provider available for request: {request}")

    def list_providers(self) -> list[str]:
        return list(self.registry.providers.keys())

    def get_provider(self, name: str) -> Any:
        return self.registry.get_provider(name)
