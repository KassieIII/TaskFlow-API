from datetime import datetime
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_archived: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime
    task_count: int = 0

    model_config = {"from_attributes": True}
