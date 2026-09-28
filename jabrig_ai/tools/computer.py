from __future__ import annotations

from typing import Any


class LinuxComputerAdapter:
    async def open_application(self, app: str) -> dict[str, Any]:
        return {"status": "ok", "application": app}

    async def close_application(self, app: str) -> dict[str, Any]:
        return {"status": "ok", "application": app}

    async def focus_window(self, title: str) -> dict[str, Any]:
        return {"status": "ok", "window": title}

    async def keyboard(self, keys: str) -> dict[str, Any]:
        return {"status": "ok", "keys": keys}

    async def mouse(self, x: int, y: int) -> dict[str, Any]:
        return {"status": "ok", "x": x, "y": y}

    async def screenshot(self) -> dict[str, Any]:
        return {"status": "ok", "path": "/tmp/screenshot.png"}

    async def clipboard(self, value: str | None = None) -> dict[str, Any]:
        return {"status": "ok", "value": value}

    async def screen_info(self) -> dict[str, Any]:
        return {"status": "ok", "platform": "linux"}


class ComputerAdapter:
    """Platform adapter registry for computer operations."""

    def __init__(self) -> None:
        self.platform_adapters = {
            "linux": LinuxComputerAdapter(),
        }

    async def open_application(self, app: str) -> dict[str, Any]:
        return await self.platform_adapters["linux"].open_application(app)

    async def close_application(self, app: str) -> dict[str, Any]:
        return await self.platform_adapters["linux"].close_application(app)

    async def focus_window(self, title: str) -> dict[str, Any]:
        return await self.platform_adapters["linux"].focus_window(title)
