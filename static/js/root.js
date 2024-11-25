// root.js
console.log("root.js loaded successfully");

document.addEventListener("DOMContentLoaded", async function () {
    // Check if we're on the base page
    console.log("Current path:", window.location.pathname);
    if (window.location.pathname === "/") {
        // Fetch the token from localStorage
        const token = localStorage.getItem("access_token");
        console.log("Token retrieved from localStorage:", token);

        // If no token is found, redirect to login page
        if (!token) {
            console.error("No token found, redirecting to login...");
            window.location.href = "/auth/login-page";
            return; // Add return to stop any further execution
        }

        // Verify the token's validity by making a request to the server
        try {
            const response = await fetch("/auth/verify-token", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (response.ok) {
                console.log("Token is valid, redirecting to dashboard...");
                window.location.href = "/auth/dashboard";
                return; // Ensure further code doesn't execute after redirect
            } else {
                console.error("Invalid token, redirecting to login...");
                window.location.href = "/auth/login-page";
                return; // Add return to prevent further execution
            }
        } catch (error) {
            console.error("Error verifying token, redirecting to login...", error);
            window.location.href = "/auth/login-page";
            return; // Add return to prevent further execution
        }
    }
});
