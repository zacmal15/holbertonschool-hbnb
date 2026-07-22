document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }

    if (placesList) {
        checkAuthentication();
    }

    if (priceFilter) {
        priceFilter.addEventListener('change', filterPlacesByPrice);
    }
});


function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (const cookie of cookies) {
        const trimmedCookie = cookie.trim();
        const [cookieName, cookieValue] = trimmedCookie.split('=');

        if (cookieName === name) {
            return cookieValue;
        }
    }

    return null;
}


function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    fetchPlaces(token);
}


async function fetchPlaces(token) {
    try {
        const headers = {};

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(
            'http://127.0.0.1:5000/api/v1/places/',
            {
                method: 'GET',
                headers: headers
            }
        );

        if (!response.ok) {
            throw new Error(`Failed to fetch places: ${response.status}`);
        }

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);

        const placesList = document.getElementById('places-list');

        if (placesList) {
            placesList.innerHTML =
                '<p>Unable to load places at the moment.</p>';
        }
    }
}


function displayPlaces(places) {
    const placesList = document.getElementById('places-list');

    if (!placesList) {
        return;
    }

    placesList.innerHTML = '';

    places.forEach((place) => {
        const placeCard = document.createElement('article');

        placeCard.classList.add('place-card');
        placeCard.dataset.price = place.price;

        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>${place.description || 'No description available.'}</p>
            <p><strong>Price:</strong> $${place.price} per night</p>
            <a
                href="place.html?id=${place.id}"
                class="details-button"
            >
                View Details
            </a>
        `;

        placesList.appendChild(placeCard);
    });
}


function filterPlacesByPrice(event) {
    const selectedValue = event.target.value;
    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach((card) => {
        const placePrice = Number(card.dataset.price);

        if (
            selectedValue === 'all' ||
            placePrice <= Number(selectedValue)
        ) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}


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

        if (loginForm) {
            loginForm.appendChild(errorMessage);
        }
    }

    errorMessage.textContent = message;
}