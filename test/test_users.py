from todoapp3.database import get_db
from todoapp3.routers.auth import get_current_user
from .utils import *  # Assuming reusable functions and fixtures are in utils.py

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Update the dependency override to use the new implementation
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[oauth2_scheme] = override_oauth2_scheme

client = TestClient(app)

# Test function for get_user endpoint
def test_get_user(test_user):
    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a GET request to the user endpoint
    response = client.get("/user/", headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == test_user.username
    assert response.json()["phone_number"] == test_user.phone_number


# Test function for change_password endpoint
def test_change_password_success(test_user):
    # Prepare the password change request data
    password_data = {
        "password": "testpassword",
        "new_password": "newpassword123"
    }

    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a PUT request to change the password
    response = client.put("/user/password", json=password_data, headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the password has been updated
    with TestingSessionLocal() as db:
        updated_user = db.query(Users).filter(Users.id == test_user.id).first()
        assert bcrypt_context.verify("newpassword123", updated_user.hashed_password)


# Test function for changing password with incorrect current password
def test_change_password_incorrect(test_user):
    # Prepare the incorrect password change request data
    password_data = {
        "password": "wrongpassword",
        "new_password": "newpassword123"
    }

    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a PUT request to change the password
    response = client.put("/user/password", json=password_data, headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Error on password change"


# Test function for get_phone_number_history endpoint
def test_get_phone_number_history(test_user):
    # Add phone number history for the user
    with TestingSessionLocal() as db:
        phone_history = PhoneNumberHistory(
            user_id=test_user.id,
            phone_number="123456789",
            changed_at=datetime.now(timezone.utc)
        )
        db.add(phone_history)
        db.commit()

    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a GET request to the phone number history endpoint
    response = client.get("/user/phone_number/history", headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["phone_number"] == "123456789"



# Test function for updating phone number
def test_update_phone_number(test_user):
    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a PUT request to update the phone number, passing the new phone number as a query parameter
    response = client.put("/user/phone_number?new_phone_number=987654321", headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_200_OK

    # Verify the updated phone number in the database
    with TestingSessionLocal() as db:
        user_in_db = db.query(Users).filter(Users.id == test_user.id).first()
        assert user_in_db is not None
        assert user_in_db.phone_number == "987654321"


# Test function for updating phone number when user not found
def test_update_phone_number_user_not_found():
    # Override get_current_user to simulate a non-existent user
    async def override_get_current_user_not_found(request: Request):
        # Return a user ID that does not exist in the database
        return {"username": "nonexistentuser", "id": 9999, "user_role": "user"}

    # Apply the dependency override
    app.dependency_overrides[get_current_user] = override_get_current_user_not_found

    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a PUT request to update the phone number for a non-existent user
    response = client.put("/user/phone_number?new_phone_number=987654321", headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"

    # Reset the dependency override
    app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.parametrize("test_user_data, user_update_data, user_identifier, expected_status, expected_message", [
    # Admin updating another user's details
    (get_admin_user(), {"username": "new_username"}, "existing_user", 200, "User details updated successfully"),
    # Admin trying to update without providing user_identifier
    (get_admin_user(), {"username": "new_username"}, None, 400, "Admin must provide a username or email to update a user."),
    # Non-admin attempting to update another user's details
    (get_non_admin_user(), {"username": "new_username"}, "existing_user", 403, "Non-admin users cannot specify another user."),
    # Non-admin updating their own details
    (get_non_admin_user(), {"username": "new_username"}, None, 200, "User details updated successfully"),
    # Duplicate username
    (get_non_admin_user(), {"username": "existing_user"}, None, 400, "Username is already in use by another account"),
    # Non-admin trying to change role
    (get_non_admin_user(), {"role": "admin"}, None, 403, "Only admins can change the role")
])
def test_update_user_details(mock_get_db, test_user_data, user_update_data, user_identifier, expected_status, expected_message):
    # Apply dependency overrides
    app.dependency_overrides[get_db] = lambda: mock_get_db
    app.dependency_overrides[get_current_user] = lambda: test_user_data

    # Prepare the request parameters
    params = {}
    if user_identifier:
        params["user_identifier"] = user_identifier

    try:
        # Make the PUT request to update user details
        response = client.put("/user/update_details", params=params, json=user_update_data)

        # Print the response details for debugging
        print("Response status:", response.status_code)
        print("Response body:", response.json())

        # Assert response status and message
        assert response.status_code == expected_status, f"Expected status {expected_status} but got {response.status_code}."
        if response.status_code == 200:
            assert response.json()["message"] == expected_message, f"Unexpected message: {response.json().get('message')}"
        else:
            assert response.json()["detail"] == expected_message, f"Unexpected detail message: {response.json().get('detail')}"
    finally:
        # Ensure dependency overrides are removed
        app.dependency_overrides = {}


@pytest.fixture
def mock_get_db():
    db = MagicMock()

    # Set up existing users to simulate the database state
    existing_user = Users(
        id=4,
        username="existing_user",
        email="existing_email@example.com",
        first_name="OldFirstName",
        last_name="OldLastName",
        role="user",
        phone_number="9876543210"
    )

    duplicate_user = Users(
        id=5,
        username="existing_user",
        email="duplicate_email@example.com",
        first_name="DuplicateFirstName",
        last_name="DuplicateLastName",
        role="user",
        phone_number="1234567890"
    )

    # Mock the query() behavior to properly differentiate scenarios
    def query_side_effect(model):
        query_mock = MagicMock()
        if model == Users:
            def filter_side_effect(*args, **kwargs):
                # Simulate different scenarios for the uniqueness check and user retrieval
                if "username" in str(args) and "existing_user" in str(args):
                    # If checking for a duplicate username, return the duplicate user
                    return MagicMock(first=lambda: duplicate_user)
                elif "id" in str(args) or "username" not in str(args):
                    # If retrieving by ID or for a valid existing user, return the existing user
                    return MagicMock(first=lambda: existing_user)
                else:
                    # Otherwise, return None to simulate no match found
                    return MagicMock(first=lambda: None)
            query_mock.filter.side_effect = filter_side_effect
        return query_mock

    db.query.side_effect = query_side_effect

    yield db
