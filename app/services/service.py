from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models import models
from app.schemas import schemas
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta

class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(models.User)\
                .filter(models.User.email == email)\
                .first()

    @staticmethod
    def create_user(db: Session, user: schemas.UserCreate):
        # Vérifier si l'email existe déjà
        db_user = UserService.get_user_by_email(db, user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email déjà enregistré"
            )
        
        # Créer le nouvel utilisateur
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = UserService.get_user_by_email(db, email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Utilisateur inactif"
            )
        return user

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = db.query(models.User)\
                .filter(models.User.id == user_id)\
                .first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        return user

class TagService:
    @staticmethod
    def create_tag(db: Session, tag: schemas.TagCreate) -> models.Tag:
        db_tag = models.Tag(**tag.dict())
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag

    @staticmethod
    def get_tags(db: Session) -> List[models.Tag]:
        return db.query(models.Tag).all()

    @staticmethod
    def get_tag(db: Session, tag_id: int) -> Optional[models.Tag]:
        return db.query(models.Tag).filter(models.Tag.id == tag_id).first()

    @staticmethod
    def update_tag(db: Session, tag_id: int, tag: schemas.TagCreate) -> models.Tag:
        db_tag = TagService.get_tag(db, tag_id)
        if not db_tag:
            raise HTTPException(status_code=404, detail="Tag non trouvé")
        
        for field, value in tag.dict().items():
            setattr(db_tag, field, value)
        
        db.commit()
        db.refresh(db_tag)
        return db_tag

    @staticmethod
    def delete_tag(db: Session, tag_id: int) -> bool:
        db_tag = TagService.get_tag(db, tag_id)
        if not db_tag:
            raise HTTPException(status_code=404, detail="Tag non trouvé")
        
        db.delete(db_tag)
        db.commit()
        return True

class TodoService:
    @staticmethod
    def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Todo]:
        """Récupérer toutes les tâches d'un utilisateur"""
        return db.query(models.Todo)\
                .filter(models.Todo.owner_id == user_id)\
                .offset(skip)\
                .limit(limit)\
                .all()

    @staticmethod
    def get_todo(db: Session, todo_id: int, user_id: int) -> Optional[models.Todo]:
        """Récupérer une tâche spécifique"""
        return db.query(models.Todo)\
                .filter(models.Todo.id == todo_id)\
                .filter(models.Todo.owner_id == user_id)\
                .first()

    @staticmethod
    def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int) -> models.Todo:
        """Créer une nouvelle tâche"""
        db_todo = models.Todo(
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            due_date=todo.due_date,
            owner_id=user_id
        )
        if todo.tag_ids:
            tags = db.query(models.Tag)\
                    .filter(models.Tag.id.in_(todo.tag_ids))\
                    .all()
            db_todo.tags.extend(tags)
        
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoUpdate, user_id: int) -> Optional[models.Todo]:
        """Mettre à jour une tâche"""
        db_todo = TodoService.get_todo(db, todo_id, user_id)
        if not db_todo:
            return None

        update_data = todo_update.model_dump(exclude_unset=True)
        
        # Gérer les tags séparément
        if "tag_ids" in update_data:
            tag_ids = update_data.pop("tag_ids")
            if tag_ids is not None:
                tags = db.query(models.Tag)\
                        .filter(models.Tag.id.in_(tag_ids))\
                        .all()
                db_todo.tags = tags

        # Mettre à jour les autres champs
        for field, value in update_data.items():
            setattr(db_todo, field, value)

        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete_todo(db: Session, todo_id: int, user_id: int) -> bool:
        """Supprimer une tâche"""
        db_todo = TodoService.get_todo(db, todo_id, user_id)
        if not db_todo:
            return False
        
        db.delete(db_todo)
        db.commit()
        return True

    @staticmethod
    def search_todos(
        db: Session,
        user_id: int,
        query: str,
        completed: Optional[bool] = None,
        tag_id: Optional[int] = None,
        priority: Optional[int] = None
    ) -> List[models.Todo]:
        """Rechercher des tâches avec filtres"""
        search = db.query(models.Todo)\
                  .filter(models.Todo.owner_id == user_id)

        # Recherche par texte
        if query:
            search = search.filter(
                or_(
                    models.Todo.title.ilike(f"%{query}%"),
                    models.Todo.description.ilike(f"%{query}%")
                )
            )

        # Filtres optionnels
        if completed is not None:
            search = search.filter(models.Todo.completed == completed)

        if tag_id:
            search = search.filter(models.Todo.tags.any(models.Tag.id == tag_id))

        if priority:
            search = search.filter(models.Todo.priority == priority)

        return search.all()

    @staticmethod
    def filter_todos(
        db: Session,
        user_id: int,
        search_term: Optional[str] = None,
        completed: Optional[bool] = None,
        tag_id: Optional[int] = None,
        priority: Optional[schemas.TodoPriority] = None,
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None
    ) -> List[models.Todo]:
        """Filtrer les tâches selon plusieurs critères"""
        query = db.query(models.Todo)\
                 .filter(models.Todo.owner_id == user_id)

        if search_term:
            query = query.filter(
                or_(
                    models.Todo.title.ilike(f"%{search_term}%"),
                    models.Todo.description.ilike(f"%{search_term}%")
                )
            )

        if completed is not None:
            query = query.filter(models.Todo.completed == completed)

        if tag_id:
            query = query.filter(models.Todo.tags.any(models.Tag.id == tag_id))

        if priority:
            query = query.filter(models.Todo.priority == priority)

        if due_before:
            query = query.filter(models.Todo.due_date <= due_before)

        if due_after:
            query = query.filter(models.Todo.due_date >= due_after)

        return query.all()

    @staticmethod
    def update_todo(
        db: Session, 
        todo_id: int, 
        todo_update: schemas.TodoUpdate, 
        user_id: int
    ) -> Optional[models.Todo]:
        """Mettre à jour une tâche existante"""
        db_todo = db.query(models.Todo)\
                   .filter(models.Todo.id == todo_id)\
                   .filter(models.Todo.owner_id == user_id)\
                   .first()
        
        if not db_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo non trouvé"
            )

        # Mise à jour des champs simples
        update_data = todo_update.dict(exclude_unset=True)
        
        # Gestion spéciale pour les tags si présents
        if 'tag_ids' in update_data:
            tag_ids = update_data.pop('tag_ids')
            if tag_ids is not None:
                tags = db.query(models.Tag)\
                         .filter(models.Tag.id.in_(tag_ids))\
                         .all()
                db_todo.tags = tags

        # Mise à jour des autres champs
        for field, value in update_data.items():
            setattr(db_todo, field, value)

        try:
            db.commit()
            db.refresh(db_todo)
            return db_todo
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erreur lors de la mise à jour: {str(e)}"
            )

class RecurringTodoService:
    @staticmethod
    def create_recurring_todo(
        db: Session, 
        todo: schemas.RecurringTodoCreate, 
        user_id: int
    ) -> models.RecurringTodo:
        todo_data = todo.dict(exclude={'tag_ids'})
        db_todo = models.RecurringTodo(**todo_data, owner_id=user_id)
        
        if todo.tag_ids:
            tags = db.query(models.Tag).filter(models.Tag.id.in_(todo.tag_ids)).all()
            db_todo.tags = tags
        
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def get_recurring_todos(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[models.RecurringTodo]:
        return db.query(models.RecurringTodo)\
                .filter(models.RecurringTodo.owner_id == user_id)\
                .filter(models.RecurringTodo.active == True)\
                .offset(skip)\
                .limit(limit)\
                .all()

    @staticmethod
    def update_recurring_todo(
        db: Session,
        recurring_id: int,
        todo: schemas.RecurringTodoUpdate,
        user_id: int
    ) -> models.RecurringTodo:
        db_todo = db.query(models.RecurringTodo)\
                    .filter(models.RecurringTodo.id == recurring_id)\
                    .filter(models.RecurringTodo.owner_id == user_id)\
                    .first()
        
        if not db_todo:
            raise HTTPException(status_code=404, detail="Tâche récurrente non trouvée")
        
        update_data = todo.dict(exclude_unset=True)
        
        if 'tag_ids' in update_data:
            tag_ids = update_data.pop('tag_ids')
            if tag_ids:
                tags = db.query(models.Tag).filter(models.Tag.id.in_(tag_ids)).all()
                db_todo.tags = tags
        
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        
        db.commit()
        db.refresh(db_todo)
        return db_todo

    @staticmethod
    def generate_todo(
        db: Session,
        recurring_id: int,
        user_id: int
    ) -> models.Todo:
        recurring = db.query(models.RecurringTodo)\
                     .filter(models.RecurringTodo.id == recurring_id)\
                     .filter(models.RecurringTodo.owner_id == user_id)\
                     .first()
        
        if not recurring:
            raise HTTPException(status_code=404, detail="Tâche récurrente non trouvée")
        
        # Calculer la prochaine date d'échéance
        if recurring.frequency == "daily":
            due_date = datetime.utcnow() + timedelta(days=1)
        elif recurring.frequency == "weekly":
            due_date = datetime.utcnow() + timedelta(weeks=1)
        elif recurring.frequency == "monthly":
            due_date = datetime.utcnow() + timedelta(days=30)
        
        # Créer la nouvelle tâche
        new_todo = models.Todo(
            title=recurring.title,
            description=recurring.description,
            owner_id=user_id,
            due_date=due_date,
            recurring_todo_id=recurring.id
        )
        
        # Copier les tags
        new_todo.tags = recurring.tags
        
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo

    @staticmethod
    def delete_recurring_todo(db: Session, recurring_id: int, user_id: int) -> bool:
        db_todo = db.query(models.RecurringTodo)\
                    .filter(models.RecurringTodo.id == recurring_id)\
                    .filter(models.RecurringTodo.owner_id == user_id)\
                    .first()
        
        if not db_todo:
            raise HTTPException(status_code=404, detail="Tâche récurrente non trouvée")
        
        # Désactiver plutôt que supprimer
        db_todo.active = False
        db.commit()
        return True