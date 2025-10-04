from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task_id: int, author_id: int, content: str):
        from .models import Comment
        comment = Comment(task_id=task_id, author_id=author_id, content=content)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_by_id(self, comment_id: int):
        from .models import Comment
        return self.db.execute(
            select(Comment).where(Comment.id == comment_id)
        ).scalar_one_or_none()

    def get_by_task(self, task_id: int, skip: int = 0, limit: int = 100):
        from .models import Comment
        return self.db.execute(
            select(Comment).where(Comment.task_id == task_id).offset(skip).limit(limit)
        ).scalars().all()

    def get_by_author(self, author_id: int, skip: int = 0, limit: int = 100):
        from .models import Comment
        return self.db.execute(
            select(Comment).where(Comment.author_id == author_id).offset(skip).limit(limit)
        ).scalars().all()

    def get_all(self, skip: int = 0, limit: int = 100):
        from .models import Comment
        return self.db.execute(
            select(Comment).offset(skip).limit(limit)
        ).scalars().all()

    def update(self, comment_id: int, content: Optional[str] = None):
        comment = self.get_by_id(comment_id)
        if not comment:
            return None
        if content is not None:
            comment.content = content
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment_id: int) -> bool:
        comment = self.get_by_id(comment_id)
        if not comment:
            return False
        self.db.delete(comment)
        self.db.commit()
        return True

    def count(self) -> int:
        from .models import Comment
        return self.db.query(Comment).count()
