from __future__ import annotations

from typing import Any

from jabrig_ai.core.domain import MemoryItem


class MemoryStore:
    """Simple in-memory store for Phase 5."""

    def __init__(self) -> None:
        self.items: list[MemoryItem] = []

    async def search(self, query: str, namespace: str | None = None) -> list[MemoryItem]:
        q = query.lower()
        results = []
        for item in self.items:
            if namespace and item.namespace != namespace:
                continue
            if q in item.content.lower():
                results.append(item)
        return results

    async def store(self, item: MemoryItem) -> MemoryItem:
        self.items.append(item)
        return item

    async def delete(self, item_id: str) -> None:
        self.items = [item for item in self.items if item.id != item_id]

    async def summarize(self, namespace: str | None = None) -> dict[str, Any]:
        subset = [item for item in self.items if namespace is None or item.namespace == namespace]
        return {"count": len(subset), "namespace": namespace or "all"}


class WorkingMemory(MemoryStore):
    name = "working"


class EpisodicMemory(MemoryStore):
    name = "episodic"


class SemanticMemory(MemoryStore):
    name = "semantic"


class ProceduralMemory(MemoryStore):
    name = "procedural"
