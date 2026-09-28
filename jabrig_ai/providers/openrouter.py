from __future__ import annotations

from jabrig_ai.core.domain import ModelRequest, ModelResponse


class OpenRouterProvider:
    name = "openrouter"
    supports_tools = True
    supports_vision = False
    supports_streaming = True
    supports_reasoning = True
    context_window = 128000
    max_output_tokens = 4096
    default_model = "openrouter/default"

    async def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            content="",
            provider=self.name,
            model=request.model or self.default_model,
            metadata={"placeholder": True, "request": request.model_dump(exclude_none=True)},
        )
