from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db

from .services import ProjectService
from .schemas import ProjectCreate, ProjectResponse, ProjectList, ProjectUpdate

project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    return service.create_project(
        name=project_data.name,
        owner_id=project_data.owner_id,
        description=project_data.description
    )


@project_router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    service = ProjectService(db)
    return service.get_project(project_id)


@project_router.get("/owner/{owner_id}", response_model=ProjectList)
def get_projects_by_owner(owner_id: int, skip: int = 0, limit: int = 100,
                          db: Session = Depends(get_db)):
    service = ProjectService(db)
    return service.get_projects_by_owner(owner_id=owner_id, skip=skip, limit=limit)


@project_router.get("/", response_model=ProjectList)
def get_all_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ProjectService(db)
    return service.get_all_projects(skip=skip, limit=limit)


@project_router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    return service.update_project(
        project_id=project_id,
        name=project_data.name,
        description=project_data.description
    )


@project_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    service = ProjectService(db)
    service.delete_project(project_id)
    return None
