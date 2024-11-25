import { updateTodoStatus, deleteTodo } from './api.js';
import { openTodoForm } from './todo-form.js';

export function addEventListeners(todosTableBody, token) {
    // Add event listeners to checkboxes
    todosTableBody.querySelectorAll('.todo-completed-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', async function (event) {
            // Handle checkbox change...
            const tr = event.target.closest('tr');
            const todoId = tr.getAttribute('data-todo-id');
            const completed = event.target.checked;
            await updateTodoStatus(todoId, completed, token);
        });
    });

    // Add event listeners to edit icons
    todosTableBody.querySelectorAll('.edit-todo-icon').forEach(icon => {
        icon.addEventListener('click', function () {
            const tr = icon.closest('tr');
            const todoId = tr.getAttribute('data-todo-id');
            const todo = {
                id: todoId,
                title: tr.querySelector('.todo-title').textContent,
                priority: tr.querySelector('.todo-priority').textContent,
                description: tr.querySelector('.todo-description').textContent,
            };
            openTodoForm(todo, token);
        });
    });

    // Add event listeners to delete icons
    todosTableBody.querySelectorAll('.delete-todo-icon').forEach(icon => {
        icon.addEventListener('click', async function () {
            const tr = icon.closest('tr');
            const todoId = tr.getAttribute('data-todo-id');
            if (confirm("Are you sure you want to delete this todo?")) {
                await deleteTodo(todoId, token);
                tr.remove();
            }
        });
    });
}
