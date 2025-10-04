from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional, List


class TaskService:
    def __init__(self, db: Session):
        from .repository import TaskRepository
        self.repo = TaskRepository(db)
        self.db = db

    def create_task(self, title: str, project_id: int, description: Optional[str] = None,
                    task_status: str = "todo", assignee_id: Optional[int] = None,
                    tag_ids=None):
        if tag_ids is None:
            tag_ids = []
        self._validate_project_exists(project_id)
        if assignee_id:
            self._validate_user_exists(assignee_id)
        if tag_ids:
            self._validate_tags_exist(tag_ids)

        return self.repo.create(
            title=title,
            project_id=project_id,
            description=description,
            status=task_status,
            assignee_id=assignee_id,
            tag_ids=tag_ids
        )

    def get_task(self, task_id: int):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task

    def get_tasks_by_project(self, project_id: int, skip: int = 0, limit: int = 100):
        self._validate_project_exists(project_id)
        tasks = self.repo.get_by_project(project_id=project_id, skip=skip, limit=limit)
        return {"tasks": tasks, "total": len(tasks)}

    def get_tasks_by_assignee(self, assignee_id: int, skip: int = 0, limit: int = 100):
        self._validate_user_exists(assignee_id)
        tasks = self.repo.get_by_assignee(assignee_id=assignee_id, skip=skip, limit=limit)
        return {"tasks": tasks, "total": len(tasks)}

    def get_tasks_by_status(self, task_status: str, skip: int = 0, limit: int = 100):
        tasks = self.repo.get_by_status(status=task_status, skip=skip, limit=limit)
        return {"tasks": tasks, "total": len(tasks)}

    def get_all_tasks(self, skip: int = 0, limit: int = 100):
        tasks = self.repo.get_all(skip=skip, limit=limit)
        total = self.repo.count()
        return {"tasks": tasks, "total": total}

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, task_status: Optional[str] = None,
                    assignee_id: Optional[int] = None, tag_ids: Optional[List[int]] = None):
        if assignee_id:
            self._validate_user_exists(assignee_id)
        if tag_ids is not None:
            self._validate_tags_exist(tag_ids)

        task = self.repo.update(
            task_id=task_id,
            title=title,
            description=description,
            status=task_status,
            assignee_id=assignee_id,
            tag_ids=tag_ids
        )

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task

    def delete_task(self, task_id: int):
        if not self.repo.delete(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return {"message": "Task deleted successfully"}

    def _validate_project_exists(self, project_id: int):
        from ..projects.repository import ProjectRepository
        project_repo = ProjectRepository(self.db)
        if not project_repo.get_by_id(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

    def _validate_user_exists(self, user_id: int):
        from ..users.repository import UserRepository
        user_repo = UserRepository(self.db)
        if not user_repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    def _validate_tags_exist(self, tag_ids: List[int]):
        from ..tags.repository import TagRepository
        tag_repo = TagRepository(self.db)
        tags = tag_repo.get_by_ids(tag_ids)
        if len(tags) != len(tag_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more tags not found"
            )
