-- =============================================================
-- WFRP Combat Tracker — Migration v4
-- Version: 4.0
-- Description: Enable Row Level Security (RLS) on all
--              dictionary tables. Allow public read-only
--              access via Supabase Data API.
--              Write access only via backend connection string.
-- =============================================================

-- -------------------------------------------------------------
-- SKILLS
-- -------------------------------------------------------------
ALTER TABLE skills ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read skills"
    ON skills FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- TALENTS
-- -------------------------------------------------------------
ALTER TABLE talents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read talents"
    ON talents FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- TRAIT CATEGORIES
-- -------------------------------------------------------------
ALTER TABLE trait_categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read trait_categories"
    ON trait_categories FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- ITEM TRAITS
-- -------------------------------------------------------------
ALTER TABLE item_traits ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read item_traits"
    ON item_traits FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- WEAPON CATEGORIES
-- -------------------------------------------------------------
ALTER TABLE weapon_categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read weapon_categories"
    ON weapon_categories FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- WEAPONS
-- -------------------------------------------------------------
ALTER TABLE weapons ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read weapons"
    ON weapons FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- WEAPON ITEM TRAITS
-- -------------------------------------------------------------
ALTER TABLE weapon_item_traits ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read weapon_item_traits"
    ON weapon_item_traits FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- ARMOR CATEGORIES
-- -------------------------------------------------------------
ALTER TABLE armor_categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read armor_categories"
    ON armor_categories FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- ARMORS
-- -------------------------------------------------------------
ALTER TABLE armors ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read armors"
    ON armors FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- ARMOR ITEM TRAITS
-- -------------------------------------------------------------
ALTER TABLE armor_item_traits ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read armor_item_traits"
    ON armor_item_traits FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- ADVANTAGE ACTIONS
-- -------------------------------------------------------------
ALTER TABLE advantage_actions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read advantage_actions"
    ON advantage_actions FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- MOMENTUM ACTIONS
-- -------------------------------------------------------------
ALTER TABLE momentum_actions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read momentum_actions"
    ON momentum_actions FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- CONDITIONS
-- -------------------------------------------------------------
ALTER TABLE conditions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read conditions"
    ON conditions FOR SELECT
    USING (true);

-- -------------------------------------------------------------
-- HIT LOCATION
-- -------------------------------------------------------------
ALTER TABLE hit_location ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public read hit_location"
    ON hit_location FOR SELECT
    USING (true);
