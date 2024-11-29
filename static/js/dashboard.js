import { fetchTodos } from './api.js';
import { openTodoForm } from './todo-form.js';
import { addEventListeners } from './event-handlers.js';
import { renderTodos } from './dom-utils.js';
import { openUserDetailsForm, getCurrentUserRole } from './user_details.js';

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
                // Fetch the current user's role
                console.log("Fetching role for user...");
                const currentUserRole = await getCurrentUserRole(token);

                // Fetch the user details
                const response = await fetch('/auth/me', {
                    method: 'GET',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const userData = await response.json();
                    console.log('Fetched user data:', userData);
                    openUserDetailsForm(userData, token, currentUserRole); // Pass user data and role to the modal
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

    // Logout functionality
    document.querySelector(".nav-link[href='/auth/logout']").addEventListener("click", (event) => {
        event.preventDefault(); // Prevent the default link navigation
        localStorage.removeItem("access_token"); // Clear the token from local storage
        alert("You have been logged out.");
        window.location.href = "/auth/login-page"; // Redirect to login page
    });
});
