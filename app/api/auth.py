from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.session import get_db
from models.user import User
from schemas.auth import Token, UserRegister, UserLogin
from common.auth import verify_password, create_access_token, get_password_hash

router = APIRouter()

@router.post("/token", response_model=Token, summary="Login", description="Autentica usuário e retorna token JWT")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    if not login_data.username or not login_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username e password são obrigatórios"
        )
    
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", summary="Registrar Usuário", description="Cria uma nova conta de usuário")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Validar dados
    from common.validators import validate_username, validate_password_strength
    username = validate_username(user_data.username)
    password = validate_password_strength(user_data.password)
    
    # Verificar se usuário já existe
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=409, detail="Username já cadastrado")
    
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    
    hashed_password = get_password_hash(password)
    user = User(username=username, email=user_data.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "Usuário criado com sucesso"}