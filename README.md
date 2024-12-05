
# API de Gestion de Tâches (Todo API)

Une API REST moderne et robuste pour la gestion de tâches, construite avec FastAPI et PostgreSQL.

## Fonctionnalités

- 🔐 Authentification JWT
- ✅ Gestion complète des tâches (CRUD)
- 🏷️ Système de tags
- 🔄 Tâches récurrentes
- 🔍 Recherche et filtrage avancés
- 📊 Priorisation des tâches
- 📅 Gestion des dates d'échéance

## Prérequis

- Docker et Docker Compose
- Python 3.11+
- PostgreSQL 13+

## Installation

1. Clonez le dépôt :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_PROJET]
```

2. Créez un fichier `.env` à la racine du projet :
```bash
DATABASE_URL=postgresql://postgres:password@db:5432/todos
SECRET_KEY=votre_clé_secrète_ici
```

3. Lancez l'application avec Docker Compose :
```bash
docker-compose up -d
```


L'API sera accessible à l'adresse : http://localhost:8000

## Documentation API

La documentation Swagger UI est disponible à : http://localhost:8000/docs

## Points d'Accès Principaux

### Authentification
- POST `/api/v1/register` - Inscription
- POST `/api/v1/login` - Connexion
- GET `/api/v1/me` - Profil utilisateur

### Tâches
- GET `/api/v1/todos` - Liste des tâches
- POST `/api/v1/todos` - Création d'une tâche
- GET `/api/v1/todos/{id}` - Détails d'une tâche
- PUT `/api/v1/todos/{id}` - Modification d'une tâche
- DELETE `/api/v1/todos/{id}` - Suppression d'une tâche
- GET `/api/v1/todos/search` - Recherche de tâches

### Tags
- GET `/api/v1/tags` - Liste des tags
- POST `/api/v1/tags` - Création d'un tag
- PUT `/api/v1/tags/{id}` - Modification d'un tag
- DELETE `/api/v1/tags/{id}` - Suppression d'un tag

### Tâches Récurrentes
- GET `/api/v1/recurring` - Liste des tâches récurrentes
- POST `/api/v1/recurring` - Création d'une tâche récurrente
- PUT `/api/v1/recurring/{id}` - Modification d'une tâche récurrente
- DELETE `/api/v1/recurring/{id}` - Suppression d'une tâche récurrente
- POST `/api/v1/recurring/{id}/generate` - Génération d'une instance

## Tests

Pour exécuter les tests :
```bash
./run_tests.sh
```

## Structure du Projet
.
├── app/
│ ├── alembic/ # Migrations de base de données
│ ├── api/ # Points d'accès API
│ ├── core/ # Configuration et utilitaires
│ ├── db/ # Configuration base de données
│ ├── models/ # Modèles SQLAlchemy
│ ├── schemas/ # Schémas Pydantic
│ ├── services/ # Logique métier
│ └── tests/ # Tests
├── docker-compose.yml
├── Dockerfile
└── requirements.txt


## Technologies Utilisées

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic
- JWT
- Docker

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou soumettre une pull request.

## Licence

MIT