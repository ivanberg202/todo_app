console.log("login.js loaded successfully");

document.addEventListener("DOMContentLoaded", function () {
    // Check if we're on the login page
    if (window.location.pathname !== "/auth/login-page") {
        console.log("Not on the login page, skipping login script.");
        return;
    }

    const loginForm = document.getElementById("loginForm");
    if (!loginForm) {
        console.error("Login form not found on the page.");
        return;
    }
    const errorMessage = document.getElementById("errorMessage");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(loginForm);
        const username = formData.get("username");
        const password = formData.get("password");

        console.log("Submitting form with:", username, password); // Log username and password

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    username: username,
                    password: password
                })
            });

            console.log("Response status:", response.status); // Log response status

            if (response.ok) {
                const data = await response.json();
                console.log("Login successful:", data); // Log the response data

                // Save the token in localStorage
                localStorage.setItem("access_token", data.access_token);

                window.location.href = "/auth/dashboard";

            } else {
                console.error("Login failed. Status code:", response.status); // Log failure status
                const errorData = await response.json();
                console.error("Error details:", errorData); // Log error details
                errorMessage.style.display = "block";
                errorMessage.textContent = errorData.detail || "Invalid login credentials.";
            }
        } catch (error) {
            console.error("Error during login:", error); // Log any JavaScript errors
            errorMessage.style.display = "block";
            errorMessage.textContent = "An error occurred. Please try again.";
        }
    });
});
