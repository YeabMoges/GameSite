document.addEventListener('DOMContentLoaded', function () {
    const usernameInput = document.getElementById('username');
    const usernameError = document.getElementById('usernameError');
    const phoneNumberInput = document.getElementById('phone_number');
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    const passwordInput = document.getElementById('password');
    const addressInput = document.getElementById('address');

    // Helper function for adding/removing classes
    function updateValidationState(input, isValid, isPartial = false) {
        if (isValid) {
            input.classList.add('valid-full');
            input.classList.remove('valid-partial', 'is-invalid');
        } else if (isPartial) {
            input.classList.add('valid-partial');
            input.classList.remove('valid-full', 'is-invalid');
        } else {
            input.classList.add('is-invalid');
            input.classList.remove('valid-full', 'valid-partial');
        }
    }

    // Username validation logic
    if (usernameInput) {
        usernameInput.addEventListener('input', function () {
            const username = usernameInput.value;

            if (!username.trim()) {
                usernameError.style.display = 'none';
                updateValidationState(usernameInput, false);
                return;
            }

            fetch(`/check_username?username=${encodeURIComponent(username)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        usernameError.style.display = 'block';
                        updateValidationState(usernameInput, false);
                    } else {
                        usernameError.style.display = 'none';
                        updateValidationState(usernameInput, true);
                    }
                })
                .catch(error => {
                    console.error('Error checking username:', error);
                });
        });
    }

    // Email validation logic
    if (emailInput) {
        emailInput.addEventListener('input', function () {
            const email = emailInput.value;

            // Basic regex for validating an email
            const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            const isValid = emailPattern.test(email);

            // Update validation state based on regex match
            if (isValid) {
                updateValidationState(emailInput, true);
                emailError.style.display = 'none';
            } else if (email.trim()) {
                updateValidationState(emailInput, false, true); // Partial validity
                emailError.style.display = 'none';
            } else {
                updateValidationState(emailInput, false);
                emailError.style.display = 'block';
            }
        });
    }

    // Phone number validation logic
    if (phoneNumberInput) {
        phoneNumberInput.addEventListener('input', function () {
            const value = phoneNumberInput.value.replace(/\D/g, ''); // Remove non-digit characters
            const isValid = /^\d{10}$/.test(value); // Must be exactly 10 digits

            updateValidationState(phoneNumberInput, isValid);

            // Format phone number as (XXX) XXX-XXXX
            if (value.length >= 7) {
                phoneNumberInput.value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6)}`;
            } else if (value.length >= 4) {
                phoneNumberInput.value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
            } else if (value.length > 0) {
                phoneNumberInput.value = `(${value.slice(0, 3)}`;
            }
        });
    }

    // Password validation logic
    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            const value = passwordInput.value;
            const hasUppercase = /[A-Z]/.test(value);
            const hasNumber = /[0-9]/.test(value);
            const hasSpecialChar = /[!@#$%^&*]/.test(value);
            const isMinLength = value.length >= 8;

            if (hasUppercase && hasNumber && hasSpecialChar && isMinLength) {
                updateValidationState(passwordInput, true);
            } else if (value) {
                updateValidationState(passwordInput, false, true);
            } else {
                updateValidationState(passwordInput, false);
            }
        });
    }

    // Address validation logic
    if (addressInput) {
        addressInput.addEventListener('input', function () {
            const value = addressInput.value;
            const hasLetters = /[a-zA-Z]/.test(value);
            const hasNumbers = /[0-9]/.test(value);
            const isValid = value.length >= 5 && hasLetters && hasNumbers;

            updateValidationState(addressInput, isValid);
        });
    }

    // Flash message fade-out logic
    const flashMessages = document.querySelectorAll('.alert');
    console.log("Flash messages found:", flashMessages);

    if (flashMessages.length > 0) {
        console.log("Starting fade-out timer...");
        setTimeout(() => {
            flashMessages.forEach(alert => {
                console.log("Fading out alert:", alert);
                alert.classList.add('fade'); // Apply fade class
                setTimeout(() => {
                    console.log("Removing alert:", alert);
                    alert.remove(); // Remove the element after fading out
                }, 500); // Time to fully remove the element after fade-out
            });
        }, 5000); // 5-second delay before fading
    } else {
        console.log("No flash messages found.");
    }
});
