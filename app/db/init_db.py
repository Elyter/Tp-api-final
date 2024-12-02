from sqlalchemy import create_engine
from app.core.config import settings
from app.models.models import Base
from app.db.seed import seed_database
from app.db.session import SessionLocal

def init_db():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Remplir la base de données avec des données de test
    db = SessionLocal()
    seed_database(db)
    db.close()

if __name__ == "__main__":
    init_db()
