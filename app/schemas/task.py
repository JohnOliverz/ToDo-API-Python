from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., description="Título da tarefa", example="Estudar FastAPI")
    description: Optional[str] = Field(None, description="Descrição detalhada", example="Ler documentação e fazer exercícios")

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int = Field(..., description="ID único da tarefa")
    completed: str = Field(..., description="Status da tarefa", example="Pendente")
    user_id: int = Field(..., description="ID do usuário proprietário")

    class Config:
        from_attributes = True