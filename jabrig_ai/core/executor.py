from __future__ import annotations

from typing import Any, Callable

from jabrig_ai.core.domain import AgentPlan, PlanStep


class Executor:
    """Executes plan steps sequentially and supports dependency ordering."""

    async def execute(self, plan: AgentPlan, step_runner: Callable[[PlanStep], Any] | None = None) -> dict[str, Any]:
        if step_runner is None:
            async def default_runner(step: PlanStep) -> dict[str, Any]:
                return {"status": "ok", "step_id": step.id, "description": step.description}

            step_runner = default_runner

        completed = []
        results: list[dict[str, Any]] = []
        ordered_steps = self._order_steps(plan.steps)

        for step in ordered_steps:
            step.status = "running"
            try:
                result = await step_runner(step)
                step.status = "completed"
                completed.append(step.id)
                results.append({"step_id": step.id, "result": result})
            except Exception as exc:  # pragma: no cover - failure path is handled by verification
                step.status = "failed"
                results.append({"step_id": step.id, "error": str(exc)})
                break

        return {
            "status": "success" if completed else "failed",
            "completed_steps": len(completed),
            "total_steps": len(ordered_steps),
            "results": results,
        }

    def _order_steps(self, steps: list[PlanStep]) -> list[PlanStep]:
        ordered: list[PlanStep] = []
        pending = {step.id: step for step in steps}
        while pending:
            ready = [step for step in pending.values() if all(dep in [s.id for s in ordered] for dep in step.dependencies)]
            if not ready:
                ready = list(pending.values())
            next_step = ready[0]
            ordered.append(next_step)
            pending.pop(next_step.id)
        return ordered
