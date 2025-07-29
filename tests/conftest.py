import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adicionar app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import app
from database.session import get_db
from database.base import Base
from models.user import User
from models.task import Task
from common.auth import get_password_hash

# Banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user(client, db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post("/token", json={
        "username": "testuser",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_task(client, db_session, test_user):
    task = Task(
        title="Test Task",
        description="Test Description",
        status="Pendente",
        user_id=test_user.id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task