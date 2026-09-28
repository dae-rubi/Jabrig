from __future__ import annotations

from typing import Any


class BrowserBridge:
    """API bridge for authenticated browser control endpoints."""

    def validate_request(self, payload: dict[str, Any], auth_token: str | None) -> dict[str, bool]:
        authorized = auth_token is not None and bool(auth_token.strip())
        return {"authorized": authorized}
