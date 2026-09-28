from __future__ import annotations

from dataclasses import dataclass

from jabrig_ai.core.domain import Capability


@dataclass
class CapabilityRegistration:
    name: str
    capability: Capability


class CapabilityRegistry:
    """Registry for tools, plugins, skills, and agents."""

    def __init__(self) -> None:
        self.capabilities: dict[str, Capability] = {}
        self._seed_default_capabilities()

    def _seed_default_capabilities(self) -> None:
        defaults = [
            ("browser.search", "tool", "Search the web", "low", ["browser.read"], {}, {}, "9router"),
            ("browser.open", "tool", "Open a webpage", "low", ["browser.read"], {}, {}, "9router"),
            ("browser.click", "tool", "Click a UI element", "low", ["browser.read"], {}, {}, "9router"),
            ("browser.extract", "tool", "Extract content from a page", "low", ["browser.read"], {}, {}, "9router"),
            ("research.search", "tool", "Search research sources", "low", ["research.read"], {}, {}, "9router"),
            ("filesystem.read", "tool", "Read local files", "low", ["filesystem.read"], {}, {}, "9router"),
            ("filesystem.write", "tool", "Write local files", "low", ["filesystem.write"], {}, {}, "9router"),
            ("terminal.execute", "tool", "Execute sandboxed shell commands", "medium", ["terminal.execute"], {}, {}, "9router"),
        ]

        for name, type_, description, risk, permissions, input_schema, output_schema, provider in defaults:
            self.register(name, type_, description, risk, permissions, input_schema, output_schema, provider)

    def register(
        self,
        name: str,
        type_: str,
        description: str,
        risk: str,
        permissions: list[str],
        input_schema: dict,
        output_schema: dict,
        provider: str | None = None,
        enabled: bool = True,
        metadata: dict | None = None,
    ) -> Capability:
        capability = Capability(
            name=name,
            type=type_,
            description=description,
            risk=risk,
            permissions=permissions,
            input_schema=input_schema,
            output_schema=output_schema,
            provider=provider,
            enabled=enabled,
            metadata=metadata or {},
        )
        self.capabilities[name] = capability
        return capability

    def get(self, name: str) -> Capability | None:
        return self.capabilities.get(name)

    def list(self) -> list[Capability]:
        return list(self.capabilities.values())

    def match(self, task: object, context: dict | None = None) -> list[Capability]:
        context = context or {}
        goal_text = ""
        explicit_capabilities: list[Capability] = []
        if hasattr(task, "user_input"):
            goal_text = task.user_input.lower()
            explicit_names = getattr(task, "capabilities", []) or []
            for name in explicit_names:
                capability = self.capabilities.get(name)
                if capability and capability.enabled:
                    explicit_capabilities.append(capability)
        elif isinstance(task, str):
            goal_text = task.lower()

        matches: list[Capability] = []
        if explicit_capabilities:
            return explicit_capabilities

        for capability in self.capabilities.values():
            if not capability.enabled:
                continue
            if capability.name in ("browser.search", "browser.open", "browser.extract") and any(token in goal_text for token in ["search", "browse", "open", "website", "web", "browser"]):
                matches.append(capability)
            elif capability.name == "research.search" and any(token in goal_text for token in ["research", "compare", "analyze", "study"]):
                matches.append(capability)
            elif capability.name == "filesystem.write" and any(token in goal_text for token in ["save", "write", "file", "markdown", "output"]):
                matches.append(capability)
        return matches
