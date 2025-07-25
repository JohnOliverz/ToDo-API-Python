from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from models.task import Task
from models.user import User
from schemas.task import TaskCreate, TaskOut
from auth import get_current_user

router = APIRouter()

@router.post("/tasks", response_model=TaskOut, summary="Criar Tarefa", description="Cria uma nova tarefa para o usuário autenticado")
def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[TaskOut], summary="Listar Tarefas", description="Lista todas as tarefas do usuário autenticado")
def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.user_id == current_user.id).all()

@router.put("/tasks/{task_id}", response_model=TaskOut, summary="Atualizar Tarefa", description="Atualiza uma tarefa específica do usuário")
def update_task(task_id: int, task: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/tasks/{task_id}/complete", summary="Completar Tarefa", description="Marca uma tarefa como concluída")
def complete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.completed = "Concluída"
    db.commit()
    return {"message": "Task completed"}

@router.delete("/tasks/{task_id}", summary="Deletar Tarefa", description="Remove uma tarefa específica do usuário")
def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}