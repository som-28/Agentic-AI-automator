"""Typed execution models shared by the agent and user interfaces."""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RECOVERING = "RECOVERING"
    SKIPPED = "SKIPPED"


class VerificationStatus(str, Enum):
    NOT_CHECKED = "NOT_CHECKED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    UNAVAILABLE = "UNAVAILABLE"


class ToolResult(BaseModel):
    success: bool
    data: Any = None
    summary: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    confidence: Optional[float] = None
    source: Optional[str] = None


class VerificationResult(BaseModel):
    verified: bool
    confidence: float = 0.0
    issues: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)


class PlanStep(BaseModel):
    id: str | int
    tool: str
    args: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str | int] = Field(default_factory=list)


class ExecutionPlan(BaseModel):
    input: str
    steps: List[PlanStep] = Field(default_factory=list)


def validate_plan(plan: dict, registry) -> ExecutionPlan:
    """Validate a planner result before it can reach the controller."""
    validated = ExecutionPlan.model_validate(plan)
    task_ids = [str(step.id) for step in validated.steps]
    if len(task_ids) != len(set(task_ids)):
        raise ValueError("Plan contains duplicate step IDs")

    known_ids = set(task_ids)
    for step in validated.steps:
        if not registry.get(step.tool):
            raise ValueError(f"Unknown tool in plan: {step.tool}")
        missing = [str(dep) for dep in step.dependencies if str(dep) not in known_ids]
        if missing:
            raise ValueError(
                f"Step {step.id} depends on unknown step IDs: {', '.join(missing)}"
            )
    return validated


class TaskEvent(BaseModel):
    timestamp: datetime = Field(default_factory=utc_now)
    event_type: str
    task_id: Optional[str] = None
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskExecution(BaseModel):
    id: str
    goal: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    tool: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    input: Dict[str, Any] = Field(default_factory=dict)
    output: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    verification_status: VerificationStatus = VerificationStatus.NOT_CHECKED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    confidence: Optional[float] = None

    def start(self) -> None:
        self.status = TaskStatus.RUNNING
        self.started_at = utc_now()

    def complete(self, output: Any = None) -> None:
        self.status = TaskStatus.COMPLETED
        self.output = output
        self.completed_at = utc_now()

    def fail(self, error: str) -> None:
        self.status = TaskStatus.FAILED
        self.error = error
        self.completed_at = utc_now()
