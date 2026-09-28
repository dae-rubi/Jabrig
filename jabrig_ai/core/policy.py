from __future__ import annotations

from typing import Any


class PolicyEngine:
    """Security and permission gate for dangerous operations."""

    async def check(self, request: dict[str, Any]) -> bool:
        tool = str(request.get("tool", "")).lower()
        risk = str(request.get("risk", "low")).lower()
        requested_permission = bool(request.get("requested_permission", False))
        autonomy_level = str(request.get("autonomy_level", "assistant")).lower()

        if tool in {"filesystem.delete", "terminal.execute", "email.send", "financial.transaction"}:
            if autonomy_level == "assistant":
                return False
            if risk in {"high", "critical"}:
                return requested_permission
            return True

        if tool in {"browser.read", "browser.search", "research.search"}:
            return True

        if risk in {"high", "critical"} and not requested_permission:
            return False

        return True
