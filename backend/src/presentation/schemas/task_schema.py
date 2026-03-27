from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    is_done: bool | None = None


class TaskResponse(BaseModel):
    id: int | None
    title: str
    description: str | None
    is_done: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
