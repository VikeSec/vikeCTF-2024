#!/bin/sh

set -eu

DB_NAME="db.sqlite3"

if [ -e "$DB_NAME" ]; then
    echo "database $DB_NAME already exists, exiting"
    exit 1
fi

sqlite3 "$DB_NAME" -bail "
CREATE TABLE user (
    username TEXT,
    password TEXT
);

INSERT INTO user (username, password) VALUES (
    'admin',
    '$(xxd -l 32 -c 32 -p /dev/random)'
);

CREATE TABLE listing (
    id TEXT,
    title TEXT,
    description TEXT,
    priceCents INTEGER,
    image TEXT,
    PRIMARY KEY (id)
);

INSERT INTO listing (id, title, description, priceCents, image)
VALUES (
    '299f2f88-2da2-4d1a-a7c0-da7431393f4a',
    'Viking Beanie',
    'Warm and cozy beanie with a Viking-inspired design.',
    2500,
    '_694ffa14-0e1f-4477-a0ed-bd64b3997a57.jpg'
), (
    'd30fc1e8-838d-4d25-b3ee-76007376cdef',
    'Sweater Vest',
    'Classic sweater vest perfect for layering in chilly weather.',
    3500,
    '_c07fee49-8e5e-45e6-9144-ebac60e1ced3.jpg'
), (
    'bf223350-c731-42f7-ba0d-e738b556581f',
    'Bottle Opener',
    'Sturdy stainless steel bottle opener with ergonomic handle.',
    1000,
    '_780729f1-fc8c-4e90-930e-26acd2167fb6.jpg'
), (
    'ea5e8447-8e48-482b-9f62-f6a7e77d68d1',
    'Viking Shield Wall Art',
    'Handcrafted wooden wall art featuring a Viking shield design.',
    4500,
    '_4a3d1c6e-07ab-4d3c-a47e-51296f8206b1.jpg'
), (
    '6e3b0a1b-f905-41c4-b74b-99cb80fa34bc',
    'Thor''s Hammer Pendant',
    'Detailed stainless steel pendant shaped like Thor''s hammer, Mjölnir.',
    2800,
    '_e7e26434-cd4b-4350-bf69-7be88fdc51b6.jpg'
), (
    'c1a5bc52-7db7-48b6-bda3-492c54b83207',
    'Viking Drinking Horn',
    'Authentic drinking horn with intricate carvings, perfect for mead or ale.',
    3200,
    '_f426e77b-0ea7-4613-aaa5-5c4274f9d8f2.jpg'
), (
    '8b6ef5e7-563a-4b92-a4dd-45f9da1ff32e',
    'Rune Stone Coasters',
    'Set of four coasters featuring Viking rune stone designs.',
    1800,
    '_125d3722-b8b9-49ec-98dd-8a379475ba65.jpg'
), (
    '72a6b066-2fa7-42de-b44a-fb0f81ab0518',
    'Viking Axe Keychain',
    'Miniature replica of a Viking battle axe, perfect for a keychain.',
    1200,
    '_cae90c88-756e-4ab9-b429-ed9f325f906c.jpg'
), (
    '5b7d8db1-d5b4-4b1f-971f-d7fc94e4357b',
    'Viking Rune T-shirt',
    'Soft cotton t-shirt featuring Viking rune symbols and their meanings.',
    2900,
    '_adcef4f0-0de4-415f-b25d-91c03cea5e45.jpg'
), (
    '4fdab11a-7d0a-40ac-8c7d-62026886cd15',
    'Viking Horned Helmet Mug',
    'Ceramic mug shaped like a Viking horned helmet, perfect for your favorite beverage.',
    2400,
    '_f955e086-d781-4728-8b33-6a3ab81c1a9e.jpg'
), (
    '7e25b441-bb90-4dc3-b1f8-38a59db79e70',
    'Viking Rune Journal',
    'Leather-bound journal with Viking rune inscriptions on the cover.',
    3800,
    '_60af98f3-aa5a-4cb3-80a3-37ad1fa823ea.jpg'
), (
    '91f7973e-6880-4dcb-bfc8-9f67e742b181',
    'Viking Ship Model Kit',
    'Build-your-own Viking longship model kit, complete with sails and oars.',
    5000,
    '_3d45f00f-12fd-4a38-a7b6-fb38d8f421f7.jpg'
);
"