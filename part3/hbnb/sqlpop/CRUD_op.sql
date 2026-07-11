SELECT id, email, is_admin FROM User WHERE email = 'admin@hbnb.io';
SELECT id, name FROM Amenity ORDER BY name;


INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('4912053e-48d2-4790-90a3-a4084a038af1', 'Jesse', 'Pinkman', 'jesse.pinkman@crack.com', 'hashisfun', FALSE);

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

SELECT * FROM Place WHERE id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';

SELECT p.title, a.name
FROM Place p
JOIN Place_Amenity pa ON p.id = pa.place_id
JOIN Amenity a ON pa.amenity_id = a.id
WHERE p.id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';

SELECT r.text, r.rating, u.email AS reviewer, p.title AS place
FROM Review r
JOIN User u ON r.user_id = u.id
JOIN Place p ON r.place_id = p.id;

UPDATE Place SET price = 99.99 WHERE id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';
UPDATE Review SET rating = 4 WHERE id = 'edaf5334-cb89-4b93-92f3-9544fdc43000';

SELECT price FROM Place WHERE id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';
SELECT rating FROM Review WHERE id = 'edaf5334-cb89-4b93-92f3-9544fdc43000';

DELETE FROM Review WHERE id = '33333333-3333-3333-3333-333333333333';
DELETE FROM Place_Amenity WHERE place_id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';

SELECT COUNT(*) AS remaining_reviews FROM Review WHERE place_id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';

DELETE FROM Place WHERE id = '15828bb0-162d-47e2-b3e2-e7dbc3dd744c';
DELETE FROM User WHERE id = '4912053e-48d2-4790-90a3-a4084a038af1';