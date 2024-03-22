document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.signup-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        // Email
        const emailInput = document.getElementById('email');
        const email = emailInput.value.trim();
        if (!isValidEmail(email)) {
            showError(emailInput, 'Please enter a valid email address');
            return;
        }

        // Username
        const usernameInput = document.getElementById('username');
        const username = usernameInput.value.trim();
        if (username.length < 3) {
            showError(usernameInput, 'Username must be at least 3 characters long');
            return;
        }
        const disallowedCharsRegex = /[^a-zA-Z0-9]/;
        if (disallowedCharsRegex.test(username)) {
            showError(usernameInput, 'Username can only contain letters and numbers');
            return;
        }

        // Password
        const passwordInput = document.getElementById('password');
        const password = passwordInput.value.trim();
        if (!isValidPassword(password)) {
            showError(passwordInput, 'Password must be at least 6 characters long');
            return;
        }

        // Confirm Password
        const confirmPassword = confirmPasswordInput.value.trim();
        if (password !== confirmPassword) {
            showError(confirmPasswordInput, 'Passwords do not match');
            return;
        }
        
        // If all validations pass, submit the form
        form.submit();
    });

    passwordInput.addEventListener('input', function () {
        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();
        if (confirmPassword && password !== confirmPassword) {
            showError(confirmPasswordInput, 'Passwords do not match');
        } else {
            clearError(confirmPasswordInput);
        }
    });

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPassword(password) {
        return password.length >= 6;
    }

    function showError(input, errorMessage) {
        const formGroup = input.parentElement;
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerText = errorMessage;
        formGroup.appendChild(errorDiv);
        input.style.border = '1px solid red';
        setTimeout(function () {
            errorDiv.remove();
            input.style.border = '1px solid #ccc';
        }, 3000); // Remove the error message after 3 seconds
    }

    function clearError(input) {
        const formGroup = input.parentElement;
        const errorDiv = formGroup.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.remove();
            input.style.border = '1px solid #ccc';
        }
    }
    
    setTimeout(function () {
        const flashMessages = document.getElementById('flash-messages');
        if (flashMessages) {
            flashMessages.style.display = 'none';
        }
    }, 3000);
});