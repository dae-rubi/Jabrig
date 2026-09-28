from __future__ import annotations

from typing import Any

from jabrig_ai.security.redaction import redact_secret


class AuditLogger:
    """Security audit log that strips raw secrets before storing events."""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def record(self, **payload: Any) -> dict[str, Any]:
        sanitized = redact_secret(payload)
        self.events.append(sanitized)
        return sanitized
