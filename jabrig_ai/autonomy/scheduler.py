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

    async def run_one(self, name: str) -> Any:
        for task_name, task in self.tasks:
            if task_name == name:
                result = task()
                if hasattr(result, "__await__"):
                    return await result
                return result
        raise KeyError(f"Scheduled task not found: {name}")
