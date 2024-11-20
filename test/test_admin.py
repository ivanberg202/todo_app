from todoapp3.database import get_db
from todoapp3.routers.auth import get_current_user

# Import overrides from utils.py
from .utils import *


# Update the dependency override to use the new implementation
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db
# Use app.dependency_overrides to mock the OAuth2 scheme
app.dependency_overrides[oauth2_scheme] = override_oauth2_scheme


# Test function to read all todos as admin
def test_admin_read_all_todos(test_todo):
    # Set up the Authorization header to simulate an authenticated admin user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a GET request to the admin endpoint to read all todos
    response = client.get("/admin/todo", headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == test_todo.title
    assert response.json()[0]["description"] == test_todo.description
    assert response.json()[0]["priority"] == test_todo.priority
    assert response.json()[0]["complete"] == test_todo.complete


# Test function for reading all todos with non-admin user
def test_admin_read_all_todos_non_admin():
    # Override get_current_user to simulate a non-admin user
    async def override_get_current_user_non_admin(request: Request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed",
            )
        # Mock non-admin user
        return {"username": "testuser", "id": 1, "user_role": "user"}

    app.dependency_overrides[get_current_user] = override_get_current_user_non_admin

    # Set up the Authorization header to simulate an authenticated non-admin user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a GET request to the admin endpoint to read all todos
    response = client.get("/admin/todo", headers=headers)

    # Assert the response for unauthorized access
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Authentication Failed"

    # Reset the get_current_user dependency override back to admin
    app.dependency_overrides[get_current_user] = override_get_current_user

# Test function to delete a specific todo as admin
def test_admin_delete_todo_success(test_todo):
    # Set up the Authorization header to simulate an authenticated admin user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a DELETE request to remove the todo item
    response = client.delete(f"/admin/todo/{test_todo.id}", headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the todo is removed from the database
    with TestingSessionLocal() as db:
        todo_in_db = db.query(Todos).filter(Todos.id == test_todo.id).first()
        assert todo_in_db is None

# Test function to delete a specific todo as non-admin user
def test_admin_delete_todo_non_admin(test_todo):
    # Override get_current_user to simulate a non-admin user
    async def override_get_current_user_non_admin(request: Request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed",
            )
        # Mock non-admin user
        return {"username": "testuser", "id": 1, "user_role": "user"}

    app.dependency_overrides[get_current_user] = override_get_current_user_non_admin

    # Set up the Authorization header to simulate an authenticated non-admin user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a DELETE request to remove the todo item
    response = client.delete(f"/admin/todo/{test_todo.id}", headers=headers)

    # Assert the response for unauthorized access
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Authentication Failed"

    # Reset the get_current_user dependency override back to admin
    app.dependency_overrides[get_current_user] = override_get_current_user

# Test function to delete a non-existent todo as admin
def test_admin_delete_todo_not_found():
    # Set up the Authorization header to simulate an authenticated admin user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a DELETE request to a non-existent todo_id
    response = client.delete("/admin/todo/9999", headers=headers)  # Assume 9999 does not exist

    # Assert the response for not found
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Todo not found."
