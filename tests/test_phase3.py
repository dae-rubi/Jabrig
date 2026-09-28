import pytest

from jabrig_ai.core.domain import AgentTask, RoutingDecision
from jabrig_ai.routing.capability_registry import CapabilityRegistry
from jabrig_ai.routing.capability_router import CapabilityRouter
from jabrig_ai.routing.jev_adapter import JEVAdapter


@pytest.mark.asyncio
async def test_capability_registry_registers_and_finds_capabilities():
    registry = CapabilityRegistry()
    registry.register("browser.search", "tool", "Search the web", "low", ["browser.read"], {}, {}, "9router")
    capability = registry.get("browser.search")

    assert capability is not None
    assert capability.name == "browser.search"
    assert capability.enabled is True


@pytest.mark.asyncio
async def test_local_router_routes_search_tasks():
    router = CapabilityRouter()
    task = AgentTask(
        id="task-1",
        user_input="Search for laptop options and compare them",
        capabilities=["browser.search", "research.search"],
        context={"goal": "research"},
    )

    decision = await router.route(task, context={})

    assert decision.selected_capability.startswith("browser.") or decision.selected_capability.startswith("research.")
    assert decision.selected_agent in {"research", "browser"}
    assert decision.reason


@pytest.mark.asyncio
async def test_jev_adapter_falls_back_to_local_router_when_unavailable():
    adapter = JEVAdapter()
    task = AgentTask(
        id="task-2",
        user_input="Open a webpage and extract details",
        capabilities=["browser.open", "browser.extract"],
        context={"goal": "browser"},
    )

    decision = await adapter.route(task, context={})

    assert isinstance(decision, RoutingDecision)
    assert decision.selected_capability in {"browser.open", "browser.extract"}
    assert decision.selected_agent in {"browser", "research"}
