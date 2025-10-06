from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db

from .services import TaskService
from .schemas import TaskCreate, TaskResponse, TaskList, TaskUpdate

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.create_task(
        title=task_data.title,
        project_id=task_data.project_id,
        description=task_data.description,
        task_status=task_data.status,
        assignee_id=task_data.assignee_id,
        tag_ids=task_data.tag_ids
    )


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_task(task_id)


@task_router.get("/project/{project_id}", response_model=TaskList)
def get_tasks_by_project(project_id: int, skip: int = 0, limit: int = 100,
                         db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_tasks_by_project(project_id=project_id, skip=skip, limit=limit)


@task_router.get("/assignee/{assignee_id}", response_model=TaskList)
def get_tasks_by_assignee(assignee_id: int, skip: int = 0, limit: int = 100,
                          db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_tasks_by_assignee(assignee_id=assignee_id, skip=skip, limit=limit)


@task_router.get("/status/{status}", response_model=TaskList)
def get_tasks_by_status(task_status: str, skip: int = 0, limit: int = 100,
                        db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_tasks_by_status(task_status=task_status, skip=skip, limit=limit)


@task_router.get("/", response_model=TaskList)
def get_all_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_all_tasks(skip=skip, limit=limit)


@task_router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.update_task(
        task_id=task_id,
        title=task_data.title,
        description=task_data.description,
        task_status=task_data.status,
        assignee_id=task_data.assignee_id,
        tag_ids=task_data.tag_ids,
        project_id=task_data.project_id
    )


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    service = TaskService(db)
    service.delete_task(task_id)
