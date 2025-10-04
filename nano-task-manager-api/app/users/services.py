from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional


class UserService:
    def __init__(self, db: Session):
        from .repository import UserRepository
        self.repo = UserRepository(db)

    def create_user(self, name: str, email: str):
        existing_user = self.repo.get_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        return self.repo.create(name=name, email=email)

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def get_user_by_email(self, email: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def get_all_users(self, skip: int = 0, limit: int = 100):
        users = self.repo.get_all(skip=skip, limit=limit)
        total = self.repo.count()
        return {"users": users, "total": total}

    def update_user(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if email and email != user.email:
            existing_user = self.repo.get_by_email(email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        return self.repo.update(user_id=user_id, name=name, email=email)

    def delete_user(self, user_id: int):
        if not self.repo.delete(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return {"message": "User deleted successfully"}
