from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db

from .services import TagService
from .schemas import TagCreate, TagResponse, TagList, TagUpdate

tag_router = APIRouter(prefix="/tags", tags=["Tags"])


@tag_router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
def create_tag(tag_data: TagCreate, db: Session = Depends(get_db)):
    service = TagService(db)
    return service.create_tag(name=tag_data.name)


@tag_router.get("/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    service = TagService(db)
    return service.get_tag(tag_id)


@tag_router.get("/", response_model=TagList)
def get_all_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = TagService(db)
    return service.get_all_tags(skip=skip, limit=limit)


@tag_router.patch("/{tag_id}", response_model=TagResponse)
def update_tag(tag_id: int, tag_data: TagUpdate, db: Session = Depends(get_db)):
    service = TagService(db)
    return service.update_tag(tag_id=tag_id, name=tag_data.name)


@tag_router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    service = TagService(db)
    service.delete_tag(tag_id)
    return None
