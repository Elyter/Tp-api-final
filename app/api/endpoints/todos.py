from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.dependencies import get_db, get_current_user
from app.services.service import TodoService
from app.schemas import schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Todo])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer toutes les tâches"""
    return TodoService.get_todos(db, current_user.id, skip=skip, limit=limit)

@router.get("/search", response_model=List[schemas.Todo])
def search_todos(
    query: str = Query(..., description="Terme de recherche"),
    completed: Optional[bool] = None,
    tag_id: Optional[int] = None,
    priority: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Rechercher des tâches avec filtres optionnels"""
    return TodoService.search_todos(
        db=db,
        user_id=current_user.id,
        query=query,
        completed=completed,
        tag_id=tag_id,
        priority=priority
    )

@router.get("/{todo_id}", response_model=schemas.Todo)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer une tâche spécifique"""
    todo = TodoService.get_todo(db, todo_id, current_user.id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo non trouvé"
        )
    return todo

@router.post("/", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle tâche"""
    return TodoService.create_todo(db, todo, current_user.id)

@router.put("/{todo_id}", response_model=schemas.Todo)
def update_todo(
    todo_id: int,
    todo_update: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une tâche"""
    todo = TodoService.update_todo(db, todo_id, todo_update, current_user.id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo non trouvé"
        )
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une tâche"""
    if not TodoService.delete_todo(db, todo_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo non trouvé"
        )
    return None