from __future__ import annotations

from typing import Any


class TerminalTool:
    """Terminal executor with explicit guards and dangerous command denylist."""

    DANGEROUS_COMMANDS = (
        "rm -rf",
        "mkfs",
        "dd if=/dev/zero",
        "format",
        "sudo rm",
    )

    def __init__(self, allowed_cwd: str | None = None) -> None:
        self.allowed_cwd = allowed_cwd or "/tmp"

    async def execute(self, command: str, cwd: str | None = None) -> dict[str, Any]:
        normalized = command.strip()
        if any(block in normalized for block in self.DANGEROUS_COMMANDS):
            return {"status": "denied", "reason": "Dangerous command blocked by policy."}
        if cwd and cwd != self.allowed_cwd:
            return {"status": "denied", "reason": "Working directory outside allowed policy."}
        return {"status": "ok", "command": normalized, "stdout": "command completed"}
