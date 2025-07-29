from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=True)
    status = Column(String, index=True, default="Pendente")
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", backref="tasks")