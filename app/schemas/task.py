from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from common.validators import validate_task_title, validate_task_description

class TaskBase(BaseModel):
    title: str = Field(..., description="Título da tarefa", example="Estudar FastAPI")
    description: Optional[str] = Field(None, description="Descrição detalhada", example="Ler documentação e fazer exercícios")
    
    @validator('title')
    def validate_title_field(cls, v):
        return validate_task_title(v)
    
    @validator('description')
    def validate_description_field(cls, v):
        return validate_task_description(v)

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int = Field(..., description="ID único da tarefa")
    status: str = Field(..., description="Status da tarefa", example="Pendente")
    user_id: int = Field(..., description="ID do usuário proprietário")

    class Config:
        from_attributes = True

class TaskStatusUpdate(BaseModel):
    status: Literal["Pendente", "Em Progresso", "Concluída"] = Field(..., description="Novo status da tarefa", example="Em Progresso")