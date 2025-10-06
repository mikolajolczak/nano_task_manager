import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from ..core.database import Base
from ..tags.models import task_tag


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="todo")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.UTC))
    tags = relationship("Tag", secondary=task_tag, back_populates="tasks")

    project = relationship("Project", back_populates="task")
    assignee = relationship("User", back_populates="tasks")