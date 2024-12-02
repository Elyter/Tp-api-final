from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import auth, todos, tags, recurring
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base

# Configuration de la base de données
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables au démarrage
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()  # Initialiser la base de données

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(
    auth.router,
    prefix=settings.API_V1_STR,
    tags=["auth"]
)
app.include_router(
    todos.router,
    prefix=f"{settings.API_V1_STR}/todos",
    tags=["todos"]
)
app.include_router(
    tags.router,
    prefix=f"{settings.API_V1_STR}/tags",
    tags=["tags"]
)
app.include_router(
    recurring.router,
    prefix=f"{settings.API_V1_STR}/recurring",
    tags=["recurring"]
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}