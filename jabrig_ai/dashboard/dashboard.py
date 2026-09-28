from __future__ import annotations

from typing import Any


class Dashboard:
    """Minimal dashboard snapshot showing the core UI sections required by the spec."""

    def snapshot(self) -> dict[str, Any]:
        return {
            "current_task": "idle",
            "active_tools": [],
            "permissions": [],
            "logs": [],
            "model": "n/a",
            "agent": "n/a",
        }
