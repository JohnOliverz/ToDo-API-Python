import pytest
from fastapi import status

class TestAuth:
    """Testes para endpoints de autenticação"""
    
    def test_register_success(self, client, db_session):
        """Teste: Registro de usuário com sucesso"""
        response = client.post("/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123"
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Usuário criado com sucesso"
    
    def test_register_duplicate_username(self, client, test_user):
        """Teste: Registro com username duplicado"""
        response = client.post("/register", json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "pass123"
        })
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "Username já cadastrado" in response.json()["detail"]
    
    def test_register_duplicate_email(self, client, test_user):
        """Teste: Registro com email duplicado"""
        response = client.post("/register", json={
            "username": "anotheruser",
            "email": "test@example.com",
            "password": "pass123"
        })
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "Email já cadastrado" in response.json()["detail"]
    
    def test_register_invalid_username(self, client, db_session):
        """Teste: Username inválido (muito curto)"""
        response = client.post("/register", json={
            "username": "ab",
            "email": "test@example.com",
            "password": "pass123"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "pelo menos 3 caracteres" in response.json()["detail"]
    
    def test_register_invalid_password(self, client, db_session):
        """Teste: Senha inválida (muito curta)"""
        response = client.post("/register", json={
            "username": "validuser",
            "email": "test@example.com",
            "password": "123"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "pelo menos 6 caracteres" in response.json()["detail"]
    
    def test_register_password_no_letter(self, client, db_session):
        """Teste: Senha sem letra"""
        response = client.post("/register", json={
            "username": "validuser",
            "email": "test@example.com",
            "password": "123456"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "pelo menos uma letra" in response.json()["detail"]
    
    def test_register_password_no_number(self, client, db_session):
        """Teste: Senha sem número"""
        response = client.post("/register", json={
            "username": "validuser",
            "email": "test@example.com",
            "password": "abcdef"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "pelo menos um número" in response.json()["detail"]
    
    def test_login_success(self, client, test_user):
        """Teste: Login com sucesso"""
        response = client.post("/token", json={
            "username": "testuser",
            "password": "testpass123"
        })
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
    
    def test_login_wrong_username(self, client, db_session):
        """Teste: Login com username inexistente"""
        response = client.post("/token", json={
            "username": "wronguser",
            "password": "testpass123"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Usuário não encontrado" in response.json()["detail"]
    
    def test_login_wrong_password(self, client, test_user):
        """Teste: Login com senha incorreta"""
        response = client.post("/token", json={
            "username": "testuser",
            "password": "wrongpass"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Senha incorreta" in response.json()["detail"]
    
    def test_login_empty_credentials(self, client, db_session):
        """Teste: Login com credenciais vazias"""
        response = client.post("/token", json={
            "username": "",
            "password": ""
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "obrigatórios" in response.json()["detail"]