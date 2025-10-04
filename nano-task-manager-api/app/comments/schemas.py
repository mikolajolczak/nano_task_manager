from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    task_id: int
    author_id: int


class CommentUpdate(BaseModel):
    content: str | None = None


class CommentResponse(CommentBase):
    id: int
    task_id: int
    author_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentList(BaseModel):
    comments: list[CommentResponse]
    total: int
