# WFRP Combat Tracker

Aplikacja webowa wspierająca Mistrzów Gry w prowadzeniu walk w systemie
**Warhammer Fantasy Roleplay 4. edycja**.

> Dokumentacja projektu: [`PRD.md`](PRD.md) | Kontekst dla AI: [`AGENTS.md`](AGENTS.md)

---

## Wymagania

- Python 3.11+
- Konto na [Supabase](https://supabase.com) (darmowe)
- Git

---

## Uruchomienie lokalne

```bash
# 1. Klonuj repozytorium
git clone https://github.com/twoj-login/wfrp-combat-tracker.git
cd wfrp-combat-tracker

# 2. Utwórz wirtualne środowisko
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Skonfiguruj zmienne środowiskowe
cp .env.example .env
# Edytuj .env — wpisz DATABASE_URL z Supabase

# 5. Utwórz tabele w bazie
python backend/db/migrate.py

# 6. Uruchom serwer deweloperski
uvicorn backend.main:app --reload --port 8000
```

Aplikacja dostępna pod: http://localhost:8000  
Dokumentacja API (Swagger): http://localhost:8000/docs

---

## Stack technologiczny

| Warstwa | Technologia |
|---------|-------------|
| Backend | Python 3.11 + FastAPI |
| Walidacja | Pydantic v2 |
| Baza danych (słowniki) | PostgreSQL na Supabase |
| Baza danych (postacie) | JSON na lokalnym dysku |
| Frontend | HTML + Alpine.js 3.x |
| Hosting | Render.com |

---

## Struktura projektu

```
wfrp-combat-tracker/
├── backend/          # FastAPI — logika serwera i API
├── frontend/         # HTML + Alpine.js — interfejs użytkownika
├── data/             # Lokalne pliki JSON (gitignore!)
├── PRD.md            # Wymagania produktowe
├── AGENTS.md         # Kontekst dla AI (Warp, Claude, etc.)
└── requirements.txt  # Zależności Python
```

Pełna struktura katalogów w [`AGENTS.md`](AGENTS.md).
