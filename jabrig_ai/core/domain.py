from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class Event(BaseModel):
    name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data: dict[str, Any] = Field(default_factory=dict)
    trace_id: str | None = None
    task_id: str | None = None
    user_id: str | None = None


class AgentTask(BaseModel):
    id: str
    user_input: str
    mode: str = "assistant"
    context: dict[str, Any] = Field(default_factory=dict)
    capabilities: list[str] = Field(default_factory=list)
    risk_level: Literal["low", "medium", "high", "critical"] = "low"
    require_confirmation: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentPlan(BaseModel):
    id: str
    task_id: str
    goal: str
    steps: list["PlanStep"] = Field(default_factory=list)
    status: str = "pending"


class PlanStep(BaseModel):
    id: str
    description: str
    capabilities: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    risk: Literal["low", "medium", "high", "critical"] = "low"
    retry_policy: dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    capability: str | None = None


class ToolResult(BaseModel):
    id: str
    call_id: str
    status: Literal["success", "failed", "partial"] = "success"
    output: Any = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    task_id: str
    status: Literal["success", "failed", "partial"] = "success"
    summary: str
    artifacts: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Capability(BaseModel):
    name: str
    type: str
    description: str
    risk: Literal["low", "medium", "high", "critical"] = "low"
    permissions: list[str] = Field(default_factory=list)
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    provider: str | None = None
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class Skill(BaseModel):
    name: str
    description: str = ""
    risk: Literal["low", "medium", "high", "critical"] = "low"
    requires: list[str] = Field(default_factory=list)
    version: str = "1.0.0"
    enabled: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class Plugin(BaseModel):
    name: str
    type: str = "integration"
    manifest: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    permissions: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    enabled: bool = True


class MemoryItem(BaseModel):
    id: str
    namespace: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    ttl_seconds: int | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RoutingDecision(BaseModel):
    selected_capability: str
    selected_agent: str
    selected_skill: str | None = None
    selected_model: str | None = None
    reason: str
    risk: Literal["low", "medium", "high", "critical"] = "low"
    required_permissions: list[str] = Field(default_factory=list)
    fallbacks: list[str] = Field(default_factory=list)


class PermissionRequest(BaseModel):
    id: str
    action: str
    reason: str
    risk: Literal["low", "medium", "high", "critical"] = "low"
    status: Literal["pending", "granted", "denied"] = "pending"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConfirmationRequest(BaseModel):
    id: str
    message: str
    action: str
    status: Literal["pending", "approved", "rejected"] = "pending"


class ExecutionContext(BaseModel):
    task_id: str
    session_id: str | None = None
    user_id: str | None = None
    environment: str = "development"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ModelRequest(BaseModel):
    messages: list[dict[str, str]] = Field(default_factory=list)
    model: str | None = None
    provider: str | None = None
    system_prompt: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    stream: bool = False
    stream_response: bool = False
    tools: list[dict[str, Any]] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ModelResponse(BaseModel):
    content: str = ""
    provider: str | None = None
    model: str | None = None
    usage: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    is_streaming: bool = False
    finish_reason: str | None = None
