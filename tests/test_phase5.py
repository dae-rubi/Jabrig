import pytest

from jabrig_ai.core.domain import MemoryItem
from jabrig_ai.memory.base import MemoryStore, WorkingMemory, EpisodicMemory, SemanticMemory, ProceduralMemory
from jabrig_ai.memory.registry import MemoryRegistry
from jabrig_ai.agents.hermes import HermesAdapter
from jabrig_ai.skills.registry import SkillRegistry


@pytest.mark.asyncio
async def test_memory_store_roundtrip():
    store = MemoryStore()
    item = MemoryItem(id="m1", namespace="working", content="Session state")
    await store.store(item)
    result = await store.search("Session")
    assert result


@pytest.mark.asyncio
async def test_skill_registry_register_and_load():
    registry = SkillRegistry()
    registry.register("browser-search", "Search the web", risk="low", requires=["browser"])
    skill = registry.get("browser-search")
    assert skill is not None
    assert skill.name == "browser-search"


@pytest.mark.asyncio
async def test_hermes_adapter_handles_missing_service():
    adapter = HermesAdapter()
    result = await adapter.execute({"id": "task-1", "user_input": "hello"})
    assert result["status"] in {"degraded", "ok"}


@pytest.mark.asyncio
async def test_memory_registry_has_expected_stores():
    registry = MemoryRegistry()
    names = {store.name for store in registry.stores.values()}
    assert {"working", "episodic", "semantic", "procedural"}.issubset(names)
