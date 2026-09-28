import pytest

from jabrig_ai.core.domain import AgentTask, AgentPlan, PlanStep
from jabrig_ai.core.executor import Executor
from jabrig_ai.core.planner import Planner
from jabrig_ai.core.policy import PolicyEngine
from jabrig_ai.core.verifier import Verifier


@pytest.mark.asyncio
async def test_planner_creates_steps_for_research_task():
    planner = Planner()
    task = AgentTask(
        id="task-plan-1",
        user_input="Research laptops and compare them",
        context={"goal": "research"},
        capabilities=["browser.search", "research.search", "filesystem.write"],
    )

    plan = await planner.create(task, routing={"selected_capability": "research.search"}, context={})

    assert isinstance(plan, AgentPlan)
    assert plan.steps
    assert any(step.description.lower().startswith("search") or "search" in step.description.lower() for step in plan.steps)


@pytest.mark.asyncio
async def test_policy_engine_restricts_destructive_actions():
    engine = PolicyEngine()
    request = {
        "tool": "filesystem.delete",
        "risk": "high",
        "requested_permission": False,
        "autonomy_level": "assistant",
    }

    allowed = await engine.check(request)
    assert allowed is False


@pytest.mark.asyncio
async def test_executor_runs_steps_and_marks_completed():
    executor = Executor()

    async def fake_step(step: PlanStep):
        return {"status": "ok", "step_id": step.id}

    plan = AgentPlan(
        id="plan-1",
        task_id="task-1",
        goal="Demo execution",
        steps=[
            PlanStep(id="step-1", description="Perform action", capabilities=["browser.search"], dependencies=[]),
            PlanStep(id="step-2", description="Collect result", capabilities=["browser.extract"], dependencies=["step-1"]),
        ],
    )

    result = await executor.execute(plan, step_runner=fake_step)

    assert result["status"] == "success"
    assert result["completed_steps"] >= 1


@pytest.mark.asyncio
async def test_verifier_passes_valid_output():
    verifier = Verifier()
    result = {"status": "success", "content": "Laptop A vs. B"}

    verdict = await verifier.verify(task={"user_input": "Compare laptops"}, result=result)

    assert verdict["passed"] is True
    assert verdict["status"] == "passed"
