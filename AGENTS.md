# AGENTS.md — WFRP Combat Tracker

> This file is the primary context document for AI agents (Warp AI, Claude, Copilot, etc.)
> working on this project. Read this file in full before making any changes.

---

## Project Identity

**Name:** WFRP Combat Tracker
**Purpose:** A web application supporting Game Masters running combat sessions in
Warhammer Fantasy Roleplay 4th Edition (WFRP 4e) and 5th Edition (WFRP 5e).
Tracks initiative, wounds, Momentum (5e per-character), group advantage (4e Pod Bronią),
and provides quick access to character stats, skills, talents, and weapon traits.
**Target users:** Game Masters (MG in Polish). Not players. Not a full character builder.
**Language:** Application UI in Polish. Code and comments in English.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     BROWSER (GM's device)               │
│  HTML + Alpine.js frontend                              │
│  ├── Combat Tracker view (full party + enemies)         │
│  │   ├── Group advantage counters (BG / BN)             │
│  │   └── Momentum toggle per combatant (✓/✗)           │
│  ├── Character Card view (stats, skills, weapons)       │
│  └── Tooltip system (skills, talents, momentum actions) │
└──────────────┬──────────────────────────────────────────┘
               │ HTTP / JSON (REST API)
┌──────────────▼──────────────────────────────────────────┐
│                   BACKEND (FastAPI / Python)             │
│  ├── /api/characters     — load/save JSON characters    │
│  ├── /api/combat         — session state management     │
│  ├── /api/skills         — dictionary lookup (→ DB)     │
│  ├── /api/talents        — dictionary lookup (→ DB)     │
│  ├── /api/item-traits    — weapon/armor traits (→ DB)   │
│  ├── /api/advantage      — advantage actions (→ DB)     │
│  └── /api/momentum       — momentum actions (→ DB)      │
└──────────────┬──────────────────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────────────────────────────┐
│ LOCAL FILES │  │  PostgreSQL (Supabase)               │
│ /data/*.json│  │  Read-only dictionary tables:        │
│             │  │  - skills, talents                   │
│ Characters  │  │  - item_traits, trait_categories     │
│ (BG / BN)   │  │  - weapons, armors, categories       │
│ Session     │  │  - advantage_actions                 │
│ state       │  │  - momentum_actions                  │
│             │  │  Write: only via admin export tool   │
└─────────────┘  └──────────────────────────────────────┘
```

---

## Tech Stack

| Layer            | Technology              | Version / Notes                        |
|------------------|-------------------------|----------------------------------------|
| Backend language | Python                  | 3.11+                                  |
| Web framework    | FastAPI                 | Latest stable                          |
| Data validation  | Pydantic v2             | Models in `backend/schemas/`           |
| DB driver        | psycopg2-binary         | PostgreSQL only                        |
| ORM / queries    | SQLAlchemy 2.x          | Core preferred for PL/pgSQL            |
| Database         | PostgreSQL 15+          | Hosted on Supabase (free tier)         |
| Frontend         | HTML5 + Alpine.js 3.x   | No build step, CDN import              |
| CSS              | Custom CSS + CSS vars   | No framework, dark theme               |
| Local storage    | JSON files on disk      | `/data/` directory, see schema below   |
| Hosting          | Render.com              | Free tier, auto-deploy from GitHub     |

---

## Directory Structure

```
wfrp-combat-tracker/
│
├── AGENTS.md                    ← YOU ARE HERE
├── README.md                    ← Setup and run instructions
├── PRD.md                       ← Full product requirements
├── requirements.txt             ← Python dependencies
├── .env.example                 ← Environment variable template
├── .gitignore
│
├── backend/
│   ├── main.py                  ← FastAPI app entry point
│   ├── config.py                ← Settings (env vars, DB URL)
│   ├── db/
│   │   ├── connection.py        ← PostgreSQL connection pool
│   │   ├── migration_v1.sql     ← Initial schema
│   │   ├── migration_v2.sql     ← Momentum + for_combat flags
│   │   └── migrate.py           ← Migration runner script
│   ├── api/
│   │   └── routes/
│   │       ├── characters.py    ← CRUD for local JSON characters
│   │       ├── combat.py        ← Combat session management
│   │       ├── skills.py        ← GET /skills, GET /skills/{name}
│   │       ├── talents.py       ← GET /talents, GET /talents/{name}
│   │       ├── item_traits.py   ← GET /item-traits/{name}
│   │       ├── advantage.py     ← GET /advantage/actions
│   │       └── momentum.py      ← GET /momentum/actions
│   ├── models/
│   │   └── db_models.py         ← SQLAlchemy table definitions
│   ├── schemas/
│   │   ├── character_card.py    ← Pydantic: CharacterCard
│   │   ├── character_stats.py   ← Pydantic: CharacterStats (10 stats)
│   │   ├── skill_entry.py       ← Pydantic: SkillEntry
│   │   ├── talent_entry.py      ← Pydantic: TalentEntry
│   │   ├── weapon_entry.py      ← Pydantic: WeaponEntry
│   │   ├── armor_entry.py       ← Pydantic: ArmorEntry
│   │   └── combat.py            ← Pydantic: CombatSession, CombatantState
│   └── services/
│       ├── character_service.py ← Load/save JSON files
│       ├── combat_service.py    ← Initiative, wounds, momentum logic
│       └── export_service.py    ← JSON → PostgreSQL (admin only)
│
├── frontend/
│   ├── templates/
│   │   ├── index.html           ← Main combat tracker view
│   │   ├── character.html       ← Character card view
│   │   └── partials/
│   │       ├── combatant_row.html
│   │       └── tooltip.html
│   └── static/
│       ├── css/
│       │   └── main.css
│       └── js/
│           ├── combat.js        ← Alpine.js combat tracker logic
│           └── tooltips.js      ← Fetch descriptions from API
│
└── data/                        ← LOCAL ONLY, not in git
    ├── characters/
    │   ├── players/             ← BG (Bohaterowie Graczy)
    │   └── enemies/             ← BN / Przeciwnicy
    ├── sessions/                ← Active/saved combat sessions
    └── templates/               ← Reusable enemy archetypes
```

---

## Data Schemas

### Character JSON (`/data/characters/**/{uuid}.json`)

Files are named by UUID: `{character.id}.json`

```json
{
  "id": "uuid-v4",
  "name": "Ragnar Żelazna Pięść",
  "type": "player",
  "stats": {
    "WS":  45,
    "BS":  30,
    "S":   40,
    "T":   45,
    "I":   35,
    "Ag":  30,
    "Dex": 30,
    "Int": 35,
    "WP":  30,
    "Fel": 30,
    "fate":          3,
    "fortune":       3,
    "resilience":    2,
    "determination": 2
  },
  "skills": [
    { "name": "Uniki", "advances": 10 },
    { "name": "Broń biała (zwykła)", "advances": 5 }
  ],
  "talents": [
    { "name": "Błyskawiczny refleks", "rank": 1 }
  ],
  "weapons": [
    {
      "name": "Topór bojowy",
      "damage": 4,
      "uses_strength_bonus": true
    }
  ],
  "armor": [
    {
      "name": "Hełm skórzany",
      "armor_points": 1,
      "penalty": 0,
      "penalty_stat": null
    }
  ],
  "notes": ""
}
```

### Combat Session JSON (`/data/sessions/{uuid}.json`)

```json
{
  "session_id": "uuid-v4",
  "name": "Sesja — Karczma Pod Wisielcem",
  "round": 1,
  "group_advantage": {
    "players": 0,
    "enemies": 0
  },
  "combatants": [
    {
      "character_id": "uuid-v4",
      "name": "Ragnar Żelazna Pięść",
      "type": "player",
      "initiative_roll": 42,
      "current_wounds": 14,
      "momentum": false,
      "conditions": [],
      "is_active": true
    }
  ],
  "initiative_order": ["uuid1", "uuid2", "uuid3"],
  "created_at": "2024-01-15T19:00:00Z",
  "updated_at": "2024-01-15T21:30:00Z"
}
```

### PostgreSQL Dictionary Schema (current — after migration_v2)

```sql
-- Skills: for_combat flag for combat view filter
CREATE TABLE skills (
    id             SERIAL PRIMARY KEY,
    name           VARCHAR(100) NOT NULL UNIQUE,
    description    TEXT NOT NULL,
    governing_stat VARCHAR(10),
    is_grouped     BOOLEAN DEFAULT FALSE,
    is_basic       BOOLEAN DEFAULT TRUE,
    for_combat     BOOLEAN DEFAULT FALSE,
    source         VARCHAR(50) DEFAULT 'WFRP4e Core'
);

-- Talents: for_combat + requires_momentum flags
CREATE TABLE talents (
    id                SERIAL PRIMARY KEY,
    name              VARCHAR(100) NOT NULL UNIQUE,
    description       TEXT NOT NULL,
    max_rank          VARCHAR(50),
    tests             VARCHAR(200),
    for_combat        BOOLEAN DEFAULT FALSE,
    requires_momentum BOOLEAN DEFAULT FALSE,
    source            VARCHAR(50) DEFAULT 'WFRP4e Core'
);

-- Momentum actions (WFRP 5e)
CREATE TABLE momentum_actions (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    action_type VARCHAR(50) CHECK (action_type IN ('specjalna', 'darmowa', 'ruch'))
);

-- Advantage actions (Pod Bronią / WFRP 4e)
CREATE TABLE advantage_actions (
    id             SERIAL PRIMARY KEY,
    advantage_cost INT NOT NULL,
    name           VARCHAR(200) NOT NULL,
    description    TEXT NOT NULL,
    action_type    VARCHAR(50) CHECK (action_type IN ('specjalna', 'darmowa', 'ruch'))
);

-- Item traits (shared for weapons and armor)
CREATE TABLE trait_categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE  -- 'Broń', 'Pancerz'
);

CREATE TABLE item_traits (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    description  TEXT NOT NULL,
    category_id  INT NOT NULL REFERENCES trait_categories(id),
    is_advantage BOOLEAN DEFAULT TRUE,
    has_rating   BOOLEAN DEFAULT FALSE,
    trait_rating INT,
    source       VARCHAR(50) DEFAULT 'WFRP4e Core'
);

-- Weapon categories and weapons
CREATE TABLE weapon_categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE weapons (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR(100) NOT NULL UNIQUE,
    category_id         INT NOT NULL REFERENCES weapon_categories(id),
    damage              INT NOT NULL,
    uses_strength_bonus BOOLEAN DEFAULT FALSE,
    reach               VARCHAR(50),
    range_yards         INT,
    availability        VARCHAR(50),
    price_gc            INT,
    price_ss            INT,
    price_bp            INT,
    encumbrance         INT DEFAULT 0,
    source              VARCHAR(50) DEFAULT 'WFRP4e Core',
    CONSTRAINT check_weapon_type CHECK (
        (reach IS NOT NULL AND range_yards IS NULL) OR
        (reach IS NULL AND range_yards IS NOT NULL) OR
        (reach IS NULL AND range_yards IS NULL)
    )
);

CREATE TABLE weapon_item_traits (
    weapon_id INT NOT NULL REFERENCES weapons(id) ON DELETE CASCADE,
    trait_id  INT NOT NULL REFERENCES item_traits(id) ON DELETE CASCADE,
    PRIMARY KEY (weapon_id, trait_id)
);

-- Armor categories and armors
CREATE TABLE armor_categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE armors (
    id                 SERIAL PRIMARY KEY,
    name               VARCHAR(100) NOT NULL UNIQUE,
    category_id        INT NOT NULL REFERENCES armor_categories(id),
    penalty            INT,
    penalty_stat       VARCHAR(10),
    protected_location VARCHAR[],
    armor_points       INT,
    availability       VARCHAR(50),
    price_gc           INT,
    price_ss           INT,
    price_bp           INT,
    encumbrance        INT DEFAULT 0,
    source             VARCHAR(50) DEFAULT 'WFRP4e Core'
);

CREATE TABLE armor_item_traits (
    armor_id INT NOT NULL REFERENCES armors(id) ON DELETE CASCADE,
    trait_id INT NOT NULL REFERENCES item_traits(id) ON DELETE CASCADE,
    PRIMARY KEY (armor_id, trait_id)
);

-- Conditions dictionary
CREATE TABLE conditions (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100),
    description TEXT
);
```

---

## API Endpoints

| Method | Path                          | Description                           | Data source |
|--------|-------------------------------|---------------------------------------|-------------|
| GET    | `/api/characters/`            | List characters (name, type, id)      | JSON        |
| GET    | `/api/characters/{id}`        | Full character card                   | JSON        |
| POST   | `/api/characters/`            | Create character (save to JSON)       | JSON        |
| PUT    | `/api/characters/{id}`        | Update character                      | JSON        |
| DELETE | `/api/characters/{id}`        | Delete character file                 | JSON        |
| GET    | `/api/combat/sessions`        | List saved sessions                   | JSON        |
| GET    | `/api/combat/sessions/{id}`   | Load session state                    | JSON        |
| POST   | `/api/combat/sessions`        | Create new combat session             | JSON        |
| PUT    | `/api/combat/sessions/{id}`   | Update session (wounds, momentum)     | JSON        |
| GET    | `/api/skills`                 | List all skills                       | PostgreSQL  |
| GET    | `/api/skills/{name}`          | Skill description (tooltip)           | PostgreSQL  |
| GET    | `/api/talents`                | List all talents                      | PostgreSQL  |
| GET    | `/api/talents/{name}`         | Talent description (tooltip)          | PostgreSQL  |
| GET    | `/api/item-traits/{name}`     | Item trait description (tooltip)      | PostgreSQL  |
| GET    | `/api/advantage/actions`      | Advantage actions list (Pod Bronią)   | PostgreSQL  |
| GET    | `/api/momentum/actions`       | Momentum actions list (WFRP 5e)       | PostgreSQL  |
| POST   | `/api/admin/export/{id}`      | Export character JSON → PostgreSQL    | Both        |

---

## Core Business Logic

### Initiative Order
1. GM sets initiative manually per combatant (based on I characteristic)
2. Stored in session JSON, sorted descending
3. Active combatant highlighted in tracker
4. Round increments when all combatants have acted

### Wounds Tracking
- `current_wounds` decremented manually by GM
- Never goes below 0
- Color indicator: green (>50%), orange (25–50%), red (<25%), grey (0 = incapacitated)
- Max wounds (Vitality) calculated from character stats — not stored, computed at runtime

### Momentum (WFRP 5e)
- Per-character boolean: `momentum: true/false` in session JSON
- Toggled manually by GM
- Tooltip on hover shows:
  1. Static actions from `momentum_actions` table
  2. Character's own talents where `requires_momentum = TRUE`
- Does NOT stack — binary state only

### Group Advantage (Pod Bronią / WFRP 4e)
- Two group counters: `group_advantage.players` and `group_advantage.enemies`
- Set manually, minimum 0
- Reset to 0 at end of each round
- `/api/advantage/actions` returns available actions per point level

### Tooltip System
- On hover over skill/talent/trait name → fetch from `/api/{resource}/{name}`
- Response cached in Alpine.js `$store.cache` to avoid repeated DB calls
- Momentum tooltip also fetches character's `requires_momentum` talents dynamically

---

## Environment Variables

```bash
# .env (copy from .env.example, never commit)
DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
ENVIRONMENT=development
DATA_DIR=./data
ADMIN_SECRET=change_me
```

---

## Development Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill env file
cp .env.example .env

# 3. Run migrations
python -m backend.db.migrate backend/db/migration_v1.sql
python -m backend.db.migrate backend/db/migration_v2.sql

# 4. Start dev server
uvicorn backend.main:app --reload --port 8000

# 5. Open in browser
open http://localhost:8000
```

---

## Key Constraints for AI Agents

1. **Never store character data in PostgreSQL** — only JSON files. PostgreSQL is for
   dictionaries only (skills, talents, item traits, weapons, armors, advantage/momentum actions).

2. **Character files are named by UUID** — `{character.id}.json`. Never use character
   name as filename.

3. **Never break the JSON schema** — character and session schemas defined above are
   authoritative. Use Pydantic models in `schemas/` to validate all data.

4. **Momentum is per-character boolean** — stored in session JSON `combatants[].momentum`,
   never in the character JSON (it's a combat state, not a character property).

5. **Group advantage is per-session** — stored in session JSON `group_advantage.players`
   and `group_advantage.enemies`. Never per individual combatant.

6. **All dictionary reads are cached** — always check Alpine.js `$store.cache` before
   fetching from API.

7. **Admin endpoints are protected** — `/api/admin/*` requires `X-Admin-Secret` header.

8. **Frontend is Alpine.js only** — no React, Vue, or build toolchain.

9. **PL/pgSQL for complex queries** — joins across 3+ tables go into database functions.

10. **Polish UI, English code** — stat names in UI: WS→WW, BS→US, S, T→Wt, I, Ag→Zw,
    Dex→Zr, Int, WP→SW, Fel→Ogd. Conditions and UI labels in Polish. Code in English.

11. **This is a learning project** — readable, well-commented code over clever
    optimizations. Each module understandable by a Python beginner.
