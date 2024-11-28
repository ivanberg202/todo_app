document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const repeatPassword = document.getElementById("repeatPassword").value;

    // Check if passwords match
    if (password !== repeatPassword) {
        displayErrorMessage("Passwords do not match.");
        return;
    }

    // Make request for registration
    fetch("/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            username: username,
            password: password
        })
    })
        .then((response) => {
            if (!response.ok) {
                return response.json().then((data) => {
                    throw new Error(data.message || "An error occurred during registration.");
                });
            }
            return response.json();
        })
        .then(() => {
            // On successful registration, automatically log in the user
            return fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({
                    username: username,
                    password: password
                })
            });
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Auto-login failed after registration.");
            }
            return response.json();
        })
        .then((data) => {
            // Store the JWT token and redirect to the dashboard
            localStorage.setItem("access_token", data.access_token);
            window.location.href = "/auth/dashboard";
        })
        .catch((error) => {
            displayErrorMessage(error.message);
        });
});

function displayErrorMessage(message) {
    const errorMessageElement = document.getElementById("errorMessage");
    errorMessageElement.innerText = message;
    errorMessageElement.style.display = "block";
}
