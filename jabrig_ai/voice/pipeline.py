from __future__ import annotations

from typing import Any


class VoicePipeline:
    """Optional voice stack that gracefully degrades to text-only mode."""

    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    async def process(self, text: str) -> dict[str, Any]:
        if not self.enabled:
            return {"status": "text-only", "message": text}
        return {"status": "ok", "message": text}
