import { addOrUpdateTodo } from './api.js';

export function openTodoForm(todo = null, token) {
    // Create form elements
    const formModal = document.createElement('div');
    formModal.classList.add('modal');
    formModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${todo ? 'Edit Todo' : 'Add a Todo'}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="todoForm">
                        <div class="mb-3">
                            <label for="todoTitle" class="form-label">Title</label>
                            <input type="text" class="form-control" id="todoTitle" value="${todo ? todo.title : ''}" required>
                        </div>
                        <div class="mb-3">
                            <label for="todoPriority" class="form-label">Priority</label>
                            <input type="number" class="form-control" id="todoPriority" value="${todo ? todo.priority : ''}" required>
                        </div>
                        <div class="mb-3">
                            <label for="todoDescription" class="form-label">Description</label>
                            <input type="text" class="form-control" id="todoDescription" value="${todo ? todo.description : ''}" required>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" id="saveTodoButton">${todo ? 'Save Changes' : 'Add Todo'}</button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(formModal);
    formModal.style.display = 'block';

    const saveTodoButton = document.getElementById('saveTodoButton');
    saveTodoButton.addEventListener('click', async function () {
        const title = document.getElementById('todoTitle').value;
        const priority = document.getElementById('todoPriority').value;
        const description = document.getElementById('todoDescription').value;

        const todoData = {
            title,
            priority: parseInt(priority, 10),
            description,
        };

        const method = todo ? "PUT" : "POST";
        const response = await addOrUpdateTodo(todoData, todo ? todo.id : null, method, token);

        if (response.ok) {
            console.log(`Todo ${todo ? 'updated' : 'added'} successfully.`);
            formModal.style.display = 'none';
            formModal.remove();
            location.reload(); // Refresh the page to show the updated list
        } else {
            console.error(`Failed to ${todo ? 'update' : 'add'} todo. Status code: ${response.status}`);
        }
    });
}
