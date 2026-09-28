from __future__ import annotations

import os

import httpx

from jabrig_ai.core.domain import ModelRequest, ModelResponse


class NineRouterProvider:
    name = "9router"
    supports_tools = True
    supports_vision = False
    supports_streaming = True
    supports_reasoning = True
    context_window = 128000
    max_output_tokens = 4096
    default_model = os.getenv("NINEROUTER_DEFAULT_MODEL", "gpt-oss-20b")

    async def generate(self, request: ModelRequest) -> ModelResponse:
        api_key = os.getenv("NINEROUTER_API_KEY")
        if not api_key:
            return ModelResponse(
                content="",
                provider=self.name,
                model=request.model or self.default_model,
                metadata={"placeholder": True, "request": request.model_dump(exclude_none=True)},
            )

        model = request.model or self.default_model
        payload = {
            "model": model,
            "messages": request.messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        base_url = os.getenv("NINEROUTER_BASE_URL", "http://localhost:20128/v1")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{base_url.rstrip('/')}/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            )
            response.raise_for_status()
            body = response.json()

        message = body.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = body.get("usage", {})
        return ModelResponse(
            content=message,
            provider=self.name,
            model=model,
            usage=usage,
            metadata={"api": "9router", "request": request.model_dump(exclude_none=True)},
        )
