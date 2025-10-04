from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, project_id: int, description: Optional[str] = None,
               status: str = "todo", assignee_id: Optional[int] = None, tag_ids=None):
        if tag_ids is None:
            tag_ids = []
        from .models import Task
        from ..tags.models import Tag

        task = Task(
            title=title,
            project_id=project_id,
            description=description,
            status=status,
            assignee_id=assignee_id
        )

        if tag_ids:
            tags = self.db.execute(select(Tag).where(Tag.id.in_(tag_ids))).scalars().all()
            task.tags = tags

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int):
        from .models import Task
        return self.db.execute(
            select(Task).where(Task.id == task_id)
        ).scalar_one_or_none()

    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 100):
        from .models import Task
        return self.db.execute(
            select(Task).where(Task.project_id == project_id).offset(skip).limit(limit)
        ).scalars().all()

    def get_by_assignee(self, assignee_id: int, skip: int = 0, limit: int = 100):
        from .models import Task
        return self.db.execute(
            select(Task).where(Task.assignee_id == assignee_id).offset(skip).limit(limit)
        ).scalars().all()

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100):
        from .models import Task
        return self.db.execute(
            select(Task).where(Task.status == status).offset(skip).limit(limit)
        ).scalars().all()

    def get_all(self, skip: int = 0, limit: int = 100):
        from .models import Task
        return self.db.execute(
            select(Task).offset(skip).limit(limit)
        ).scalars().all()

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
               status: Optional[str] = None, assignee_id: Optional[int] = None,
               tag_ids: Optional[List[int]] = None):
        from ..tasks.models import Task
        from ..tags.models import Tag

        task = self.get_by_id(task_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if assignee_id is not None:
            task.assignee_id = assignee_id
        if tag_ids is not None:
            tags = self.db.execute(select(Tag).where(Tag.id.in_(tag_ids))).scalars().all()
            task.tags = tags

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True

    def count(self) -> int:
        from .models import Task
        return self.db.query(Task).count()
