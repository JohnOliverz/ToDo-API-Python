import pytest
from fastapi import status

class TestIntegration:
    """Testes de integração - fluxos completos"""
    
    def test_complete_user_workflow(self, client, db_session):
        """Teste: Fluxo completo do usuário"""
        # 1. Registrar usuário
        register_response = client.post("/register", json={
            "username": "integrationuser",
            "email": "integration@example.com",
            "password": "intpass123"
        })
        assert register_response.status_code == status.HTTP_200_OK
        
        # 2. Fazer login
        login_response = client.post("/token", json={
            "username": "integrationuser",
            "password": "intpass123"
        })
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Obter perfil
        profile_response = client.get("/users/me", headers=headers)
        assert profile_response.status_code == status.HTTP_200_OK
        assert profile_response.json()["username"] == "integrationuser"
        
        # 4. Atualizar perfil
        update_response = client.put("/users/me", headers=headers, json={
            "username": "updatedintegration",
            "email": "updated@example.com"
        })
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["username"] == "updatedintegration"
    
    def test_complete_task_workflow(self, client, auth_headers):
        """Teste: Fluxo completo de tarefas"""
        # 1. Criar tarefa
        create_response = client.post("/tasks", headers=auth_headers, json={
            "title": "Tarefa de Integração",
            "description": "Teste de fluxo completo"
        })
        assert create_response.status_code == status.HTTP_200_OK
        task_id = create_response.json()["id"]
        
        # 2. Listar tarefas
        list_response = client.get("/tasks", headers=auth_headers)
        assert list_response.status_code == status.HTTP_200_OK
        tasks = list_response.json()
        assert len(tasks) >= 1
        assert any(task["id"] == task_id for task in tasks)
        
        # 3. Atualizar tarefa
        update_response = client.put(f"/tasks/{task_id}", headers=auth_headers, json={
            "title": "Tarefa Atualizada",
            "description": "Descrição atualizada"
        })
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["title"] == "Tarefa Atualizada"
        
        # 4. Mudar status para Em Progresso
        status_response = client.patch(f"/tasks/{task_id}/status", headers=auth_headers, json={
            "status": "Em Progresso"
        })
        assert status_response.status_code == status.HTTP_200_OK
        
        # 5. Marcar como concluída
        complete_response = client.patch(f"/tasks/{task_id}/status", headers=auth_headers, json={
            "status": "Concluída"
        })
        assert complete_response.status_code == status.HTTP_200_OK
        
        # 6. Deletar tarefa
        delete_response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert delete_response.status_code == status.HTTP_200_OK
        
        # 7. Verificar que foi deletada
        final_list = client.get("/tasks", headers=auth_headers)
        final_tasks = final_list.json()
        assert not any(task["id"] == task_id for task in final_tasks)
    
    def test_task_isolation_between_users(self, client, db_session):
        """Teste: Isolamento de tarefas entre usuários"""
        # Criar dois usuários
        client.post("/register", json={
            "username": "user1", "email": "user1@test.com", "password": "pass123"
        })
        client.post("/register", json={
            "username": "user2", "email": "user2@test.com", "password": "pass123"
        })
        
        # Login dos dois usuários
        token1 = client.post("/token", json={"username": "user1", "password": "pass123"}).json()["access_token"]
        token2 = client.post("/token", json={"username": "user2", "password": "pass123"}).json()["access_token"]
        
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # User1 cria uma tarefa
        task_response = client.post("/tasks", headers=headers1, json={
            "title": "Tarefa do User1", "description": "Privada"
        })
        task_id = task_response.json()["id"]
        
        # User2 não deve ver a tarefa do User1
        user2_tasks = client.get("/tasks", headers=headers2).json()
        assert len(user2_tasks) == 0
        
        # User2 não deve conseguir acessar a tarefa do User1
        access_response = client.get(f"/tasks", headers=headers2)
        user2_task_ids = [task["id"] for task in access_response.json()]
        assert task_id not in user2_task_ids
        
        # User2 não deve conseguir deletar tarefa do User1
        delete_response = client.delete(f"/tasks/{task_id}", headers=headers2)
        assert delete_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_authentication_required_for_protected_endpoints(self, client, db_session):
        """Teste: Autenticação obrigatória para endpoints protegidos"""
        protected_endpoints = [
            ("GET", "/users/me"),
            ("PUT", "/users/me"),
            ("DELETE", "/users/me"),
            ("GET", "/tasks"),
            ("POST", "/tasks"),
            ("PUT", "/tasks/1"),
            ("PATCH", "/tasks/1/status"),
            ("DELETE", "/tasks/1")
        ]
        
        for method, endpoint in protected_endpoints:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "POST":
                response = client.post(endpoint, json={})
            elif method == "PUT":
                response = client.put(endpoint, json={})
            elif method == "PATCH":
                response = client.patch(endpoint, json={})
            elif method == "DELETE":
                response = client.delete(endpoint)
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED