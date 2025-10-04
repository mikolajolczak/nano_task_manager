from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db

from .schemas import UserCreate, UserResponse, UserList, UserUpdate
from .services import UserService

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):


    service = UserService(db)
    user = service.create_user(name=user_data.name, email=user_data.email)
    return user


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    service = UserService(db)
    return service.get_user(user_id)


@user_router.get("/", response_model=UserList)
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    service = UserService(db)
    return service.get_all_users(skip=skip, limit=limit)


@user_router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):

    service = UserService(db)
    return service.update_user(
        user_id=user_id,
        name=user_data.name,
        email=user_data.email
    )


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):

    service = UserService(db)
    service.delete_user(user_id)
    return None