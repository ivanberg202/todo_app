export function fetchUserDetails() {
    const jwtToken = getJwtToken();

    if (!jwtToken) {
        handleSessionExpired();
        return;
    }

    $.ajax({
        url: "/auth/me",
        type: "GET",
        headers: {
            "Authorization": "Bearer " + jwtToken
        },
        success: function(response) {
            console.log("User details fetched successfully:", response);
            const displayName = response.first_name ? response.first_name : response.username;
            $("#todosHeading").text(`${displayName}'s TODOs`);
        },
        error: function(xhr) {
            console.error("Error fetching user details:", xhr);
            if (xhr.status === 401) {
                handleSessionExpired();
            } else {
                $("#todosHeading").text('Error fetching user details.');
            }
        }
    });
}
