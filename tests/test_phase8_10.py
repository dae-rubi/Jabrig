import pytest

from jabrig_ai.autonomy.scheduler import Scheduler
from jabrig_ai.autonomy.self_improvement import SelfImprovementEngine
from jabrig_ai.dashboard.dashboard import Dashboard
from jabrig_ai.voice.pipeline import VoicePipeline


@pytest.mark.asyncio
async def test_voice_pipeline_is_optional_and_works_in_text_mode():
    pipeline = VoicePipeline(enabled=False)
    result = await pipeline.process("hello from text mode")
    assert result["status"] == "text-only"


@pytest.mark.asyncio
async def test_scheduler_runs_tasks():
    scheduler = Scheduler()
    run = []

    async def sample_task():
        run.append("done")

    await scheduler.schedule(sample_task, name="demo")
    await scheduler.run_all()
    assert "done" in run


@pytest.mark.asyncio
async def test_self_improvement_generates_candidate_skill():
    engine = SelfImprovementEngine(skill_auto_publish=False)
    candidate = await engine.analyze(
        {
            "task": "Generate weekly report",
            "success_count": 3,
            "result": {"status": "success"},
        }
    )
    assert candidate["skill_name"]


def test_dashboard_snapshot_has_expected_sections():
    dashboard = Dashboard()
    snapshot = dashboard.snapshot()
    for key in ["current_task", "active_tools", "permissions", "logs"]:
        assert key in snapshot
