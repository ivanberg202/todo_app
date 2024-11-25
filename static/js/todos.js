export function fetchTodos() {
    const jwtToken = getJwtToken();

    if (!jwtToken) {
        handleSessionExpired();
        return;
    }

    $.ajax({
        url: "/todos/",
        type: "GET",
        headers: {
            "Authorization": "Bearer " + jwtToken
        },
        success: function(response) {
            const todoList = $("#todoList");
            todoList.empty(); // Clear the existing list
            response.forEach(todo => {
                addTodoToDOM(todo);
            });
        },
        error: function(xhr) {
            if (xhr.status === 401) {
                handleSessionExpired();
            } else {
                alert("Error fetching TODOs: " + xhr.responseText);
            }
        }
    });
}

export function handleDeleteTodoButton(todoId) {
    const userConfirmed = confirm("Are you sure you want to delete this TODO?");
    if (userConfirmed) {
        $.ajax({
            url: `/todos/todo/${todoId}`,
            type: "DELETE",
            headers: {
                "Authorization": "Bearer " + getJwtToken()
            },
            success: function() {
                removeTodoFromDOM(todoId);
            },
            error: function(xhr) {
                if (xhr.status === 401) {
                    alert("Session expired. Please log in again.");
                } else {
                    alert("Error deleting TODO: " + xhr.responseText);
                }
            }
        });
    }
}
