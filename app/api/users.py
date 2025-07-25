from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from models.user import User
from schemas.user import UserOut, UserCreate
from auth import get_current_user, get_password_hash

router = APIRouter()

@router.get("/users/me", response_model=UserOut, summary="Meu Perfil", description="Obtém informações do usuário autenticado")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/users/me", response_model=UserOut, summary="Atualizar Perfil", description="Atualiza dados do usuário autenticado")
def update_current_user(user_data: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.username = user_data.username
    current_user.email = user_data.email
    if user_data.password:
        current_user.hashed_password = get_password_hash(user_data.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/users/me", summary="Deletar Conta", description="Remove a conta do usuário autenticado")
def delete_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}