import { fetchTodos } from './api.js';
import { openTodoForm } from './todo-form.js';
import { addEventListeners } from './event-handlers.js';
import { renderTodos } from './dom-utils.js';
import { openUserDetailsForm } from './user_details.js';


document.addEventListener("DOMContentLoaded", async function () {
    // Ensure user is authenticated
    const token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "/auth/login-page";
        return;
    }

    // Add event listener for the user profile button
    const userProfileButton = document.getElementById('userProfileButton');
    if (userProfileButton) {
        userProfileButton.addEventListener('click', async () => {
            try {
                const response = await fetch('/auth/me', {
                    method: 'GET',
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    const userData = await response.json();
                    openUserDetailsForm(userData, token); // Open modal with user data
                } else {
                    console.error('Failed to fetch user details');
                }
            } catch (error) {
                console.error('Error fetching user details:', error);
            }
        });
    }

    // Bind event listener to the "Add a Todo" button
    const addTodoButton = document.getElementById('addTodoButton');
    if (addTodoButton) {
        addTodoButton.addEventListener('click', function () {
            openTodoForm(null, token);
        });
    }

    // Fetch and render todos
    try {
        const todosResponse = await fetchTodos(token);
        if (todosResponse.ok) {
            const todosData = await todosResponse.json();
            const todosTableBody = document.getElementById("todos-table-body");
            todosTableBody.innerHTML = ""; // Clear previous content

            // Render todos and add event listeners
            renderTodos(todosData, todosTableBody);
            addEventListeners(todosTableBody, token);
        } else {
            console.error("Failed to fetch todos data.");
        }
    } catch (error) {
        console.error("Error loading todos:", error);
    }
});

document.querySelector(".nav-link[href='/auth/logout']").addEventListener("click", (event) => {
    event.preventDefault(); // Prevent the default link navigation
    localStorage.removeItem("access_token"); // Clear the token from local storage
    alert("You have been logged out.");
    window.location.href = "/auth/login-page"; // Redirect to login page
});
