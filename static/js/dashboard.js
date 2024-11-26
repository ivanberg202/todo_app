import { fetchTodos } from './api.js';
import { openTodoForm } from './todo-form.js';
import { addEventListeners } from './event-handlers.js';
import { renderTodos } from './dom-utils.js';  // Import the render function

document.addEventListener("DOMContentLoaded", async function () {
    // Main entry point logic for dashboard
    const token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "/auth/login-page";
        return;
    }

    const addTodoButton = document.createElement('button');
    addTodoButton.textContent = "Add a Todo";
    addTodoButton.classList.add('btn', 'btn-primary', 'mb-3');
    addTodoButton.style.position = 'absolute';
    addTodoButton.style.top = '10px';
    addTodoButton.style.right = '10px';
    document.body.appendChild(addTodoButton);

    addTodoButton.addEventListener('click', function () {
        openTodoForm(null, token);
    });

    try {
        const todosResponse = await fetchTodos(token);
        if (todosResponse.ok) {
            const todosData = await todosResponse.json();
            const todosTableBody = document.getElementById("todos-table-body");
            todosTableBody.innerHTML = ""; // Clear previous content

            // Render todos and add event listeners...
            renderTodos(todosData, todosTableBody);  // Render todos into the table
            addEventListeners(todosTableBody, token); // Add event listeners after rendering todos
        } else {
            console.error("Failed to fetch todos data.");
        }
    } catch (error) {
        console.error("Error loading todos:", error);
    }
});
