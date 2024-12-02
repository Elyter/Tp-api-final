from sqlalchemy.orm import Session
from app.models import models
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

def seed_database(db: Session):
    # Création d'utilisateurs
    users = [
        {
            "email": "test@test.fr",
            "password": "test"
        },
        {
            "email": "user2@test.fr",
            "password": "test"
        },
        {
            "email": "user3@test.fr",
            "password": "test"
        }
    ]

    db_users = []
    for user_data in users:
        db_user = models.User(
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"]),
            is_active=True
        )
        db.add(db_user)
        db_users.append(db_user)
    db.commit()

    # Création de tags
    tags = [
        {"name": "Personnel", "color": "#FF0000"},
        {"name": "Travail", "color": "#00FF00"},
        {"name": "Urgent", "color": "#FF6B6B"},
        {"name": "Important", "color": "#4ECDC4"},
        {"name": "Shopping", "color": "#45B7D1"},
        {"name": "Santé", "color": "#96CEB4"},
        {"name": "Loisirs", "color": "#FFEEAD"},
        {"name": "Famille", "color": "#D4A5A5"}
    ]

    db_tags = []
    for tag_data in tags:
        db_tag = models.Tag(**tag_data)
        db.add(db_tag)
        db_tags.append(db_tag)
    db.commit()

    # Création de tâches récurrentes
    recurring_todos = [
        {
            "title": "Réunion d'équipe",
            "description": "Réunion hebdomadaire avec l'équipe",
            "frequency": "weekly"
        },
        {
            "title": "Payer les factures",
            "description": "Vérifier et payer les factures mensuelles",
            "frequency": "monthly"
        },
        {
            "title": "Exercice physique",
            "description": "30 minutes de sport",
            "frequency": "daily"
        }
    ]

    for user in db_users:
        for recurring_data in recurring_todos:
            # Sélection aléatoire de tags (1 à 3 tags par tâche récurrente)
            selected_tags = random.sample(db_tags, random.randint(1, 3))
            
            db_recurring = models.RecurringTodo(
                title=recurring_data["title"],
                description=recurring_data["description"],
                frequency=recurring_data["frequency"],
                owner_id=user.id,
                active=True
            )
            db_recurring.tags.extend(selected_tags)
            db.add(db_recurring)
    db.commit()

    # Création de tâches normales
    todo_titles = [
        "Faire les courses", "Appeler le médecin", "Préparer la présentation",
        "Réviser le rapport", "Nettoyer la maison", "Répondre aux emails",
        "Faire une sauvegarde", "Organiser les fichiers", "Planifier les vacances",
        "Acheter un cadeau", "Réparer le vélo", "Lire un livre",
        "Apprendre Python", "Méditer", "Faire du yoga",
        "Jardiner", "Cuisiner", "Ranger le garage"
    ]

    priorities = [1, 2, 3]  # LOW, MEDIUM, HIGH
    
    for user in db_users:
        # Créer 20 tâches pour chaque utilisateur
        for _ in range(20):
            # Dates aléatoires sur les 30 prochains jours
            random_days = random.randint(-5, 30)
            due_date = datetime.utcnow() + timedelta(days=random_days)
            
            # Sélection aléatoire de tags (1 à 3 tags par tâche)
            selected_tags = random.sample(db_tags, random.randint(1, 3))
            
            todo = models.Todo(
                title=random.choice(todo_titles),
                description=f"Description de la tâche {random.randint(1, 1000)}",
                completed=random.choice([True, False]),
                due_date=due_date,
                priority=random.choice(priorities),
                owner_id=user.id
            )
            todo.tags.extend(selected_tags)
            db.add(todo)
    
    db.commit()

if __name__ == "__main__":
    from app.db.session import SessionLocal
    db = SessionLocal()
    seed_database(db)
    db.close() 