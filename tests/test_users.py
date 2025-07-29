import pytest
from fastapi import status

class TestUsers:
    """Testes para endpoints de usuários"""
    
    def test_get_current_user_success(self, client, auth_headers):
        """Teste: Obter perfil do usuário autenticado"""
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "id" in data
    
    def test_get_current_user_unauthorized(self, client):
        """Teste: Obter perfil sem autenticação"""
        response = client.get("/users/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user_invalid_token(self, client):
        """Teste: Obter perfil com token inválido"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_user_success(self, client, auth_headers):
        """Teste: Atualizar perfil com sucesso"""
        response = client.put("/users/me", headers=auth_headers, json={
            "username": "updateduser",
            "email": "updated@example.com"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "updateduser"
        assert data["email"] == "updated@example.com"
    
    def test_update_user_with_password(self, client, auth_headers):
        """Teste: Atualizar perfil incluindo senha"""
        response = client.put("/users/me", headers=auth_headers, json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "newpass123"
        })
        assert response.status_code == status.HTTP_200_OK
        
        # Testar login com nova senha
        login_response = client.post("/token", json={
            "username": "testuser",
            "password": "newpass123"
        })
        assert login_response.status_code == status.HTTP_200_OK
    
    def test_update_user_invalid_username(self, client, auth_headers):
        """Teste: Atualizar com username inválido"""
        response = client.put("/users/me", headers=auth_headers, json={
            "username": "ab",
            "email": "test@example.com"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "pelo menos 3 caracteres" in response.json()["detail"]
    
    def test_update_user_invalid_password(self, client, auth_headers):
        """Teste: Atualizar com senha inválida"""
        response = client.put("/users/me", headers=auth_headers, json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "pelo menos 6 caracteres" in response.json()["detail"]
    
    def test_update_user_unauthorized(self, client):
        """Teste: Atualizar perfil sem autenticação"""
        response = client.put("/users/me", json={
            "username": "testuser",
            "email": "test@example.com"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_user_success(self, client, auth_headers):
        """Teste: Deletar conta com sucesso"""
        response = client.delete("/users/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert "deleted successfully" in response.json()["message"]
        
        # Verificar que não consegue mais fazer login
        login_response = client.post("/token", json={
            "username": "testuser",
            "password": "testpass123"
        })
        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_user_unauthorized(self, client):
        """Teste: Deletar conta sem autenticação"""
        response = client.delete("/users/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED