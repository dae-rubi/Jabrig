from __future__ import annotations

from jabrig_ai.memory.base import EpisodicMemory, ProceduralMemory, SemanticMemory, WorkingMemory


class MemoryRegistry:
    def __init__(self) -> None:
        self.stores = {
            "working": WorkingMemory(),
            "episodic": EpisodicMemory(),
            "semantic": SemanticMemory(),
            "procedural": ProceduralMemory(),
        }

    def get(self, name: str):
        return self.stores.get(name)
