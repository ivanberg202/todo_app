// dom-utils.js

export function renderTodos(todosData, todosTableBody) {
    todosData.forEach(todo => {
        const row = document.createElement('tr');

        // Add 'completed' class if the todo is complete
        if (todo.complete) {
            row.classList.add('completed');
        }

        // Create the inner HTML for the row
        row.innerHTML = `
            <td>${todo.title}</td>
            <td>${todo.priority}</td>
            <td>${todo.description}</td>
            <td>
                <input type="checkbox" class="todo-complete-checkbox" data-todo-id="${todo.id}" ${todo.complete ? 'checked' : ''}>
            </td>
            <td>
                <button class="btn btn-sm btn-primary edit-todo-button" data-todo-id="${todo.id}" data-todo-data='${JSON.stringify(todo)}'>Edit</button>
                <button class="btn btn-sm btn-danger delete-todo-button" data-todo-id="${todo.id}">Delete</button>
            </td>
        `;

        // Append the row to the table body
        todosTableBody.appendChild(row);
    });
}
