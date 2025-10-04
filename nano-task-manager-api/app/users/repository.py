from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, email: str):
        from .models import User
        user = User(name=name, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int):
        from .models import User
        return self.db.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()

    def get_by_email(self, email: str):
        from .models import User
        return self.db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100):
        from .models import User
        return self.db.execute(
            select(User).offset(skip).limit(limit)
        ).scalars().all()

    def update(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None):
        user = self.get_by_id(user_id)
        if not user:
            return None
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def count(self) -> int:
        from .models import User
        return self.db.query(User).count()
