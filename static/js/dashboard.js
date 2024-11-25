// dashboard.js
console.log("dashboard.js loaded successfully");

document.addEventListener("DOMContentLoaded", async function () {
    // Check if we're on the dashboard page
    console.log("Current path:", window.location.pathname);
    if (window.location.pathname !== "/auth/dashboard") {
        console.log("Not on the dashboard page, skipping dashboard loading script.");
        return;
    }

    // Fetch the token from localStorage
    const token = localStorage.getItem("access_token");
    console.log("Token retrieved from localStorage:", token);

    // If no token is found, redirect to login page
    if (!token) {
        console.error("No token found, redirecting to login...");
        window.location.href = "/auth/login-page";
        return;
    }

    try {
        // Now, fetch the todos for the user
        console.log("Making fetch request to /todos with token.");
        const todosResponse = await fetch("/todos/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        console.log("Todos fetch request complete. Response status:", todosResponse.status);

        if (todosResponse.ok) {
            const todosData = await todosResponse.json();
            console.log("Todos data:", todosData);

            // Find the todos table body and populate it
            const todosTableBody = document.getElementById("todos-table-body");
            todosTableBody.innerHTML = ""; // Clear any previous content

            if (todosData.length === 0) {
                todosTableBody.innerHTML = `<tr><td colspan="5" class="text-center">You have no todos.</td></tr>`;
            } else {
                todosData.forEach(todo => {
                    const tr = document.createElement("tr");
                    tr.setAttribute("data-todo-id", todo.id); // Set todo ID for reference

                    tr.innerHTML = `
                        <td class="todo-title ${todo.complete ? 'completed' : ''}">${todo.title}</td>
                        <td>${todo.priority}</td>
                        <td>${todo.description}</td>
                        <td><input type="checkbox" class="todo-completed-checkbox" ${todo.complete ? "checked" : ""}></td>
                    `;
                    todosTableBody.appendChild(tr);
                });
            }

            // Add event listeners to checkboxes
            document.querySelectorAll('.todo-completed-checkbox').forEach(checkbox => {
                checkbox.addEventListener('change', async function (event) {
                    const tr = event.target.closest('tr');
                    if (!tr) {
                        console.error("Table row not found");
                        return;
                    }

                    const todoId = tr.getAttribute('data-todo-id');
                    if (!todoId) {
                        console.error("Todo ID not found on the row");
                        return;
                    }

                    console.log(`Attempting to update todo with ID: ${todoId}`);

                    const completed = event.target.checked;

                    // Update the visual representation
                    const cells = tr.querySelectorAll('.todo-title, .todo-priority, .todo-description');

                    if (cells.length > 0) {
                        cells.forEach(cell => {
                            if (completed) {
                                cell.classList.add('text-decoration-line-through', 'text-muted');
                            } else {
                                cell.classList.remove('text-decoration-line-through', 'text-muted');
                            }
                        });
                    } else {
                        console.error("No cells found for todo ID:", todoId);
                    }

                    // Construct the URL for updating the todo
                    const updateUrl = `/todos/todo/${todoId}`;
                    console.log(`Update URL: ${updateUrl}`);

                    // Send update request to server
                    try {
                        const updateResponse = await fetch(updateUrl, {
                            method: "PUT",
                            headers: {
                                "Content-Type": "application/json",
                                "Authorization": `Bearer ${token}`
                            },
                            body: JSON.stringify({ complete: completed })
                        });

                        if (!updateResponse.ok) {
                            console.error(`Failed to update todo status. Status code: ${updateResponse.status}`);
                            // Optionally revert checkbox if update fails
                            event.target.checked = !completed;
                        } else {
                            console.log(`Todo ${todoId} updated successfully.`);
                        }
                    } catch (error) {
                        console.error(`Error updating todo status: ${error}`);
                        // Optionally revert checkbox if there's an error
                        event.target.checked = !completed;
                    }
                });
            });
        } else {
            console.error("Failed to fetch todos data. Status code:", todosResponse.status);
            const todosTableBody = document.getElementById("todos-table-body");
            todosTableBody.innerHTML = `<tr><td colspan="5" class="text-center">Failed to load your todos. Please try again later.</td></tr>`;
        }

    } catch (error) {
        console.error("Error loading todos:", error);
        window.location.href = "/auth/login-page";
    }
});
