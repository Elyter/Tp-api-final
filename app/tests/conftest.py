import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.test_config import test_settings
from app.db.base_class import Base
from app.main import app
from app.api.dependencies import get_db
from fastapi.testclient import TestClient

# Créer le moteur de base de données de test
engine = create_engine(test_settings.DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    # Créer la base de données de test
    Base.metadata.create_all(bind=engine)
    
    # Créer une session de test
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Nettoyer la base de données après les tests
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(db):
    # Override la dépendance de base de données
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client 