from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional


class CommentService:
    def __init__(self, db: Session):
        from .repository import CommentRepository
        self.repo = CommentRepository(db)
        self.db = db

    def create_comment(self, task_id: int, author_id: int, content: str):
        self._validate_task_exists(task_id)
        self._validate_user_exists(author_id)

        return self.repo.create(task_id=task_id, author_id=author_id, content=content)

    def get_comment(self, comment_id: int):
        comment = self.repo.get_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        return comment

    def get_comments_by_task(self, task_id: int, skip: int = 0, limit: int = 100):
        self._validate_task_exists(task_id)
        comments = self.repo.get_by_task(task_id=task_id, skip=skip, limit=limit)
        return {"comments": comments, "total": len(comments)}

    def get_comments_by_author(self, author_id: int, skip: int = 0, limit: int = 100):
        self._validate_user_exists(author_id)
        comments = self.repo.get_by_author(author_id=author_id, skip=skip, limit=limit)
        return {"comments": comments, "total": len(comments)}

    def get_all_comments(self, skip: int = 0, limit: int = 100):
        comments = self.repo.get_all(skip=skip, limit=limit)
        total = self.repo.count()
        return {"comments": comments, "total": total}

    def update_comment(self, comment_id: int, content: Optional[str] = None):
        comment = self.repo.update(comment_id=comment_id, content=content)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        return comment

    def delete_comment(self, comment_id: int):
        if not self.repo.delete(comment_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        return {"message": "Comment deleted successfully"}

    def _validate_task_exists(self, task_id: int):
        from ..tasks.repository import TaskRepository
        task_repo = TaskRepository(self.db)
        if not task_repo.get_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

    def _validate_user_exists(self, user_id: int):
        from ..users.repository import UserRepository
        user_repo = UserRepository(self.db)
        if not user_repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
