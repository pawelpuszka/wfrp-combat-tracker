# AGENTS.md — WFRP Combat Tracker

> This file is the primary context document for AI agents (Warp AI, Claude, Copilot, etc.)
> working on this project. Read this file in full before making any changes.

---

## Project Identity

**Name:** WFRP Combat Tracker
**Purpose:** A web application supporting Game Masters running combat sessions in
Warhammer Fantasy Roleplay 4th Edition (WFRP 4e). Tracks initiative, wounds,
advantage points, and provides quick access to character stats, skills, talents,
and weapon traits.
**Target users:** Game Masters (MG in Polish). Not players. Not a full character builder.
**Language:** Application UI in Polish. Code and comments in English.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     BROWSER (GM's device)               │
│  HTML + Alpine.js frontend                              │
│  ├── Combat Tracker view (full party + enemies)         │
│  ├── Character Card view (stats, skills, weapons)       │
│  └── Advantage Point counter per combatant              │
└──────────────┬──────────────────────────────────────────┘
               │ HTTP / JSON (REST API)
┌──────────────▼──────────────────────────────────────────┐
│                   BACKEND (FastAPI / Python)             │
│  ├── /api/characters   — load/save JSON character files │
│  ├── /api/combat       — session state management       │
│  ├── /api/skills       — dictionary lookup (→ DB)       │
│  ├── /api/talents      — dictionary lookup (→ DB)       │
│  └── /api/weapon-traits— dictionary lookup (→ DB)       │
└──────────────┬──────────────────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────────────────────────────┐
│ LOCAL FILES │  │  PostgreSQL (Supabase)               │
│ /data/*.json│  │  Read-only dictionary tables:        │
│             │  │  - skills, talents, weapon_traits    │
│ Characters  │  │  - advantage_actions                 │
│ (BG / BN)   │  │                                      │
│ Session     │  │  Write: only via admin export tool   │
│ state       │  └──────────────────────────────────────┘
└─────────────┘
```

---

## Tech Stack

| Layer            | Technology              | Version / Notes                        |
|------------------|-------------------------|----------------------------------------|
| Backend language | Python                  | 3.11+                                  |
| Web framework    | FastAPI                 | Latest stable                          |
| Data validation  | Pydantic v2             | Models in `backend/schemas/`           |
| DB driver        | psycopg2-binary         | PostgreSQL only                        |
| ORM / queries    | SQLAlchemy 2.x          | Core (not ORM) preferred for PL/pgSQL  |
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
│   │   └── queries.py           ← Raw SQL / PL/pgSQL calls
│   ├── api/
│   │   └── routes/
│   │       ├── characters.py    ← CRUD for local JSON characters
│   │       ├── combat.py        ← Combat session management
│   │       ├── skills.py        ← GET /skills, GET /skills/{name}
│   │       ├── talents.py       ← GET /talents, GET /talents/{name}
│   │       └── weapon_traits.py ← GET /weapon-traits/{name}
│   ├── models/
│   │   └── db_models.py         ← SQLAlchemy table definitions
│   ├── schemas/
│   │   ├── character.py         ← Pydantic: CharacterCard, WeaponEntry
│   │   ├── combat.py            ← Pydantic: CombatSession, CombatantState
│   │   └── dictionary.py        ← Pydantic: Skill, Talent, WeaponTrait
│   └── services/
│       ├── character_service.py ← Load/save JSON files
│       ├── combat_service.py    ← Initiative, wounds, advantage logic
│       └── export_service.py    ← JSON → PostgreSQL export (admin only)
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
│           └── tooltips.js      ← Fetch skill/talent descriptions from API
│
└── data/                        ← LOCAL ONLY, not in git (see .gitignore)
    ├── characters/
    │   ├── players/             ← BG (Bohaterowie Graczy)
    │   │   └── example_ragnar.json
    │   └── enemies/             ← BN / Przeciwnicy
    │       └── example_chaos_warrior.json
    ├── sessions/                ← Active/saved combat sessions
    │   └── example_session.json
    └── templates/               ← Reusable enemy archetypes
        └── chaos_warrior_template.json
```

---

## Data Schemas

### Character JSON (`/data/characters/players/*.json`)

```json
{
  "id": "uuid-v4",
  "name": "Ragnar Żelazna Pięść",
  "type": "player",
  "stats": {
    "WW": 45,
    "US": 30,
    "S": 40,
    "Wt": 45,
    "I": 35,
    "Zw": 30,
    "Zr": 30,
    "Int": 35,
    "SW": 30,
    "Ogd": 30
  },
  "wounds": {
    "max": 14,
    "current": 14
  },
  "advantage": 0,
  "basic skills": [
    { "name": "Uniki", "advances": 10 },
    { "name": "Broń biała (zwykła)", "advances": 5 }
  ],
  "talents": [
    { "name": "Błyskawiczny refleks" }
  ],
  "weapons": [
    {
      "name": "Topór bojowy",
      "group": "Broń biała",
      "damage": "S+4",
      "reach": "Średni",
      "traits": ["Obuchowa 1", "Parująca"]
    }
  ],
  "armour": [
    {
      "location": "Głowa",
      "ap": 1,
      "name": "Hełm skórzany"
    }
  ],
  "notes": ""
}
```

### Combat Session JSON (`/data/sessions/*.json`)

```json
{
  "session_id": "uuid-v4",
  "name": "Sesja 2024-01-15 — Karczma Pod Wisielcem",
  "round": 1,
  "combatants": [
    {
      "character_id": "uuid-v4",
      "name": "Ragnar Żelazna Pięść",
      "type": "player",
      "initiative_roll": 42,
      "current_wounds": 14,
      "advantage": 0,
      "conditions": [],
      "is_active": true
    }
  ],
  "initiative_order": ["uuid1", "uuid2", "uuid3"],
  "created_at": "2024-01-15T19:00:00Z",
  "updated_at": "2024-01-15T21:30:00Z"
}
```

### PostgreSQL Dictionary Schema

```sql
-- Skills dictionary
CREATE TABLE skills (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    governing_stat VARCHAR(10),
    is_grouped  BOOLEAN DEFAULT FALSE,
    is_basic	BOOLEAN DEFAULT TRUE,
    source      VARCHAR(50) DEFAULT 'WFRP4e Core'
);

-- Talents dictionary
CREATE TABLE talents (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    max_rank    VARCHAR(50),
    tests       VARCHAR(200),
    source      VARCHAR(50) DEFAULT 'WFRP4e Core'
);

-- Weapon traits dictionary
CREATE TABLE weapon_traits (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    has_rating  BOOLEAN DEFAULT FALSE,
    source      VARCHAR(50) DEFAULT 'WFRP4e Core'
);

-- Advantage actions table
CREATE TABLE advantage_actions (
    id          SERIAL PRIMARY KEY,
    min_advantage INT NOT NULL,
    name        VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    action_type VARCHAR(50)
);
```

---

## API Endpoints

| Method | Path                        | Description                          | Data source |
|--------|-----------------------------|--------------------------------------|-------------|
| GET    | `/api/characters`           | List all local character files       | JSON        |
| GET    | `/api/characters/{id}`      | Load one character card              | JSON        |
| POST   | `/api/characters`           | Create new character (saves to JSON) | JSON        |
| PUT    | `/api/characters/{id}`      | Update character (saves to JSON)     | JSON        |
| GET    | `/api/combat/sessions`      | List saved sessions                  | JSON        |
| GET    | `/api/combat/sessions/{id}` | Load session state                   | JSON        |
| POST   | `/api/combat/sessions`      | Create new combat session            | JSON        |
| PUT    | `/api/combat/sessions/{id}` | Update session (wounds, advantage)   | JSON        |
| GET    | `/api/skills`               | List all skills                      | PostgreSQL  |
| GET    | `/api/skills/{name}`        | Get skill description (for tooltip)  | PostgreSQL  |
| GET    | `/api/talents`              | List all talents                     | PostgreSQL  |
| GET    | `/api/talents/{name}`       | Get talent description (for tooltip) | PostgreSQL  |
| GET    | `/api/weapon-traits/{name}` | Get weapon trait description         | PostgreSQL  |
| GET    | `/api/advantage/actions`    | List all advantage actions           | PostgreSQL  |
| POST   | `/api/admin/export/{id}`    | Export character JSON → PostgreSQL   | Both        |

---

## Core Business Logic

### Initiative Order
1. Each combatant has set Initiative manualy (I characteristic value used as base)
2. Results stored in session JSON, sorted descending
3. Active combatant highlighted in tracker
4. Round increments when all combatants have acted

### Wounds Tracking
- `current_wounds` decremented manualy
- Never goes below 0
- Color indicator: green (>50%), orange (25–50%), red (<25%), grey (0 = incapacitated)

### Advantage Points
- Each group of characters (players and enemies) has `advantage` counter (integer, min 0)
- The counter is set manualy for each group
- Reset to 0 when round ends.
- `/api/advantage/actions` returns what each advantage level enables
- Tooltip/panel shows available actions based on current advantage value

### Weapon Trait Tooltips
- On hover over trait name → fetch `/api/weapon-traits/{name}`
- Response cached in Alpine.js store to avoid repeated DB calls
- Same pattern for skills and talents on character card

---

## Environment Variables

```bash
# .env (copy from .env.example, never commit)
DATABASE_URL=postgresql://user:password@db.supabase.co:5432/postgres
ENVIRONMENT=development       # development | production
DATA_DIR=./data               # path to local JSON storage
ADMIN_SECRET=change_me        # protects /api/admin/* endpoints
```

---

## Development Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill env file
cp .env.example .env

# 3. Run database migrations (first time)
python backend/db/migrate.py

# 4. Start dev server
uvicorn backend.main:app --reload --port 8000

# 5. Open in browser
open http://localhost:8000
```

---

## Key Constraints for AI Agents

1. **Never store character data in PostgreSQL** — only JSON files. PostgreSQL is for
   dictionaries (skills, talents, weapon traits, advantage actions) only.

2. **Never break the JSON schema** — character and session JSON schemas are defined
   above and must be respected. Use Pydantic models in `schemas/` to validate.

3. **All dictionary reads are cached** — when fetching from PostgreSQL for tooltips,
   always check the Alpine.js `$store.cache` first.

4. **Admin endpoints are protected** — `/api/admin/*` requires `X-Admin-Secret` header
   matching `ADMIN_SECRET` env var.

5. **Frontend is Alpine.js only** — do not introduce React, Vue, or any build toolchain.
   Keep it CDN-importable and simple.

6. **PL/pgSQL for complex queries** — if a query involves joins across 3+ tables or
   complex logic, put it in a database function, not Python.

7. **Polish WFRP terminology** — use Polish stat names in UI (WW, US, S, Wt, I, Zw)
   and Polish condition names. English in code only.

8. **This is a learning project** — prefer readable, well-commented code over clever
   optimizations. Each module should be understandable by a Python beginner.
