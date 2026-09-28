from __future__ import annotations

from typing import Any, Callable


class Scheduler:
    """Simple background scheduler for tasks."""

    def __init__(self) -> None:
        self.tasks: list[tuple[str, Callable[[], Any]]] = []

    async def schedule(self, task: Callable[[], Any], name: str = "task") -> None:
        self.tasks.append((name, task))

    async def run_all(self) -> list[Any]:
        results = []
        for _, task in self.tasks:
            result = task()
            if hasattr(result, "__await__"):
                result = await result
            results.append(result)
        return results
