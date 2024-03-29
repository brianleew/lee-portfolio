INSERT INTO drp_periods (start_time, end_time)
VALUES
    ('2021-03-29 07:00', '2021-03-30 07:00'),
    ('2021-05-25 17:00', '2021-05-26 17:00'),
    ('2021-06-14 16:00', '2021-06-15 16:00'),
    ('2021-07-29 14:00', '2021-07-30 14:00');

INSERT INTO organizations (org_name)
VALUES
    ('ABC Corporation'),
    ('XYZ Industries'),
    ('Tech Innovators Ltd.'),
    ('Global Logistics Inc.'),
    ('MegaMart Superstores'),
    ('Software Solutions Co.'),
    ('United Builders Group'),
    ('Acme Widget Manufacturing'),
    ('Infinite Innovations'),
    ('Pacific Shipping Services');

INSERT INTO meter_map (entity_id, meter_id)
VALUES
    (3, 16335457),
    (4, 18762999),
    (5, 56068032),
    (6, 56073008),
    (7, 56210792),
    (8, 56464971),
    (9, 66675284),
    (10, 66676872),
    (11, 66735042),
    (12, 82458402),
    (3, 82458430),
    (4, 82458528),
    (5, 82458535),
    (6, 82458544),
    (7, 83425325),
    (8, 83425950),
    (9, 83425960),
    (10, 83426095),
    (11, 83692447),
    (12, 83692449),
    (3, 83692455),
    (4, 83692461),
    (5, 83692509),
    (6, 83692538),
    (7, 83693653),
    (8, 83693711),
    (9, 83694184),
    (10, 83761529),
    (11, 83761545),
    (12, 95282692),
    (3, 96186888),
    (4, 96186904),
    (5, 96375911),
    (6, 98569140),
    (7, 98790323),
    (8, 98790342),
    (9, 98828727),
    (10, 98828741),
    (11, 98828744),
    (12, 98828745),
    (3, 98828746),
    (4, 98828748),
    (5, 98828750),
    (6, 98923621),
    (7, 98923641),
    (8, 98923648),
    (9, 98923655),
    (10, 98923661),
    (11, 98923662),
    (12, 98923663),
    (3, 230156289);

INSERT INTO users (email, first_name, last_name, org_id)
VALUES
    ('contact@abccorp.com', 'John', 'Doe', 3),
    ('info@xyzindustries.com', 'Alice', 'Smith', 4),
    ('info@techinnovators.com', 'Robert', 'Johnson', 5),
    ('contact@globallogistics.com', 'Emily', 'Brown', 6),
    ('support@megamart.com', 'Michael', 'Lee', 7),
    ('info@softwaresolutions.com', 'Sophia', 'Wilson', 8),
    ('support@unitedbuilders.com', 'William', 'Davis', 9),
    ('contact@acmewidgets.com', 'Olivia', 'Evans', 10),
    ('info@infiniteinnovations.com', 'Daniel', 'Harris', 11),
    ('info@pacificshipping.com', 'Ava', 'Clark', 12);

-- PASSWORD IS 'example' FOR ALL USERS
INSERT INTO logins (account_id, password_hash)
VALUES
    (13, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (14, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (15, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (16, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (17, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (18, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (19, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (20, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (21, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y'),
    (22, '$2b$12$SLlIS3C5B0U77dgSKxvgiup4X2sJVkSCkDfa2bMl1aK3NuAvmAA0y');