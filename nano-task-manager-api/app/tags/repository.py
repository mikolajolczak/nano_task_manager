from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str):
        from .models import Tag
        tag = Tag(name=name)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def get_by_id(self, tag_id: int):
        from .models import Tag
        return self.db.execute(
            select(Tag).where(Tag.id == tag_id)
        ).scalar_one_or_none()

    def get_by_name(self, name: str):
        from .models import Tag
        return self.db.execute(
            select(Tag).where(Tag.name == name)
        ).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100):
        from .models import Tag
        return self.db.execute(
            select(Tag).offset(skip).limit(limit)
        ).scalars().all()

    def get_by_ids(self, tag_ids: List[int]):
        from .models import Tag
        return self.db.execute(
            select(Tag).where(Tag.id.in_(tag_ids))
        ).scalars().all()

    def update(self, tag_id: int, name: Optional[str] = None):
        tag = self.get_by_id(tag_id)
        if not tag:
            return None
        if name is not None:
            tag.name = name
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def delete(self, tag_id: int) -> bool:
        tag = self.get_by_id(tag_id)
        if not tag:
            return False
        self.db.delete(tag)
        self.db.commit()
        return True

    def count(self) -> int:
        from .models import Tag
        return self.db.query(Tag).count()
