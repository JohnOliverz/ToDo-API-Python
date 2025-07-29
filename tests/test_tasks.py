import pytest
from fastapi import status

class TestTasks:
    """Testes para endpoints de tarefas"""
    
    def test_create_task_success(self, client, auth_headers):
        """Teste: Criar tarefa com sucesso"""
        response = client.post("/tasks", headers=auth_headers, json={
            "title": "Nova Tarefa",
            "description": "Descrição da nova tarefa"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Nova Tarefa"
        assert data["description"] == "Descrição da nova tarefa"
        assert data["status"] == "Pendente"
        assert "id" in data
        assert "user_id" in data
    
    def test_create_task_without_description(self, client, auth_headers):
        """Teste: Criar tarefa sem descrição"""
        response = client.post("/tasks", headers=auth_headers, json={
            "title": "Tarefa sem descrição"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Tarefa sem descrição"
        assert data["description"] is None
    
    def test_create_task_empty_title(self, client, auth_headers):
        """Teste: Criar tarefa com título vazio"""
        response = client.post("/tasks", headers=auth_headers, json={
            "title": "",
            "description": "Descrição"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "não pode estar vazio" in response.json()["detail"]
    
    def test_create_task_title_too_long(self, client, auth_headers):
        """Teste: Criar tarefa com título muito longo"""
        long_title = "a" * 201
        response = client.post("/tasks", headers=auth_headers, json={
            "title": long_title,
            "description": "Descrição"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "máximo 200 caracteres" in response.json()["detail"]
    
    def test_create_task_description_too_long(self, client, auth_headers):
        """Teste: Criar tarefa com descrição muito longa"""
        long_description = "a" * 1001
        response = client.post("/tasks", headers=auth_headers, json={
            "title": "Título válido",
            "description": long_description
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "máximo 1000 caracteres" in response.json()["detail"]
    
    def test_create_task_unauthorized(self, client):
        """Teste: Criar tarefa sem autenticação"""
        response = client.post("/tasks", json={
            "title": "Tarefa",
            "description": "Descrição"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_tasks_success(self, client, auth_headers, test_task):
        """Teste: Listar tarefas com sucesso"""
        response = client.get("/tasks", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["title"] == "Test Task"
    
    def test_get_tasks_empty(self, client, auth_headers):
        """Teste: Listar tarefas quando não há nenhuma"""
        response = client.get("/tasks", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_get_tasks_unauthorized(self, client):
        """Teste: Listar tarefas sem autenticação"""
        response = client.get("/tasks")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_task_success(self, client, auth_headers, test_task):
        """Teste: Atualizar tarefa com sucesso"""
        response = client.put(f"/tasks/{test_task.id}", headers=auth_headers, json={
            "title": "Tarefa Atualizada",
            "description": "Nova descrição"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Tarefa Atualizada"
        assert data["description"] == "Nova descrição"
    
    def test_update_task_not_found(self, client, auth_headers):
        """Teste: Atualizar tarefa inexistente"""
        response = client.put("/tasks/999", headers=auth_headers, json={
            "title": "Tarefa",
            "description": "Descrição"
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "não encontrada" in response.json()["detail"]
    
    def test_update_task_invalid_id(self, client, auth_headers):
        """Teste: Atualizar tarefa com ID inválido"""
        response = client.put("/tasks/0", headers=auth_headers, json={
            "title": "Tarefa",
            "description": "Descrição"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "número positivo" in response.json()["detail"]
    
    def test_update_task_unauthorized(self, client, test_task):
        """Teste: Atualizar tarefa sem autenticação"""
        response = client.put(f"/tasks/{test_task.id}", json={
            "title": "Tarefa",
            "description": "Descrição"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_task_status_success(self, client, auth_headers, test_task):
        """Teste: Atualizar status da tarefa com sucesso"""
        response = client.patch(f"/tasks/{test_task.id}/status", headers=auth_headers, json={
            "status": "Em Progresso"
        })
        assert response.status_code == status.HTTP_200_OK
        assert "Em Progresso" in response.json()["message"]
    
    def test_update_task_status_to_completed(self, client, auth_headers, test_task):
        """Teste: Marcar tarefa como concluída"""
        response = client.patch(f"/tasks/{test_task.id}/status", headers=auth_headers, json={
            "status": "Concluída"
        })
        assert response.status_code == status.HTTP_200_OK
        assert "Concluída" in response.json()["message"]
    
    def test_update_task_status_invalid_status(self, client, auth_headers, test_task):
        """Teste: Atualizar com status inválido"""
        response = client.patch(f"/tasks/{test_task.id}/status", headers=auth_headers, json={
            "status": "Status Inválido"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_update_task_status_not_found(self, client, auth_headers):
        """Teste: Atualizar status de tarefa inexistente"""
        response = client.patch("/tasks/999/status", headers=auth_headers, json={
            "status": "Em Progresso"
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_task_status_unauthorized(self, client, test_task):
        """Teste: Atualizar status sem autenticação"""
        response = client.patch(f"/tasks/{test_task.id}/status", json={
            "status": "Em Progresso"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_task_success(self, client, auth_headers, test_task):
        """Teste: Deletar tarefa com sucesso"""
        response = client.delete(f"/tasks/{test_task.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert "deletada com sucesso" in response.json()["message"]
        
        # Verificar que a tarefa foi deletada
        get_response = client.get("/tasks", headers=auth_headers)
        tasks = get_response.json()
        task_ids = [task["id"] for task in tasks]
        assert test_task.id not in task_ids
    
    def test_delete_task_not_found(self, client, auth_headers):
        """Teste: Deletar tarefa inexistente"""
        response = client.delete("/tasks/999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "não encontrada" in response.json()["detail"]
    
    def test_delete_task_invalid_id(self, client, auth_headers):
        """Teste: Deletar tarefa com ID inválido"""
        response = client.delete("/tasks/0", headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "número positivo" in response.json()["detail"]
    
    def test_delete_task_unauthorized(self, client, test_task):
        """Teste: Deletar tarefa sem autenticação"""
        response = client.delete(f"/tasks/{test_task.id}")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED