SELECT id, email, is_admin FROM User WHERE email = 'admin@hbnb.io';
SELECT id, name FROM Amenity ORDER BY name;

SELECT * FROM User; -- Printing list of current tables
SELECT * FROM Place;
SELECT * FROM Amenity;
SELECT * FROM Review;
SELECT * FROM Place_Amenity;

INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('4912053e-48d2-4790-90a3-a4084a038af1', 'Jesse', 'Pinkman', 'jesse.pinkman@crack.com', 'hashisfun', FALSE);-- Inserting new users/places/amenitys/reviews

INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('018bb03d-1c58-4fd1-8862-4decdd150ce1', 'Pablo', 'Escobar', 'pablo.escobar@crack.com', 'theking', FALSE);

INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '15828bb0-162d-47e2-b3e2-e7dbc3dd744c',
    'Cozy Crack Production Apartment',
    'A comfortable 4-bedroom apartment close to the city center.',
    100.00,
    35.1002,
    -106.5615,
    '4912053e-48d2-4790-90a3-a4084a038af1'
);

INSERT INTO Place_Amenity (place_id, amenity_id)
VALUES (
    '15828bb0-162d-47e2-b3e2-e7dbc3dd744c',
    '47559627-1779-4a75-a1b0-aecc1bbc00f2'
);

INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES (
    'edaf5334-cb89-4b93-92f3-9544fdc43000',
    'Great location to produce high-quality methamphetamine. Highly recommend!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    '15828bb0-162d-47e2-b3e2-e7dbc3dd744c'
);

INSERT INTO Amenity (id, name)
VALUES
    ('6c749868-7068-4dd9-a4da-666f9dc2edce', 'Spoon');

SELECT * FROM User;-- Print list lists of newly inserted users/places/amenitys/reviews
SELECT * FROM Place;
SELECT * FROM Amenity;
SELECT * FROM Review;
SELECT * FROM Place_Amenity;

SELECT * FROM User WHERE id = '4912053e-48d2-4790-90a3-a4084a038af1';-- Printing specific records from the tables
SELECT * FROM Amenity WHERE id = '6c749868-7068-4dd9-a4da-666f9dc2edce';
SELECT * FROM Place WHERE id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';

SELECT p.title, a.name
FROM Place p
JOIN Place_Amenity pa ON p.id = pa.place_id
JOIN Amenity a ON pa.amenity_id = a.id
WHERE p.id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';-- Print amenities for a specific place

SELECT r.text, r.rating, u.email AS reviewer, p.title AS place
FROM Review r
JOIN User u ON r.user_id = u.id
JOIN Place p ON r.place_id = p.id;-- Print reviews for a specific place

UPDATE Place SET price = 99.99 WHERE id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';-- Updating records in the tables
UPDATE Review SET rating = 4 WHERE id = 'edaf5334-cb89-4b93-92f3-9544fdc43000';

SELECT * FROM Place WHERE id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';-- Printing updated records
SELECT * FROM Review WHERE id = 'edaf5334-cb89-4b93-92f3-9544fdc43000';

SELECT * FROM User;-- Printing list of current tables
SELECT * FROM Place;
SELECT * FROM Amenity;
SELECT * FROM Review;
SELECT * FROM Place_Amenity;

DELETE FROM Review WHERE id = 'edaf5334-cb89-4b93-92f3-9544fdc43000';-- Deleting records from the tables
DELETE FROM Place_Amenity WHERE place_id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';
DELETE FROM Amenity WHERE id = '6c749868-7068-4dd9-a4da-666f9dc2edce';
DELETE FROM Place WHERE id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';
DELETE FROM User WHERE id = '4912053e-48d2-4790-90a3-a4084a038af1';

SELECT * FROM User;-- Printing list of current tables
SELECT * FROM Place;
SELECT * FROM Amenity;
SELECT * FROM Review;
SELECT * FROM Place_Amenity;