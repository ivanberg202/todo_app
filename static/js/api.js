// api.js
export async function fetchTodos(token) {
    return fetch("/todos/", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
}

export async function updateTodoStatus(todoId, completed, token) {
    return fetch(`/todos/todo/${todoId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ complete: completed })
    });
}

export async function addOrUpdateTodo(todoData, todoId, method, token) {
    const url = todoId ? `/todos/todo/${todoId}` : `/todos/todo`;
    return fetch(url, {
        method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(todoData)
    });
}

export async function deleteTodo(todoId, token) {
    return fetch(`/todos/todo/${todoId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
}
