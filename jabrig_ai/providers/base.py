from __future__ import annotations

from typing import Protocol

from jabrig_ai.core.domain import ModelRequest, ModelResponse


class ModelProvider(Protocol):
    """Provider interface used by the model gateway."""

    name: str
    supports_tools: bool
    supports_vision: bool
    supports_streaming: bool
    supports_reasoning: bool
    context_window: int | None
    max_output_tokens: int | None

    async def generate(self, request: ModelRequest) -> ModelResponse:
        ...
