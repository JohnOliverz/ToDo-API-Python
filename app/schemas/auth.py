from pydantic import BaseModel, Field, EmailStr

class Token(BaseModel):
    access_token: str = Field(..., description="Token JWT para autenticação")
    token_type: str = Field(..., description="Tipo do token", example="bearer")

class UserLogin(BaseModel):
    username: str = Field(..., description="Nome de usuário", example="joao_silva")
    password: str = Field(..., description="Senha do usuário", example="senha123")

class UserRegister(BaseModel):
    username: str = Field(..., description="Nome de usuário único", example="joao_silva")
    email: EmailStr = Field(..., description="Email válido", example="joao@email.com")
    password: str = Field(..., description="Senha do usuário", example="senha123")