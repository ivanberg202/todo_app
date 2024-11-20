$(document).ready(function() {
    // Fetch user details and TODOs when the document is ready
    fetchUserDetails();
    fetchTodos();

    function fetchUserDetails() {
    console.log("Fetching user details..."); // Debugging statement
    $.ajax({
        url: "/auth/me",
        type: "GET",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("jwt_token")
        },
        success: function(response) {
            console.log("User details fetched successfully:", response); // Debugging statement
            // Use first_name if it exists, otherwise use username
            const displayName = response.first_name ? response.first_name : response.username;
            $("#todosHeading").text(`${displayName}'s TODOs`);
        },
        error: function(xhr) {
            console.error("Error fetching user details:", xhr); // Debugging statement
            if (xhr.status === 401) {
                $("#todosHeading").text('Session expired. Please log in again.');
            } else {
                $("#todosHeading").text('Error fetching user details.');
            }
        }
    });
}


    // Function to fetch todos and display them in the DOM
    function fetchTodos() {
        $.ajax({
            url: "/todos/",
            type: "GET",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("jwt_token")
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
                    alert("Session expired. Please log in again.");
                } else {
                    alert("Error fetching TODOs: " + xhr.responseText);
                }
            }
        });
    }

    // Show Create TODO Modal
    $("#createTodoButton").click(function() {
        $("#todoModalLabel").text("Create a TODO");
        $("#todoForm")[0].reset();
        $("#todoModal").modal("show");
        $("#saveTodoButton").data("action", "create").removeData("todoId");
    });

    // Handle Create/Update TODO Form Submission
    $("#todoForm").submit(function(event) {
        event.preventDefault();
        const action = $("#saveTodoButton").data("action");
        const todoId = $("#saveTodoButton").data("todoId");
        const url = action === "create" ? "/todos/todo" : `/todos/todo/${todoId}`;
        const method = action === "create" ? "POST" : "PUT";

        const todoData = {
            title: $("#todoTitle").val(),
            description: $("#todoDescription").val(),
            priority: parseInt($("#todoPriority").val()),
            complete: $("#todoComplete").val() === "true"
        };

        $.ajax({
            url: url,
            type: method,
            contentType: "application/json",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("jwt_token")
            },
            data: JSON.stringify(todoData),
            success: function(response) {
                $("#todoModal").modal("hide");
                if (action === "create") {
                    addTodoToDOM(response);
                } else if (action === "update") {
                    updateTodoInDOM(response);
                }
            },
            error: function(xhr) {
                if (xhr.status === 401) {
                    alert("Session expired. Please log in again.");
                } else {
                    alert("Error saving TODO: " + xhr.responseText);
                }
            }
        });
    });

    // Show Update TODO Modal
    $(document).on("click", ".updateTodoButton", function() {
        const todoItem = $(this).closest(".list-group-item");
        const todoId = todoItem.data("id");

        $("#todoTitle").val(todoItem.find("h5").text());
        $("#todoDescription").val(todoItem.find("p").first().text());
        const priorityText = todoItem.find("small").text().split(", ")[0].split(": ")[1];
        const completeText = todoItem.find("small").text().split(", ")[1].split(": ")[1];
        $("#todoPriority").val(priorityText);
        $("#todoComplete").val(completeText === "Yes" ? "true" : "false");

        $("#todoModalLabel").text("Update TODO");
        $("#todoModal").modal("show");
        $("#saveTodoButton").data("action", "update").data("todoId", todoId);
    });

    // Handle Delete TODO Button
    $(document).on("click", ".deleteTodoButton", function() {
        const todoId = $(this).closest(".list-group-item").data("id");

        const userConfirmed = confirm("Are you sure you want to delete this TODO?");
        if (userConfirmed) {
            $.ajax({
                url: `/todos/todo/${todoId}`,
                type: "DELETE",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("jwt_token")
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
    });

    // Function to add a new TODO to the DOM
    function addTodoToDOM(todo) {
        const todoList = $("#todoList");
        const todoHtml = `
            <div class="list-group-item d-flex justify-content-between align-items-center" data-id="${todo.id}">
                <div>
                    <h5>${todo.title}</h5>
                    <p>${todo.description}</p>
                    <small><strong>Priority:</strong> ${todo.priority}, <strong>Complete:</strong> ${todo.complete ? 'Yes' : 'No'}</small>
                </div>
                <div>
                    <button class="btn btn-light btn-sm updateTodoButton"><i class="fa fa-pencil" style="color: grey;"></i></button>
                    <button class="btn btn-danger btn-sm deleteTodoButton"><i class="fa fa-trash" style="color: white;"></i></button>
                </div>
            </div>
        `;
        todoList.append(todoHtml);
    }

    // Function to update a TODO in the DOM
    function updateTodoInDOM(updatedTodo) {
        const todoItem = $(`[data-id='${updatedTodo.id}']`);
        todoItem.find("h5").text(updatedTodo.title);
        todoItem.find("p").first().text(updatedTodo.description);
        todoItem.find("small").html(`<strong>Priority:</strong> ${updatedTodo.priority}, <strong>Complete:</strong> ${updatedTodo.complete ? 'Yes' : 'No'}`);
    }

    // Function to remove a TODO from the DOM
    function removeTodoFromDOM(todoId) {
        $(`[data-id='${todoId}']`).remove();
    }
});
