from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional


class TagService:
    def __init__(self, db: Session):
        from .repository import TagRepository
        self.repo = TagRepository(db)

    def create_tag(self, name: str):
        existing_tag = self.repo.get_by_name(name)
        if existing_tag:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag with this name already exists"
            )
        return self.repo.create(name=name)

    def get_tag(self, tag_id: int):
        tag = self.repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return tag

    def get_tag_by_name(self, name: str):
        tag = self.repo.get_by_name(name)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return tag

    def get_all_tags(self, skip: int = 0, limit: int = 100):
        tags = self.repo.get_all(skip=skip, limit=limit)
        total = self.repo.count()
        return {"tags": tags, "total": total}

    def update_tag(self, tag_id: int, name: Optional[str] = None):
        tag = self.repo.get_by_id(tag_id)
        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )

        if name and name != tag.name:
            existing_tag = self.repo.get_by_name(name)
            if existing_tag:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tag with this name already exists"
                )

        return self.repo.update(tag_id=tag_id, name=name)

    def delete_tag(self, tag_id: int):
        if not self.repo.delete(tag_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found"
            )
        return {"message": "Tag deleted successfully"}
