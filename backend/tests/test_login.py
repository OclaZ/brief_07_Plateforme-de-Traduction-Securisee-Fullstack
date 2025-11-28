import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from core.database import get_db
from models.users import User, Base
from passlib.context import CryptContext

# Configuration de la base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Override de la dépendance get_db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Crée les tables avant chaque test et les supprime après"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Crée un utilisateur de test dans la base de données"""
    db = TestingSessionLocal()
    
    hashed_password = pwd_context.hash("testpassword123")
    user = User(
        username="testuser",
        hashed_password=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    
    return {
        "username": "testuser",
        "password": "testpassword123"
    }

def test_login(test_user):
    """Test de connexion avec des identifiants valides"""
    response = client.post(
        "/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_protected_route_without_token():
    """Test d'accès à une route protégée sans token"""
    response = client.post(
        "/translate",
        json={
            "text": "Hello world",
            "direction": "en_fr"
        }
    )
    
    # Vérifie qu'on obtient une erreur d'authentification (403 ou 401)
    assert response.status_code in [401, 403]
    assert "detail" in response.json()