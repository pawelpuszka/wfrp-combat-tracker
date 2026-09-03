-- =============================================================
-- WFRP Combat Tracker — Initial Migration
-- Version: 1.0
-- Description: Dictionary tables for skills, talents,
--              weapon traits, advantage actions and weapons
-- =============================================================

-- -------------------------------------------------------------
-- SKILLS
-- Stores all WFRP 4e skills with their descriptions.
-- governing_stat: which characteristic the skill is based on
-- is_grouped: e.g. "Broń biała (zwykła)" — skill has subtypes
-- is_basic: basic skills can be used untrained
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS skills (
    id             SERIAL PRIMARY KEY,
    name           VARCHAR(100)    NOT NULL UNIQUE,
    description    TEXT            NOT NULL,
    governing_stat VARCHAR(10),
    is_grouped     BOOLEAN         DEFAULT FALSE,
    is_basic       BOOLEAN         DEFAULT TRUE,
    source         VARCHAR(50)     DEFAULT 'WFRP4e Core'
);

-- -------------------------------------------------------------
-- ADVANTAGE ACTIONS
-- Actions available based on current advantage points.
-- advantage_cost: how many advantage points must be spent
-- action_type: type of action per Up in Arms rules
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS advantage_actions (
    id             SERIAL PRIMARY KEY,
    advantage_cost INT             NOT NULL,
    name           VARCHAR(200)    NOT NULL,
    description    TEXT            NOT NULL,
    action_type    VARCHAR(50)     CHECK (action_type IN ('specjalna', 'darmowa', 'ruch'))
);

-- -------------------------------------------------------------
-- TALENTS
-- Stores all WFRP 4e talents with their descriptions.
-- max_rank: maximum number of times talent can be taken
-- tests: which tests the talent affects
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS talents (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100)    NOT NULL UNIQUE,
    description TEXT            NOT NULL,
    max_rank    VARCHAR(50),
    tests       VARCHAR(200),
    source      VARCHAR(50)     DEFAULT 'WFRP4e Core'
);


-- -------------------------------------------------------------
-- ITEM TRAITS
-- Individual traits that can be assigned to items.
-- has_rating: some traits have a numeric rating e.g. "Obuchowa 1"
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS trait_categories (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL UNIQUE
);

-- Seed basic categories
INSERT INTO trait_categories (name) VALUES
    ('Pancerz'),
    ('Broń')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS item_traits (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL UNIQUE,
    description     TEXT            NOT NULL,
    category_id     INT             NOT NULL REFERENCES trait_categories(id),
    is_advantage    BOOLEAN         DEFAULT TRUE,
    has_rating      BOOLEAN         DEFAULT FALSE,
    trait_rating    INT,
    source          VARCHAR(50)     DEFAULT 'WFRP4e Core'
);


-- -------------------------------------------------------------
-- WEAPON CATEGORIES
-- Dictionary of weapon categories e.g. podstawowa, drzewcowa.
-- Separate table to allow easy extension.
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapon_categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Seed basic categories
INSERT INTO weapon_categories (name) VALUES
    ('Podstawowa'),
    ('Kawaleryjska'),
    ('Szermiercza'),
    ('Bijatyka'),
    ('Korbacze'),
    ('Parująca'),
    ('Drzewcowa'),
    ('Dwuręczna'),
    ('Amunicja tradycyjna'),
    ('Amunicja prochowa'),
    ('Prochowa'),
    ('Łuki'),
    ('Kusze'),
    ('Eksperymentalne'),
    ('Materiały wybuchowe'),
    ('Proce'),
    ('Miotana')
ON CONFLICT (name) DO NOTHING;

-- -------------------------------------------------------------
-- WEAPONS
-- Full weapon entries including stats and pricing.
-- damage: base damage value (integer)
-- uses_strength_bonus: if TRUE, app adds character's SB to damage
-- reach: melee weapons only e.g. "Średni", "Długi"
-- range_yards: ranged weapons only, in yards (integer)
-- availability: e.g. "Powszechna", "Rzadka"
-- encumbrance: item weight/bulk rating
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapons (
    id                   SERIAL PRIMARY KEY,
    name                 VARCHAR(100)    NOT NULL UNIQUE,
    category_id          INT             NOT NULL REFERENCES weapon_categories(id),
    damage               INT             NOT NULL,
    uses_strength_bonus  BOOLEAN         DEFAULT FALSE,
    reach                VARCHAR(50),
    range_yards          INT,
    availability         VARCHAR(50),
    price_gc             INT,
    price_ss             INT,
    price_bp             INT,
    encumbrance          INT             DEFAULT 0,
    source               VARCHAR(50)     DEFAULT 'WFRP4e Core',

    -- a weapon can be melee (reach) or ranged (range_yards), not both
    CONSTRAINT check_weapon_type CHECK (
        (reach IS NOT NULL AND range_yards IS NULL) OR
        (reach IS NULL AND range_yards IS NOT NULL) OR
        (reach IS NULL AND range_yards IS NULL)
    )
);



-- -------------------------------------------------------------
-- WEAPON_WEAPON_TRAITS (junction table)
-- Many-to-many: one weapon can have many traits,
-- one trait can belong to many weapons.
-- trait_rating: numeric value for rated traits e.g. "Obuchowa 1" → 1
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weapon_item_traits (
    weapon_id    INT NOT NULL REFERENCES weapons(id) ON DELETE CASCADE,
    trait_id     INT NOT NULL REFERENCES item_traits(id) ON DELETE CASCADE,
    PRIMARY KEY (weapon_id, trait_id)
);

-- ----------------------------------------------------------------
-- HIT_LOCATION
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS hit_location (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Seed basic categories
INSERT INTO hit_location (name) VALUES
    ('Głowa'),
    ('Korpus'),
    ('Lewa ręka'),
    ('Prawa ręka'),
    ('Lewa noga'),
    ('Prawa noga')
ON CONFLICT (name) DO NOTHING;

-- ----------------------------------------------------------------
-- ARMOR
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS armor_categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Seed basic categories
INSERT INTO armor_categories (name) VALUES
    ('Miękka skóra'),
    ('Skóra hartowana'),
    ('Kolczugi'),
    ('Płytowe')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS armors (
    id                   SERIAL PRIMARY KEY,
    name                 VARCHAR(100)    NOT NULL UNIQUE,
    category_id          INT             NOT NULL REFERENCES armor_categories(id),
    penalty              INT,
    penalty_stat         varchar(10),
    protected_location   varchar[], --jeden armor może chronić kilka lokacji    
    armor_points         INT,              
    availability         VARCHAR(50),
    price_gc             INT,
    price_ss             INT,
    price_bp             INT,
    encumbrance          INT             DEFAULT 0,
    source               VARCHAR(50)     DEFAULT 'WFRP4e Core'
);


-- CREATE TABLE armor_hit_locations (
--     armor_id        INT NOT NULL REFERENCES armors(id) ON DELETE CASCADE,
--     hit_location_id INT NOT NULL REFERENCES hit_location(id) ON DELETE CASCADE,
--     armor_points    INT NOT NULL,
--     PRIMARY KEY (armor_id, hit_location_id)
-- );


-- -------------------------------------------------------------
-- ARMOR_ITEM_TRAITS (junction table)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS armor_item_traits (
    armor_id    INT NOT NULL REFERENCES armors(id) ON DELETE CASCADE,
    trait_id     INT NOT NULL REFERENCES item_traits(id) ON DELETE CASCADE,
    PRIMARY KEY (armor_id, trait_id)
);


-- -------------------------------------------------------------------
-- CONDITIONS
-- -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS conditions (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    description TEXT
);  
