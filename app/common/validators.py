import re
from pydantic import validator
from fastapi import HTTPException

def validate_password_strength(password: str) -> str:
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 6 caracteres")
    
    if not re.search(r"[A-Za-z]", password):
        raise HTTPException(status_code=400, detail="Senha deve conter pelo menos uma letra")
    
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Senha deve conter pelo menos um número")
    
    return password

def validate_username(username: str) -> str:
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username deve ter pelo menos 3 caracteres")
    
    if len(username) > 50:
        raise HTTPException(status_code=400, detail="Username deve ter no máximo 50 caracteres")
    
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        raise HTTPException(status_code=400, detail="Username deve conter apenas letras, números e underscore")
    
    return username

def validate_task_title(title: str) -> str:
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Título da tarefa não pode estar vazio")
    
    if len(title.strip()) > 200:
        raise HTTPException(status_code=400, detail="Título deve ter no máximo 200 caracteres")
    
    return title.strip()

def validate_task_description(description: str) -> str:
    if description and len(description) > 1000:
        raise HTTPException(status_code=400, detail="Descrição deve ter no máximo 1000 caracteres")
    
    return description.strip() if description else None