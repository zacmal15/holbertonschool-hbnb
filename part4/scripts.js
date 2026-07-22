document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const placesList = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');
    const placeDetails = document.getElementById('place-details');

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

    if (placeDetails) {
        initialisePlaceDetailsPage();
    }
});


function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (const cookie of cookies) {
        const trimmedCookie = cookie.trim();
        const separatorIndex = trimmedCookie.indexOf('=');

        if (separatorIndex === -1) {
            continue;
        }

        const cookieName = trimmedCookie.slice(0, separatorIndex);
        const cookieValue = trimmedCookie.slice(separatorIndex + 1);

        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }

    return null;
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
                `token=${encodeURIComponent(data.access_token)}; ` +
                'path=/; SameSite=Lax; Max-Age=3600';

            window.location.href = 'index.html';
        } else {
            displayLoginError(
                data.error ||
                data.message ||
                data.msg ||
                'Invalid email or password.'
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

    if (!Array.isArray(places) || places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    places.forEach((place) => {
        const placeCard = document.createElement('article');

        placeCard.classList.add('place-card');
        placeCard.dataset.price = place.price;

        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>${place.description || 'No description available.'}</p>
            <p>
                <strong>Price:</strong>
                $${place.price} per night
            </p>
            <a
                href="place.html?id=${encodeURIComponent(place.id)}"
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


function getPlaceIdFromURL() {
    const queryParameters = new URLSearchParams(window.location.search);

    return queryParameters.get('id');
}


async function initialisePlaceDetailsPage() {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const addReviewLink = document.getElementById('add-review-link');
    const loginLink = document.getElementById('login-link');

    if (!placeId) {
        displayPlaceError('No place was selected.');
        return;
    }

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    if (addReviewLink) {
        addReviewLink.href =
            `add_review.html?id=${encodeURIComponent(placeId)}`;
    }

    await fetchPlaceDetails(token, placeId);
}


async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const placeResponse = await fetch(
            `http://127.0.0.1:5000/api/v1/places/${placeId}`,
            {
                method: 'GET',
                headers: headers
            }
        );

        if (!placeResponse.ok) {
            throw new Error(
                `Failed to fetch place: ${placeResponse.status}`
            );
        }

        const place = await placeResponse.json();

        const reviewsResponse = await fetch(
            `http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`,
            {
                method: 'GET',
                headers: headers
            }
        );

        let reviews = [];

        if (reviewsResponse.ok) {
            reviews = await reviewsResponse.json();
        }

        displayPlaceDetails(place);
        displayReviews(reviews);
    } catch (error) {
        console.error('Error fetching place details:', error);
        displayPlaceError('Unable to load the place details.');
    }
}


function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');

    if (!placeDetails) {
        return;
    }

    const ownerName = place.owner
        ? `${place.owner.first_name} ${place.owner.last_name}`
        : 'Unknown host';

    const amenities = Array.isArray(place.amenities)
        ? place.amenities
        : [];

    let amenitiesContent = '<li>No amenities listed.</li>';

    if (amenities.length > 0) {
        amenitiesContent = amenities
            .map((amenity) => `<li>${amenity.name}</li>`)
            .join('');
    }

    placeDetails.innerHTML = `
        <h1>${place.title}</h1>

        <div class="place-info">
            <p>
                <strong>Host:</strong>
                ${ownerName}
            </p>

            <p>
                <strong>Price:</strong>
                $${place.price} per night
            </p>

            <p>
                <strong>Description:</strong>
                ${place.description || 'No description available.'}
            </p>

            <h2>Amenities</h2>

            <ul>
                ${amenitiesContent}
            </ul>
        </div>
    `;
}


function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');

    if (!reviewsList) {
        return;
    }

    reviewsList.innerHTML = '';

    if (!Array.isArray(reviews) || reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach((review) => {
        const reviewCard = document.createElement('article');

        reviewCard.classList.add('review-card');

        reviewCard.innerHTML = `
            <p>${review.text}</p>
            <p>
                <strong>Rating:</strong>
                ${review.rating}/5
            </p>
        `;

        reviewsList.appendChild(reviewCard);
    });
}


function displayPlaceError(message) {
    const placeDetails = document.getElementById('place-details');

    if (placeDetails) {
        placeDetails.innerHTML = `<p>${message}</p>`;
    }
}