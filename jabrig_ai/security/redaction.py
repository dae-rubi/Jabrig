from __future__ import annotations

from typing import Any


def redact_secret(data: Any) -> Any:
    if isinstance(data, dict):
        redacted: dict[str, Any] = {}
        for key, value in data.items():
            if any(token in key.lower() for token in ["secret", "token", "password", "key", "credential"]):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = redact_secret(value)
        return redacted
    if isinstance(data, list):
        return [redact_secret(item) for item in data]
    return data
