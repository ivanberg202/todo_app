// Fetch the current user's role
export async function getCurrentUserRole(token) {
    console.log('Token passed to getCurrentUserRole:', token); // Debugging
    try {
        const response = await fetch('/auth/me', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error fetching user info:', errorData);
            throw new Error(errorData.detail || 'Failed to fetch user info');
        }

        const userInfo = await response.json();
        console.log('Current user info:', userInfo); // Debugging
        return userInfo.role; // Extract the role
    } catch (error) {
        console.error('Error fetching current user role:', error);
        throw error;
    }
}

// Open the user details modal
export function openUserDetailsForm(user = {}, token, currentUserRole) {
    console.log('Opening user details form for role:', currentUserRole); // Debugging

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
                        <!-- User Identifier Field for Admins -->
                        ${currentUserRole?.toLowerCase() === 'admin' ? `
                        <div class="mb-3">
                            <label for="userIdentifier" class="form-label">Another user's username or email</label>
                            <input type="text" class="form-control" id="userIdentifier" value="${user.user_identifier || ''}">
                        </div>
                        ` : ''}

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
                        <!-- Role Field for Admins -->
                        ${currentUserRole?.toLowerCase() === 'admin' ? `
                        <div class="mb-3">
                            <label for="role" class="form-label">Role</label>
                            <select class="form-control" id="role">
                                <option value="user" ${user.role === 'user' ? 'selected' : ''}>User</option>
                                <option value="admin" ${user.role === 'admin' ? 'selected' : ''}>Admin</option>
                            </select>
                        </div>
                        ` : ''}
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" id="saveUserDetailsButton">Save Changes</button>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(formModal);

    const modalInstance = new bootstrap.Modal(formModal);
    modalInstance.show();

    formModal.addEventListener('hidden.bs.modal', () => {
        formModal.remove();
    });

    // Handle form submission
    const saveButton = formModal.querySelector('#saveUserDetailsButton');
    saveButton.addEventListener('click', async () => {
        const updatedUser = {
            user_identifier: currentUserRole === 'admin' ? formModal.querySelector('#userIdentifier')?.value : undefined,
            username: formModal.querySelector('#username').value,
            email: formModal.querySelector('#email').value,
            first_name: formModal.querySelector('#firstName').value,
            last_name: formModal.querySelector('#lastName').value,
            phone_number: formModal.querySelector('#phoneNumber').value,
            role: currentUserRole === 'admin' ? formModal.querySelector('#role')?.value : undefined, // Only for admins
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

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error updating user details:', errorData);
                alert(`Error: ${errorData.detail}`);
                return;
            }

            const result = await response.json();
            console.log('User details updated successfully:', result);
            alert('User details updated successfully.');
        } catch (error) {
            console.error('Error updating user details:', error);
            alert('An unexpected error occurred. Please try again later.');
        }
    });
}


// Fetch the role and show the modal
async function showUserDetailsModal(selectedUser, token) {
    try {
        // Fetch the current user's role
        const currentUserRole = await getCurrentUserRole(token);

        // Open the modal with the fetched role
        openUserDetailsForm(selectedUser, token, currentUserRole);
    } catch (error) {
        console.error('Failed to show user details modal:', error);
        alert('Unable to load user details. Please try again.');
    }
}

// Exported function to call from other scripts
export async function openModalForUserDetails(selectedUser, token) {
    await showUserDetailsModal(selectedUser, token);
}
