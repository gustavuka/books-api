import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.security import create_access_token, get_password_hash
from app.database.database import Base, get_db
from app.main import app
from app.models.user import User
from app.schemas.token import TokenData

# Create a test database engine
engine = create_engine("sqlite:///./test.db")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def clear_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Clear all tables after test
    yield
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f"DELETE FROM {table.name}"))
            conn.commit()


@pytest.fixture(scope="function")
def db_session(clear_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a test user and return it"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def client(clear_db):
    # Override the database dependency
    app.dependency_overrides[get_db] = test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
