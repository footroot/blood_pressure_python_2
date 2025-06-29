// blood_pressure_python_2/users/static/users/js/password_toggle.js

document.addEventListener('DOMContentLoaded', function() {
    // Select all password input fields and their toggle buttons
    const passwordFields = document.querySelectorAll('input[type="password"]');

    passwordFields.forEach(function(passwordField) {
        // Create the toggle button
        const toggleButton = document.createElement('button');
        toggleButton.type = 'button'; // Important: Prevent form submission
        toggleButton.textContent = 'Show';
        toggleButton.classList.add('password-toggle-button');
        toggleButton.setAttribute('aria-label', 'Toggle password visibility');

        // Insert the button right after the password field
        passwordField.parentNode.insertBefore(toggleButton, passwordField.nextSibling);

        toggleButton.addEventListener('click', function() {
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                toggleButton.textContent = 'Hide';
            } else {
                passwordField.type = 'password';
                toggleButton.textContent = 'Show';
            }
        });
    });
});