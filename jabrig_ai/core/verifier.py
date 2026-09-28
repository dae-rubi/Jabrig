from __future__ import annotations

from typing import Any


class Verifier:
    """Validates that task result objects contain the required evidence."""

    async def verify(self, task: dict[str, Any] | Any, result: Any) -> dict[str, Any]:
        if result is None:
            return {"passed": False, "status": "failed", "reason": "No result available."}

        if isinstance(result, dict):
            if result.get("status") == "success" and result.get("content"):
                return {"passed": True, "status": "passed", "result": result}
            if result.get("status") == "failed":
                return {"passed": False, "status": "failed", "result": result}

        if isinstance(result, str) and result.strip():
            return {"passed": True, "status": "passed", "result": result}

        return {"passed": False, "status": "partial", "reason": "Output is incomplete or malformed."}
