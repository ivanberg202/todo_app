import pytest
from datetime import timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from .utils import test_user, client, setup_database, TestingSessionLocal
from todoapp3.routers.auth import authenticate_user, create_access_token, get_current_user, SECRET_KEY, ALGORITHM
import pytest_asyncio

# Use the imported setup_database fixture
@pytest.fixture(autouse=True)
def setup_database_auto(setup_database):
    yield


def test_create_user():
    # Define the payload for user creation
    payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "newpassword",
        "role": "user",
        "phone_number": "987654321"
    }
    response = client.post("/auth/register", data=payload)
    # Assert status code for successful creation
    assert response.status_code == 201

def test_create_user_missing_fields():
    # Define a payload with missing required fields
    response = client.post(
        "/auth/register",
        json={
            "username": "incompleteuser",
            "email": "incompleteuser@example.com"
        }
    )
    # Assert that the request fails due to missing required fields
    assert response.status_code == 422

def test_login_for_access_token(test_user):
    response = client.post("/auth/login", data={"username": test_user.username, "password": "testpassword"})
    # Assert the login is successful and returns a valid access token
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post("/auth/login", data={"username": "nonexistent", "password": "wrongpassword"})
    # Assert the login fails due to invalid credentials
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate user."

def test_login_with_incorrect_password(test_user):
    response = client.post("/auth/login", data={"username": test_user.username, "password": "wrongpassword"})
    # Assert that the login fails due to incorrect password
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate user."

def test_authenticate_user(test_user):
    # Use the TestingSessionLocal to create a new session
    db = TestingSessionLocal()
    try:
        # Test with correct credentials
        authenticated_user = authenticate_user(test_user.username, "testpassword", db)
        assert authenticated_user is not False
        assert authenticated_user.username == test_user.username

        # Test with incorrect password
        incorrect_password_user = authenticate_user(test_user.username, "wrongpassword", db)
        assert incorrect_password_user is False

        # Test with non-existent username
        non_existent_user = authenticate_user("nonexistentuser", "somepassword", db)
        assert non_existent_user is False
    finally:
        db.close()


def test_create_access_token():
    # Test creating an access token
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(minutes=15)
    token = create_access_token(username, user_id, role, expires_delta)

    # Decode the token to verify its content
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role
    assert "exp" in decoded_token


@pytest_asyncio.fixture
async def test_get_current_user():
    # Test extracting user from a valid token
    username = "testuser"
    user_id = 1
    role = "user"
    expires_delta = timedelta(minutes=15)
    token = create_access_token(username, user_id, role, expires_delta)
    try:
        current_user = await get_current_user(token)
        assert current_user["username"] == username
        assert current_user["id"] == user_id
        assert current_user["user_role"] == role
    except JWTError:
        pytest.fail("get_current_user raised an unexpected JWTError")

    # Test with an invalid token
    invalid_token = "invalidtoken"
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(invalid_token)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate user."