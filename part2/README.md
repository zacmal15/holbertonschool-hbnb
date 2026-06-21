# Business Logic Layer

## Overview

The Business Logic Layer contains the core entities of the HBnB application and implements the business rules of the application. This layer is responsible for managing the four models: Users, Places, Reviews, and Amenities, while also maintaining the relationship between them.

All models inherit from the `BaseModel` class, which provides all common attributes between the models such as uuid, and time stamps.

## BaseModel

The `BaseModel` class serves as the parent class for all models to inherit from and provides the following common attributes:

- `id`: A unique UUID4 identifier
- `created_at`: Date and time the object was created
- `updated_at`: Date and time the object was last modified

## Methods

- `save()`: Updates the 'updated_at' timestamp
- `update(data)`: Updates object attributes from a dictionary and refreshes timestamp

---

## User

`User` represents a user of the HBnB application.

## Attributes

- `first_name`
- `last_name`
- `email`
- `is_admin`
- `places`
- `reviews`

## Responsibilites

- Stores user info
- Registers places under user
- Write reviews under user
- Validates user data such as email format and name length

---

## Place

`Place` model represents a property listing.

## Attributes

- `title`
- `description`
- `price`
- `latitude`
- `longitude`
- `owner`
- `reviews`
- `amenities`

## Responsibilites

- Stores information regarding the place
- Associates a place with an owner
- Maintain reviews and amenities associated with place
- Validates location and pricing information

## Methods

- `add_review(review)`
- `add_amenity(amenity)`

---

## Review

`Review` model represents feedback left by a user for a place.

## Attributes

- `text`
- `rating`
- `place`
- `user`

## Responsibilites

- Store review information
- Associate reviews with users and places
- Validate review ratings

---

## Amenity

`Amenity` model represents a feature available at a place

## Attributes

- `name`

## Responsibilites

- Stores amenity information
- Assocaites amenities with places

---

## Entity Relationships

The Business Logic Layer implements the following relationships:

- One user can own many places
- One user can write many reviews
- One place can have many reviews
- One place can have many amenities
- One review belongs to one user and one place

---

## Usage Examples

### Create a user

user = User(
    first_name="Sam",
    last_name="Lachlan",
    email="anthony@example.com
)

### Create a place

place = Place(
    title="zacshouse",
    description="mansion",
    price=3,
    latitude=11.111,
    longitude= 33.333,
    owner=user
)

### Create a review

review = Review(
    text="wasnt actually that big",
    rating=1,
    place=place,
    user=user
)

### Create an amenity

wifi = Amenity("Wifi")
place.add.amenity(wifi)

### Update an entity

user.update({
    "first_name": "Samuel"
})This is the readme for the hbnh project part 2


---

### Setup and running
1. git clone https://github.com/SamAT01ni/holbertonschool-hbnb/
2. cd part2/hbnb/
3. pip install -r requirements.txt
4. python3 run.py

Doing these four steps setup and run the api services, once this is setup you have multiple options to run and use the services.
such as through the swagger using http://127.0.0.1:5000/api/v1/ or curl/postman etc..

Example curl commands:
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}'
```
Expected output:
```
{
  "id": "ba3e4f2d-2e71-41d4-8bf0-389b8afa26f0",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```
Here you have created the user John Doe, with the email john.doe@example.com

