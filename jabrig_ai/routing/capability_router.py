from __future__ import annotations

from jabrig_ai.core.domain import AgentTask, RoutingDecision
from jabrig_ai.routing.capability_registry import CapabilityRegistry


class CapabilityRouter:
    """Local deterministic router used as a fallback and as the default router when JEV is unavailable."""

    def __init__(self, registry: CapabilityRegistry | None = None) -> None:
        self.registry = registry or CapabilityRegistry()

    async def route(self, task: AgentTask, context: dict | None = None) -> RoutingDecision:
        candidates = self.registry.match(task, context or {})
        if not candidates:
            selected_capability = "browser.search"
            selected_agent = "research"
            reason = "No direct match found; defaulting to browser research capability."
            risk = "low"
            permissions = ["browser.read"]
        else:
            best = candidates[0]
            selected_capability = best.name
            selected_agent = "browser" if selected_capability.startswith("browser.") else "research"
            reason = f"Matched capability {best.name} for task context."
            risk = best.risk
            permissions = best.permissions

        return RoutingDecision(
            selected_capability=selected_capability,
            selected_agent=selected_agent,
            selected_skill=None,
            selected_model=None,
            reason=reason,
            risk=risk,
            required_permissions=permissions,
            fallbacks=["browser.search", "research.search"],
        )
