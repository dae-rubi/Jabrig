from __future__ import annotations

from jabrig_ai.core.domain import Skill


class SkillRegistry:
    def __init__(self) -> None:
        self.skills: dict[str, Skill] = {}

    def register(self, name: str, description: str, risk: str = "low", requires: list[str] | None = None, version: str = "1.0.0") -> Skill:
        skill = Skill(
            name=name,
            description=description,
            risk=risk,
            requires=requires or [],
            version=version,
            enabled=True,
        )
        self.skills[name] = skill
        return skill

    def get(self, name: str) -> Skill | None:
        return self.skills.get(name)

    def discover(self) -> list[Skill]:
        return list(self.skills.values())

    def enable(self, name: str) -> None:
        skill = self.skills.get(name)
        if skill:
            skill.enabled = True

    def disable(self, name: str) -> None:
        skill = self.skills.get(name)
        if skill:
            skill.enabled = False

    def validate(self, skill: Skill) -> bool:
        return bool(skill.name and skill.description)
