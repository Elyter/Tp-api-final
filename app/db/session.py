from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Création du moteur SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Création de la classe SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 