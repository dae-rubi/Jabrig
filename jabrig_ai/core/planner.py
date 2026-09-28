from __future__ import annotations

from jabrig_ai.core.domain import AgentPlan, AgentTask, PlanStep


class Planner:
    """Creates a plan from a task using the selected routing decision."""

    async def create(self, task: AgentTask, routing: dict | None = None, context: dict | None = None) -> AgentPlan:
        routing = routing or {}
        task_goal = task.user_input
        steps = [
            PlanStep(
                id="step-1",
                description="Search for relevant information",
                capabilities=[routing.get("selected_capability") or "browser.search"],
                dependencies=[],
                status="pending",
                risk="low",
                retry_policy={"max_retries": 2},
            ),
            PlanStep(
                id="step-2",
                description="Collect and compare sources",
                capabilities=["research.search", "browser.extract"],
                dependencies=["step-1"],
                status="pending",
                risk="medium",
                retry_policy={"max_retries": 2},
            ),
            PlanStep(
                id="step-3",
                description="Write organized result",
                capabilities=["filesystem.write"],
                dependencies=["step-2"],
                status="pending",
                risk="low",
                retry_policy={"max_retries": 1},
            ),
        ]

        return AgentPlan(
            id=f"plan-{task.id}",
            task_id=task.id,
            goal=task_goal,
            steps=steps,
            status="pending",
        )
