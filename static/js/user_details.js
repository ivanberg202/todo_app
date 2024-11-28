export function openUserDetailsForm(user = {}, token) {
    // Create form elements
    const formModal = document.createElement('div');
    formModal.classList.add('modal', 'fade');
    formModal.setAttribute('tabindex', '-1');
    formModal.setAttribute('aria-labelledby', 'userDetailsModalLabel');
    formModal.setAttribute('aria-hidden', 'true');
    formModal.id = 'userDetailsModal';

    formModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 id="userDetailsModalLabel" class="modal-title">Edit User Details</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="userDetailsForm">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" class="form-control" id="username" value="${user.username || ''}" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" value="${user.email || ''}" required>
                        </div>
                        <div class="mb-3">
                            <label for="firstName" class="form-label">First Name</label>
                            <input type="text" class="form-control" id="firstName" value="${user.first_name || ''}">
                        </div>
                        <div class="mb-3">
                            <label for="lastName" class="form-label">Last Name</label>
                            <input type="text" class="form-control" id="lastName" value="${user.last_name || ''}">
                        </div>
                        <div class="mb-3">
                            <label for="phoneNumber" class="form-label">Phone Number</label>
                            <input type="text" class="form-control" id="phoneNumber" value="${user.phone_number || ''}">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" id="saveUserDetailsButton">Save Changes</button>
                </div>
            </div>
        </div>
    `;

    // Append the modal to the body
    document.body.appendChild(formModal);

    // Initialize and show the modal
    const modalInstance = new bootstrap.Modal(formModal);
    modalInstance.show();

    // Remove the modal from the DOM after it is hidden
    formModal.addEventListener('hidden.bs.modal', () => {
        formModal.remove();
    });

    // Handle form submission
    const saveButton = formModal.querySelector('#saveUserDetailsButton');
    saveButton.addEventListener('click', async () => {
        const updatedUser = {
            username: formModal.querySelector('#username').value,
            email: formModal.querySelector('#email').value,
            first_name: formModal.querySelector('#firstName').value,
            last_name: formModal.querySelector('#lastName').value,
            phone_number: formModal.querySelector('#phoneNumber').value,
        };

        try {
            const response = await fetch('/user/update_details', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(updatedUser),
            });

            if (response.ok) {
                console.log('User details updated successfully');
                modalInstance.hide();
                location.reload(); // Refresh to show updated user info
            } else {
                const errorData = await response.json();
                console.error('Error updating user details:', errorData);
            }
        } catch (error) {
            console.error('Error updating user details:', error);
        }
    });
}
