from __future__ import annotations

from typing import Any


class BrowserService:
    """Browser runtime facade for Playwright and Brahma-style automation.

    This keeps browser control behind a capability-based interface and allows the
    transport to switch from Playwright to a browser bridge later.
    """

    def __init__(self) -> None:
        self.capabilities = [
            "browser.open",
            "browser.search",
            "browser.click",
            "browser.type",
            "browser.scroll",
            "browser.extract",
            "browser.screenshot",
            "browser.tabs",
            "browser.close",
        ]

    async def open(self, url: str) -> dict[str, Any]:
        return {"status": "ok", "url": url}

    async def search(self, query: str) -> dict[str, Any]:
        return {"status": "ok", "query": query}

    async def click(self, selector: str) -> dict[str, Any]:
        return {"status": "ok", "selector": selector}

    async def type(self, selector: str, value: str) -> dict[str, Any]:
        return {"status": "ok", "selector": selector, "value": value}

    async def scroll(self, amount: int) -> dict[str, Any]:
        return {"status": "ok", "amount": amount}

    async def extract(self, selector: str | None = None) -> dict[str, Any]:
        return {"status": "ok", "selector": selector, "content": "example-content"}

    async def screenshot(self, path: str | None = None) -> dict[str, Any]:
        return {"status": "ok", "path": path or "browser-shot.png"}

    async def tabs(self) -> dict[str, Any]:
        return {"status": "ok", "tabs": []}

    async def close(self) -> dict[str, Any]:
        return {"status": "ok"}
