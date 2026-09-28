from __future__ import annotations

from dataclasses import dataclass

from jabrig_ai.providers.openai import OpenAIProvider
from jabrig_ai.providers.ninerouter import NineRouterProvider
from jabrig_ai.providers.openrouter import OpenRouterProvider


@dataclass
class ProviderRegistration:
    name: str
    provider: object


class ProviderRegistry:
    """Registry of configured providers."""

    def __init__(self) -> None:
        self.providers: dict[str, object] = {
            "openai": OpenAIProvider(),
            "9router": NineRouterProvider(),
            "openrouter": OpenRouterProvider(),
        }
        self.fallback_order = ["9router", "openai", "openrouter"]
        self.metadata = {
            "openai": {"supports_tools": True, "supports_streaming": True, "context_window": 128000},
            "9router": {"supports_tools": True, "supports_streaming": True, "context_window": 128000},
            "openrouter": {"supports_tools": True, "supports_streaming": True, "context_window": 128000},
        }

    @property
    def default_provider_name(self) -> str:
        return "9router"

    def register(self, name: str, provider: object) -> None:
        self.providers[name] = provider

    def get_provider(self, name: str) -> object | None:
        if name is None:
            return self.providers.get(self.default_provider_name)
        return self.providers.get(name)

    def get_fallback_chain(self, preferred: str | None = None) -> list[str]:
        if preferred is None:
            return list(self.fallback_order)
        ordered = [preferred]
        for item in self.fallback_order:
            if item != preferred:
                ordered.append(item)
        return ordered
