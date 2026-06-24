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
})

---

# Setup and running HBnB

## Clone the repository
```
git clone https://github.com/SamAT01ni/holbertonschool-hbnb.git
```
## Navigate to hbnb
```
cd holbertonschool-hbnb/part2/hbnb
```
## Install the required parts
```
pip install -r requirements.txt
```
## Run the application
```
python3 run.py
```
This starts the api server and it can be accessed on your browser through:\
http://127.0.0.1:5000/api/v1/

You can then try to create users and places yourself using Swagger UI

---

# Using the API

We recommend using swagger ui through the localhost because thats what we used so i cannot really guide you elsewhere\
Going to show you a few examples of how to use the API anyway

Here is a screenshot of how the api should appear

![swagger ui](images/swaggerstart.png)

You can play around here and create users, places, amenities and reviews

Its thankfully quite self explanatory and you can find the associated curl commands which are taking place

## Creating a user
Here is an example of how to create a user

![user creation](images/dom1.png)

Then hit the **execute** button and if you have entered 2 strings and a new email of the right format you will see

![user success](images/DOM.png)

Curl commmand:
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Dominik",
  "last_name": "Szoboszlai",
  "email": "number8@liverpool.com"
}'
```
## Amenity creation

This works much the same, enter a string and boom, an amenity has been made!!!

## Place creation

Going to the places header and going into POST, you can create a Hbnb.

Only thing to note here is that you need to enter a valid user_id so the place actually belongs to someone.

Amenities are optional but if entered they must also match with an existing amenity id. Here is an example of the creation of Anfield
![place making](images/placeenter.png)

You have to enter valid data, valid user id and amenity ids and a non zero price, as well as having conditions around the latitude and longitude.

Curl Command:
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/places/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Anfield",
  "description": "Home of Liverpool football club",
  "price": 1000000,
  "latitude": 53.4308,
  "longitude": 2.9608,
  "owner_id": "77554ac6-9aa1-4d21-94f0-364ebc196207",
  "amenities_id": [
    "631b5c50-5f89-4375-a687-ab507b9d5871",
    "99b40da4-25a0-4372-81d4-487900cf2b2b"
  ]
}'
```

After hitting execute you should see this if successful

![place success](images/placemade.png)

Bosh

## Review making

Each review has to be connected to a user and a place

If the owner of the place tries to post a review it will not be made. no funny business here we are very serious.

But this is an example of how to do it

![review making](images/reviewenter.png)

Curl Command:
```
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/reviews/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "This is the best place on earth up the reds im upset salah is gone. Bring back Nunez!!!",
  "rating": 5,
  "user_id": "a7a04858-0f05-4c89-b360-6befe1c9d7b5",
  "place_id": "437f8620-daed-41dc-aa70-75531828fadc"
}'
```
And this will show on success

![review success](images/reviewmade.png)

You can also play around with updating each of these models, and retrieving lists for them :)

***You must not create anything machester united or arsenal related or there will be consequences***
