from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.services.service import TagService
from app.schemas import schemas
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Tag)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer un nouveau tag"""
    return TagService.create_tag(db, tag)

@router.get("/", response_model=List[schemas.Tag])
def get_tags(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer tous les tags"""
    return TagService.get_tags(db)

@router.put("/{tag_id}", response_model=schemas.Tag)
def update_tag(
    tag_id: int,
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour un tag"""
    return TagService.update_tag(db, tag_id, tag)

@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer un tag"""
    TagService.delete_tag(db, tag_id)
    return {"status": "success"} 