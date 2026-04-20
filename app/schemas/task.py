from datetime import datetime
from pydantic import BaseModel, Field

from app.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=300)
    description: str | None = None
    priority: TaskPriority | None = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskAssign(BaseModel):
    assignee_id: int | None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    project_id: int
    assignee_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListParams(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: int | None = None
    search: str | None = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)
