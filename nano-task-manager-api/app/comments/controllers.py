from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db

from .services import CommentService
from .schemas import CommentCreate, CommentResponse, CommentList, CommentUpdate

comment_router = APIRouter(prefix="/comments", tags=["Comments"])


@comment_router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment_data: CommentCreate, db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.create_comment(
        task_id=comment_data.task_id,
        author_id=comment_data.author_id,
        content=comment_data.content
    )


@comment_router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.get_comment(comment_id)


@comment_router.get("/task/{task_id}", response_model=CommentList)
def get_comments_by_task(task_id: int, skip: int = 0, limit: int = 100,
                         db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.get_comments_by_task(task_id=task_id, skip=skip, limit=limit)


@comment_router.get("/author/{author_id}", response_model=CommentList)
def get_comments_by_author(author_id: int, skip: int = 0, limit: int = 100,
                           db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.get_comments_by_author(author_id=author_id, skip=skip, limit=limit)


@comment_router.get("/", response_model=CommentList)
def get_all_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.get_all_comments(skip=skip, limit=limit)


@comment_router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment_data: CommentUpdate, db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.update_comment(comment_id=comment_id, content=comment_data.content)


@comment_router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    service = CommentService(db)
    service.delete_comment(comment_id)
    return None
