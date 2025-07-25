from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., description="Nome de usuário único", example="joao_silva")
    email: EmailStr = Field(..., description="Email válido", example="joao@email.com")

class UserCreate(UserBase):
    password: Optional[str] = Field(None, description="Senha (opcional para atualização)", example="senha123")

class UserOut(UserBase):
    id: int = Field(..., description="ID único do usuário")

    class Config:
        from_attributes = True

