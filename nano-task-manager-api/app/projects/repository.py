from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, owner_id: int, description: Optional[str] = None):
        from .models import Project
        project = Project(name=name, owner_id=owner_id, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: int):
        from .models import Project
        return self.db.execute(
            select(Project).where(Project.id == project_id)
        ).scalar_one_or_none()

    def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100):
        from .models import Project
        return self.db.execute(
            select(Project).where(Project.owner_id == owner_id).offset(skip).limit(limit)
        ).scalars().all()

    def get_all(self, skip: int = 0, limit: int = 100):
        from .models import Project
        return self.db.execute(
            select(Project).offset(skip).limit(limit)
        ).scalars().all()

    def update(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None):
        project = self.get_by_id(project_id)
        if not project:
            return None
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> bool:
        project = self.get_by_id(project_id)
        if not project:
            return False
        self.db.delete(project)
        self.db.commit()
        return True

    def count(self) -> int:
        from .models import Project
        return self.db.query(Project).count()
