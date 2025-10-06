from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.users.schemas import UserBase


class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    owner_id: int


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    owner_id: int | None = None


class ProjectResponse(ProjectBase):
    id: int
    owner: UserBase
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectList(BaseModel):
    projects: list[ProjectResponse]
    total: int
