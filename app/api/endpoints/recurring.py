from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.services.service import RecurringTodoService
from app.schemas import schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.RecurringTodo)
def create_recurring_todo(
    todo: schemas.RecurringTodoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle tâche récurrente"""
    return RecurringTodoService.create_recurring_todo(db, todo, current_user.id)

@router.get("/", response_model=List[schemas.RecurringTodo])
def get_recurring_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer toutes les tâches récurrentes"""
    return RecurringTodoService.get_recurring_todos(db, current_user.id, skip, limit)

@router.put("/{recurring_id}", response_model=schemas.RecurringTodo)
def update_recurring_todo(
    recurring_id: int,
    todo: schemas.RecurringTodoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une tâche récurrente"""
    return RecurringTodoService.update_recurring_todo(db, recurring_id, todo, current_user.id)

@router.delete("/{recurring_id}")
def delete_recurring_todo(
    recurring_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une tâche récurrente"""
    RecurringTodoService.delete_recurring_todo(db, recurring_id, current_user.id)
    return {"status": "success"}

@router.post("/{recurring_id}/generate")
def generate_todo_from_recurring(
    recurring_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Générer une nouvelle tâche à partir d'une tâche récurrente"""
    return RecurringTodoService.generate_todo(db, recurring_id, current_user.id) 