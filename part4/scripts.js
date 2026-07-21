document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }
});


async function loginUser(email, password) {
    try {
        const response = await fetch(
            'http://127.0.0.1:5000/api/v1/auth/login',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (response.ok) {
            document.cookie =
                `token=${data.access_token}; path=/; SameSite=Lax`;

            window.location.href = 'index.html';
        } else {
            displayLoginError(
                data.error || data.message || 'Invalid email or password.'
            );
        }
    } catch (error) {
        console.error('Login request failed:', error);
        displayLoginError('Unable to connect to the server.');
    }
}


function displayLoginError(message) {
    let errorMessage = document.getElementById('login-error');

    if (!errorMessage) {
        errorMessage = document.createElement('p');
        errorMessage.id = 'login-error';

        const loginForm = document.getElementById('login-form');
        loginForm.appendChild(errorMessage);
    }

    errorMessage.textContent = message;
}