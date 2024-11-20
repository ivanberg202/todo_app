from todoapp3.database import get_db
from todoapp3.routers.auth import get_current_user

# Import overrides from utils.py
from .utils import *


# Update the dependency override to use the new implementation
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db
# Use app.dependency_overrides to mock the OAuth2 scheme
app.dependency_overrides[oauth2_scheme] = override_oauth2_scheme


# Test function for async def read_all
def test_read_all_todos(test_todo):
    # Make a request to the endpoint
    headers = {"Authorization": "Bearer mock_token"}
    print("Before client request")
    response = client.get("todos/", headers=headers)  # Adjust the route if necessary
    print("After client request")
    print("Response JSON:", response.json())

    # Assert the response
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Todo"
    assert response.json()[0]["description"] == "Test Description"
    assert response.json()[0]["priority"] == 1
    assert response.json()[0]["complete"] is False


# Test functions for async def read_todo
def test_read_todo_success(test_todo):
    # Make a request to the endpoint to read the created todo
    headers = {"Authorization": "Bearer mock_token"}
    response = client.get(f"todos/todo/{test_todo.id}", headers=headers)

    # Assert the response
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == test_todo.title
    assert response.json()["description"] == test_todo.description
    assert response.json()["priority"] == test_todo.priority
    assert response.json()["complete"] == test_todo.complete

def test_read_todo_not_found():
    # Make a request to the endpoint with a non-existent todo_id
    headers = {"Authorization": "Bearer mock_token"}
    response = client.get("todos/todo/9999", headers=headers)  # Assume 9999 does not exist

    # Assert the response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Todo not found."

def test_read_todo_unauthorized(test_todo):
    # Make a request to the endpoint without valid authentication headers
    response = client.get(f"todos/todo/{test_todo.id}")

    # Assert the response
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Authentication Failed"

# Test function for async def create_todo
def test_create_todo():
    # Prepare the request data for the todo item
    todo_data = {
        "title": "New Test Todo",
        "description": "This is a test todo item",
        "priority": 3,
        "complete": False
    }

    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a POST request to create a new todo item
    response = client.post("todos/todo", json=todo_data, headers=headers)

    # Assert that the response status code is 201 Created
    assert response.status_code == status.HTTP_201_CREATED

    # Verify that the todo has been added to the database by fetching it from the test database
    with TestingSessionLocal() as db:
        todo_in_db = db.query(Todos).filter(Todos.title == todo_data["title"]).first()
        assert todo_in_db is not None
        assert todo_in_db.description == todo_data["description"]
        assert todo_in_db.priority == todo_data["priority"]
        assert todo_in_db.complete == todo_data["complete"]

# Test function for async def update_todo
def test_update_todo_success(test_todo):
    # Prepare the updated data for the todo item
    updated_data = {
        "title": "Updated Test Todo",
        "description": "This is an updated description",
        "priority": 4,
        "complete": True
    }

    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a PUT request to update the todo item
    response = client.put(f"todos/todo/{test_todo.id}", json=updated_data, headers=headers)

    # Assert that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verify that the todo has been updated in the database by fetching it from the test database
    with TestingSessionLocal() as db:
        todo_in_db = db.query(Todos).filter(Todos.id == test_todo.id).first()
        assert todo_in_db is not None
        assert todo_in_db.title == updated_data["title"]
        assert todo_in_db.description == updated_data["description"]
        assert todo_in_db.priority == updated_data["priority"]
        assert todo_in_db.complete == updated_data["complete"]

# could add "not found" variation of the update todo function

# test functions for async def delete_todo
# Test function to delete an existing todo
def test_delete_todo_success(test_todo):
    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a DELETE request to remove the todo item
    response = client.delete(f"todos/todo/{test_todo.id}", headers=headers)

    # Assert that the response status code is 204 No Content
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the todo is removed from the database
    with TestingSessionLocal() as db:
        todo_in_db = db.query(Todos).filter(Todos.id == test_todo.id).first()
        assert todo_in_db is None


# Test function for deleting a non-existent todo
def test_delete_todo_not_found():
    # Set up the Authorization header to simulate an authenticated user
    headers = {"Authorization": "Bearer mock_token"}

    # Make a DELETE request to a non-existent todo_id
    response = client.delete("todos/todo/9999", headers=headers)  # Assume 9999 does not exist

    # Assert that the response status code is 404 Not Found
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Todo not found."


# Test function to delete a todo without proper authorization
def test_delete_todo_unauthorized(test_todo):
    # Make a DELETE request to remove the todo item without valid authentication headers
    response = client.delete(f"todos/todo/{test_todo.id}")

    # Assert the response for unauthorized access
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Authentication Failed"
