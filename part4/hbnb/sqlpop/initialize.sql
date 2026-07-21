INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2a$12$9B/gj2iaoiPrGLebbIyqteqimGgQM4PQdz4a4hNLeBp2UzLTvUsTa',
    TRUE
);

INSERT INTO Amenity (id, name)
VALUES
    ('47559627-1779-4a75-a1b0-aecc1bbc00f2', 'WiFi'),
    ('8f315c5c-95d6-4b6c-bb00-184ba2d51404', 'Swimming Pool'),
    ('3e5374bd-255a-43d2-90e7-c1918781c603', 'Air Conditioning');
 