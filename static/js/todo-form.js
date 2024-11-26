import { addOrUpdateTodo } from './api.js';

export function openTodoForm(todo = null, token) {
    // Create form elements
    const formModal = document.createElement('div');
    formModal.classList.add('modal', 'fade'); // Add 'fade' class for transition
    formModal.setAttribute('tabindex', '-1'); // Necessary for Bootstrap modals
    formModal.setAttribute('aria-labelledby', 'todoFormModalLabel');
    formModal.setAttribute('aria-hidden', 'true');
    formModal.id = 'todoFormModal'; // Optional: Assign an ID for reference

    formModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 id="todoFormModalLabel" class="modal-title">${todo ? 'Edit Todo' : 'Add a Todo'}</h5>
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
                        <div class="mb-3">
                            <label for="todoComplete" class="form-label">Completed</label>
                            <input type="checkbox" class="form-check-input" id="todoComplete" ${todo && todo.complete ? "checked" : ""}>
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

    // Append the modal to the body
    document.body.appendChild(formModal);

    // Initialize and show the modal using Bootstrap's JavaScript API
    const modalInstance = new bootstrap.Modal(formModal);
    modalInstance.show();

    // Remove the modal from DOM after it is hidden
    formModal.addEventListener('hidden.bs.modal', function () {
        formModal.remove();
    });

    // Use querySelector within formModal to scope the selectors
    const saveTodoButton = formModal.querySelector('#saveTodoButton');
    saveTodoButton.addEventListener('click', async function () {
        const title = formModal.querySelector('#todoTitle').value;
        const priority = formModal.querySelector('#todoPriority').value;
        const description = formModal.querySelector('#todoDescription').value;
        const complete = formModal.querySelector('#todoComplete').checked;

        const todoData = {
            title,
            priority: parseInt(priority, 10),
            description,
            complete
        };

        const method = todo ? "PUT" : "POST";
        try {
            const response = await addOrUpdateTodo(todoData, todo ? todo.id : null, method, token);

            if (response.ok) {
                console.log(`Todo ${todo ? 'updated' : 'added'} successfully.`);
                modalInstance.hide(); // Close the modal using Bootstrap's method
                location.reload(); // Refresh the page to show the updated list
            } else {
                console.error(`Failed to ${todo ? 'update' : 'add'} todo. Status code: ${response.status}`);
                const errorMessage = await response.json();
                console.error('Error message:', errorMessage);
            }
        } catch (error) {
            console.error(`Error attempting to ${todo ? 'update' : 'add'} todo:`, error);
        }
    });
}
