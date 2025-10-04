from pydantic import BaseModel
from pydantic import ConfigDict


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = None


class TagResponse(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TagList(BaseModel):
    tags: list[TagResponse]
    total: int
