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