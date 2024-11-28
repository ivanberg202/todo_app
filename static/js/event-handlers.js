// event-handlers.js

import { updateTodoStatus, deleteTodo } from './api.js';
import { openTodoForm } from './todo-form.js';

export function addEventListeners(todosTableBody, token) {
    // Delegate 'change' events for checkboxes
    todosTableBody.addEventListener('change', async function (event) {
        if (event.target.classList.contains('todo-complete-checkbox')) {
            const checkbox = event.target;
            const todoId = checkbox.dataset.todoId;
            const completed = checkbox.checked;

            try {
                const response = await updateTodoStatus(todoId, completed, token);
                if (response.ok) {
                    const todoRow = checkbox.closest('tr');
                    if (completed) {
                        todoRow.classList.add('completed'); // Add the 'completed' class
                    } else {
                        todoRow.classList.remove('completed'); // Remove the 'completed' class
                    }
                } else {
                    console.error('Failed to update todo status.');
                }
            } catch (error) {
                console.error('Error updating todo status:', error);
            }
        }
    });

    // Delegate 'click' events for edit and delete buttons
    todosTableBody.addEventListener('click', function (event) {
        const target = event.target;

        if (target.classList.contains('edit-todo-button')) {
            const todoData = JSON.parse(target.dataset.todoData);
            openTodoForm(todoData, token);
        }

        if (target.classList.contains('delete-todo-button')) {
            const todoId = target.dataset.todoId;

            if (confirm('Are you sure you want to delete this todo?')) {
                deleteTodoItem(todoId, target, token);
            }
        }
    });
}

async function deleteTodoItem(todoId, buttonElement, token) {
    try {
        const response = await deleteTodo(todoId, token);
        if (response.ok) {
            // Remove the todo row from the UI
            const todoRow = buttonElement.closest('tr');
            todoRow.remove();
        } else {
            console.error('Failed to delete todo.');
        }
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}
