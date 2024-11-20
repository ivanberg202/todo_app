import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import status, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timezone
from unittest.mock import MagicMock

# Import app and database-related components
from todoapp3.main import app
from todoapp3.database import Base
from todoapp3.models import Todos, Users, PhoneNumberHistory

# Set up bcrypt context for hashing passwords
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Set up a test database using SQLite with StaticPool for in-memory persistence during the test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override for the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override OAuth2PasswordBearer to bypass token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def override_oauth2_scheme():
    return "mock_token"


# Override get_current_user to return a mock user
async def override_get_current_user(request: Request):
    # Manually check for the Authorization header
    token = request.headers.get("Authorization")

    # Debugging token
    print("Debug: Token received in override_get_current_user:", token)

    # Check if the token is missing or invalid
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed",
        )

    # Mock successful authentication
    print("Mock get_current_user called")
    return {"username": "testuser", "id": 1, "user_role": "admin"}


# Set up the testing client
client = TestClient(app)

# Mock Users for testing scenarios
admin_user = {
    "user_role": "admin",
    "id": 1,
    "username": "admin_user"
}

non_admin_user = {
    "user_role": "user",
    "id": 2,
    "username": "regular_user"
}

# Sample user update data for testing
user_update_data = {
    "username": "new_username",
    "email": "new_email@example.com",
    "first_name": "UpdatedFirstName",
    "last_name": "UpdatedLastName",
    "role": "user",
    "phone_number": "1234567890"
}


# Create the database schema before any tests are run
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Fixture to create a sample Todo in the test database
@pytest.fixture
def test_todo():
    with TestingSessionLocal() as db:
        todo = Todos(title="Test Todo", description="Test Description", priority=1, complete=False, owner_id=1)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo


# Fixture to create a sample user in the test database
@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    try:
        hashed_password = bcrypt_context.hash("testpassword")
        user = Users(
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            hashed_password=hashed_password,
            role="user",
            phone_number="123456789",
            phone_number_last_changed=datetime.now(timezone.utc),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        yield user  # Yield instead of return to keep the session open during the test
    finally:
        db.close()


@pytest.fixture
def test_phone_history(test_user):
    # Add phone number history to the user
    with TestingSessionLocal() as db:
        phone_number_history = PhoneNumberHistory(
            phone_number=test_user.phone_number,
            changed_at=test_user.phone_number_last_changed,
            user_id=test_user.id
        )
        db.add(phone_number_history)
        db.commit()
        db.refresh(phone_number_history)

        return phone_number_history



# Helper functions to simulate current user
def get_admin_user():
    return admin_user


def get_non_admin_user():
    return non_admin_user
