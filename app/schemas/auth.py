from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str = Field(..., description="Token JWT para autenticação")
    token_type: str = Field(..., description="Tipo do token", example="bearer")

class UserLogin(BaseModel):
    username: str = Field(..., description="Nome de usuário", example="joao_silva")
    password: str = Field(..., description="Senha do usuário", example="senha123")