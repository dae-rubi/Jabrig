from __future__ import annotations

from jabrig_ai.core.domain import AgentTask, RoutingDecision
from jabrig_ai.routing.capability_router import CapabilityRouter


class JEVAdapter:
    """Thin adapter boundary for JEV routing.

    If a JEV service is unavailable, the adapter transparently falls back to the
    deterministic local router. This keeps the core routing layer independent from
    any specific JEV implementation.
    """

    def __init__(self, router: CapabilityRouter | None = None) -> None:
        self.router = router or CapabilityRouter()
        self.available = False

    async def route(self, task: AgentTask, context: dict | None = None) -> RoutingDecision:
        if not self.available:
            return await self.router.route(task, context or {})

        # Placeholder for future JEV integration. The contract remains stable.
        return await self.router.route(task, context or {})
