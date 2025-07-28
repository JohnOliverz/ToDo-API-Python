from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from common.validators import validate_username, validate_password_strength

class UserBase(BaseModel):
    username: str = Field(..., description="Nome de usuário único", example="joao_silva")
    email: EmailStr = Field(..., description="Email válido", example="joao@email.com")
    
    @validator('username')
    def validate_username_field(cls, v):
        return validate_username(v)

class UserCreate(UserBase):
    password: Optional[str] = Field(None, description="Senha (opcional para atualização)", example="senha123")
    
    @validator('password')
    def validate_password_field(cls, v):
        if v is not None:
            return validate_password_strength(v)
        return v

class UserOut(UserBase):
    id: int = Field(..., description="ID único do usuário")

    class Config:
        from_attributes = True

