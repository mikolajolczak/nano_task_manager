from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.projects.schemas import ProjectBase
from app.tags.schemas import TagResponse
from app.users.schemas import UserBase


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"


class TaskCreate(TaskBase):
    project_id: int
    assignee_id: int
    tag_ids: list[int] = []


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    project_id: int | None = None
    status: str | None = None
    assignee_id: int | None = None
    tag_ids: list[int] | None = None


class TaskResponse(TaskBase):
    id: int
    project_id: int
    project: ProjectBase
    assignee_id: int | None
    assignee: UserBase
    created_at: datetime
    tags: list[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    tasks: list[TaskResponse]
    total: int
