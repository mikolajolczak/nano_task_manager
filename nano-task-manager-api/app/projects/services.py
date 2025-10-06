from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional


class ProjectService:
    def __init__(self, db: Session):
        from .repository import ProjectRepository
        self.repo = ProjectRepository(db)
        self.db = db

    def create_project(self, name: str, owner_id: int, description: Optional[str] = None):
        self._validate_user_exists(owner_id)
        return self.repo.create(name=name, owner_id=owner_id, description=description)

    def get_project(self, project_id: int):
        project = self.repo.get_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return project

    def get_projects_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100):
        self._validate_user_exists(owner_id)
        projects = self.repo.get_by_owner(owner_id=owner_id, skip=skip, limit=limit)
        return {"projects": projects, "total": len(projects)}

    def get_all_projects(self, skip: int = 0, limit: int = 100):
        projects = self.repo.get_all(skip=skip, limit=limit)
        total = self.repo.count()
        return {"projects": projects, "total": total}

    def update_project(self, project_id: int, name: Optional[str] = None,
                       description: Optional[str] = None, owner_id: Optional[int] = None):
        project = self.repo.update(project_id=project_id, name=name, description=description, owner_id=owner_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return project

    def delete_project(self, project_id: int):
        if not self.repo.delete(project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return {"message": "Project deleted successfully"}

    def _validate_user_exists(self, user_id: int):
        from ..users.repository import UserRepository
        user_repo = UserRepository(self.db)
        if not user_repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
