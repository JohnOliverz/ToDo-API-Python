from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    completed: str
    user_id: int

    class Config:
        orm_mode = True