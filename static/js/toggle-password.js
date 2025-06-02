document.addEventListener("DOMContentLoaded", function () {
    // Select all password toggle buttons
    document.querySelectorAll(".toggle-password").forEach(button => {
        button.addEventListener("click", function () {
            let passwordField = this.previousElementSibling; // Get the password input
            let icon = this.querySelector("i"); // Get the icon inside button

            if (passwordField.type === "password") {
                passwordField.type = "text";  // Show password
                icon.classList.remove("fa-eye");
                icon.classList.add("fa-eye-slash");
            } else {
                passwordField.type = "password";  // Hide password
                icon.classList.remove("fa-eye-slash");
                icon.classList.add("fa-eye");
            }
        });
    });
});
