# PRD — WFRP Combat Tracker
# Product Requirements Document

**Wersja:** 1.2  
**Data:** 2026-09  
**Autor:** Paweł Puszka  
**Status:** Draft  

---

## Changelog

| Wersja | Zmiana |
|--------|--------|
| 1.0 | Wersja inicjalna |
| 1.1 | Przewagi grupowe (Up in Arms), pełne 10 charakterystyk WFRP 4e |
| 1.2 | Dodano mechanikę Momentum (WFRP 5e), aplikacja obsługuje obie edycje |

---

## 1. Cel produktu

WFRP Combat Tracker to aplikacja webowa wspierająca Mistrzów Gry prowadzących
sesje w systemie Warhammer Fantasy Roleplay. Aplikacja obsługuje dwie edycje:
**4. edycję** (mechanika przewagi grupowej z dodatku Pod Bronią) oraz
**5. edycję** (mechanika Momentum per postać).

Walka w WFRP jest mechanicznie złożona — wymaga jednoczesnego śledzenia inicjatywy,
punktów żywotności, stanu Momentum oraz cech broni i umiejętności wielu postaci naraz.
Aplikacja ma zastąpić kartki, kostki i tablice przy stole, dając MG jedno, szybkie
i czytelne narzędzie.

**Główny cel:** Skrócić czas obsługi walki i zmniejszyć liczbę błędów mechanicznych
podczas sesji.

---

## 2. Użytkownicy

| Persona | Opis | Główna potrzeba |
|---------|------|-----------------|
| **MG (Mistrz Gry)** | Doświadczony gracz RPG, prowadzi sesje WFRP 4e lub 5e, używa laptopa lub tabletu przy stole | Jeden ekran z całą walką: inicjatywa, żywotność, Momentum, przewaga grupowa, statystyki |
| **Gracz (opcjonalnie)** | Może używać aplikacji do podglądu własnej postaci | Przeglądanie karty postaci, śledzenie żywotności |

**Uwaga:** Priorytetem jest widok MG. Widok gracza jest opcjonalnym rozszerzeniem.

---

## 3. Zakres — co aplikacja robi

### 3.1 Moduł: Tracker walki (widok MG)

Główny widok aplikacji. Wyświetla wszystkich uczestników bieżącej walki na jednym
ekranie, posortowanych według inicjatywy.

**Funkcjonalności:**

- Wyświetlanie listy uczestników walki (BG + BN) posortowanej według inicjatywy
- Wizualne wyróżnienie aktywnej postaci (czyja tura)
- Przycisk „Następna tura" — przesuwa aktywną postać
- Licznik rund
- Licznik przewag grupowych oddzielnie dla BG i BN (mechanika Pod Bronią / 4ed)
- Na każdym wierszu uczestnika widoczne:
  - Nazwa postaci
  - Wynik inicjatywy
  - Aktualne / maksymalne punkty żywotności z paskiem postępu
  - Znacznik Momentum (✓/✗) per postać (mechanika 5ed)
  - Lista aktywnych kondycji (Ogłuszony, Ranny itd.)
  - Przycisk rozwinięcia do pełnej karty postaci

**Wskaźniki kolorystyczne żywotności:**

| Stan | Zakres | Kolor |
|------|--------|-------|
| Sprawny | >50% max Żyw | Zielony |
| Ranny | 25–50% max Żyw | Pomarańczowy |
| Krytyczny | <25% max Żyw | Czerwony |
| Obezwładniony | 0 Żyw | Szary |

### 3.2 Moduł: Momentum (WFRP 5ed)

Każdy uczestnik walki (BG i BN) może posiadać Momentum — stan binarny (masz / nie masz).

**Funkcjonalności:**

- Znacznik Momentum per postać — przełącznik ✓/✗
- Tooltip po najechaniu na znacznik — wyświetla co można zrobić posiadając Momentum:
  - Stałe akcje z bazy danych (`momentum_actions`)
  - Talenty postaci które wymagają Momentum (`requires_momentum = TRUE`) — dynamiczne,
    zależne od talentów konkretnej postaci

**Mechanika WFRP 5e:**
- Momentum zdobywa się wygrywając test przeciwstawny w walce wręcz
- Momentum nie stackuje się — postać ma je albo nie
- Momentum można wydać (utracić) na:
  - Utrzymanie Przewagi (Advantage) do testów Walki Wręcz
  - Dodatkowy atak drugą bronią
  - Aktywację talentów (Furious Assault, Shieldsman, Disarm, Drilled)
  - Bezpieczne zerwanie zwarcia (Disengage) bez testu
  - Przekazanie sojusznikowi (darmowa akcja + test Dowodzenia)
  - Przerwanie stanu walki w zwarciu (In-fighting)

### 3.3 Moduł: Punkty przewagi grupowej (Pod Bronią / WFRP 4ed)

Każda grupa biorąca udział w walce posiada licznik punktów przewagi (Advantage).

**Funkcjonalności:**

- Dwa liczniki grupowe: jeden dla BG, jeden dla BN
- Przycisk `+` i `−` dla każdej grupy
- Licznik nie schodzi poniżej 0
- Panel / tooltip „Co mogę zrobić za X punktów przewagi?" — wyświetla dostępne
  akcje na podstawie bieżącej liczby punktów (dane z bazy danych)
- Przycisk zbiorowego resetu przewagi dla obu grup

**Mechanika Pod Bronią (4ed):**
- Przewaga ustalana ręcznie przez MG na podstawie przebiegu walki
- Resetowana na końcu każdej rundy

### 3.4 Moduł: Karta postaci

Uproszczona karta postaci — tylko informacje przydatne w walce.

**Sekcja: Charakterystyki (WFRP 4e/5e)**

| Skrót (kod) | Nazwa PL | Zastosowanie w walce |
|-------------|----------|----------------------|
| WS | Walka Wręcz | Testy ataków bronią białą |
| BS | Ustrzelenie | Testy ataków dystansowych |
| S | Siła | Modyfikator obrażeń |
| T | Wytrzymałość | Odporność na obrażenia |
| I | Inicjatywa | Kolejność w walce |
| Ag | Zwinność | Uniki i testy ruchowe |
| Dex | Zręczność | Testy manualne |
| Int | Inteligencja | Umiejętność pojmowania |
| WP | Siła Woli | Odporność na złe wpływy |
| Fel | Ogłada | Wpływ na inne postacie |

Dodatkowe pola: `fate`, `fortune`, `resilience`, `determination`

**Sekcja: Żywotność**
- Maksymalna wartość (wyliczana na podstawie charakterystyk — Vitality)
- Bieżąca wartość (edytowalna w trakcie walki)
- Pasek postępu z kolorem

**Sekcja: Umiejętności**
- Lista umiejętności z liczbą rozwinięć
- Na jakiej cesze oparta jest umiejętność
- Wartość końcowa (wartość cechy + rozwinięcia)
- Oznaczenie `for_combat` — tylko bojowe umiejętności w widoku walki
- Tooltip po najechaniu — opis z bazy danych

**Sekcja: Talenty**
- Lista talentów postaci z poziomem (rank)
- Oznaczenie `for_combat` — tylko bojowe talenty w widoku walki
- Oznaczenie `requires_momentum` — talent wymaga Momentum do aktywacji
- Tooltip po najechaniu — opis z bazy danych

**Sekcja: Broń**
- Tabela: Nazwa, Obrażenia (+ czy dodaje bonus z Siły)
- Tooltip po najechaniu na cechę broni — opis z bazy danych

**Sekcja: Pancerz**
- Lista lokalizacji z wartością AP i karą pancerza

### 3.5 Moduł: Zarządzanie postaciami

Ekran startowy / zarządzanie postaciami przed walką.

**Funkcjonalności:**

- Lista dostępnych postaci z lokalnych plików JSON
- Wyszukiwanie po nazwie
- Filtrowanie: Bohaterowie Graczy / Przeciwnicy / Szablony
- Wybór postaci do bieżącej sesji walki
- Tworzenie nowej postaci (formularz → zapis do JSON)
- Edycja istniejącej postaci
- Usunięcie postaci
- Import z szablonu (klonowanie z nową nazwą)

### 3.6 Moduł: Baza słownikowa (tylko admin)

**Funkcjonalności:**

- Przeglądanie słowników w bazie danych
- Dodawanie i edycja wpisów
- Eksport postaci z JSON do PostgreSQL

---

## 4. Zakres — czego aplikacja NIE robi

- ❌ Nie jest pełną kartą postaci (brak: rasy, profesji, języków, reputacji)
- ❌ Nie rzuca kośćmi automatycznie
- ❌ Nie obsługuje systemu magii (moduł przyszłościowy)
- ❌ Nie ma trybu wieloosobowego w czasie rzeczywistym (brak WebSocket na v1)
- ❌ Nie przechowuje danych postaci BG/BN w chmurze (tylko lokalnie)
- ❌ Nie wymaga rejestracji / logowania

---

## 5. Wymagania niefunkcjonalne

| Kategoria | Wymaganie |
|-----------|-----------|
| **Wydajność** | Tooltips ładują się <300ms; dane słownikowe cache'owane lokalnie |
| **Dostępność** | Tracker walki działa bez internetu; tooltips wymagają połączenia |
| **Skalowalność** | Każdy MG trzyma swoje dane lokalnie — zero kosztów skalowania |
| **Bezpieczeństwo** | Endpointy `/admin/*` chronione nagłówkiem `X-Admin-Secret` |
| **Czytelność kodu** | Komentowany po angielsku, zrozumiały dla początkującego Pythonisty |
| **Deployment** | Automatyczny deploy na Render.com po pushu do `main` |

---

## 6. Architektura danych

### 6.1 Podział odpowiedzialności

```
JSON (lokalny dysk)                 PostgreSQL (Supabase)
─────────────────────────────────   ──────────────────────────────────
Karty postaci BG i BN               Słownik umiejętności (+ for_combat)
Stan aktywnej walki (sesja)         Słownik talentów (+ for_combat,
Historia sesji                        requires_momentum)
Szablony przeciwników               Słownik cech przedmiotów (item_traits)
                                    Tabela akcji przewagi (advantage_actions)
                                    Tabela akcji Momentum (momentum_actions)
                                    Słownik broni i pancerzy

ZAPIS: aplikacja, zawsze            ZAPIS: tylko admin export
ODCZYT: zawsze lokalny              ODCZYT: tooltips, lista słownikowa
```

### 6.2 Szkic głównego widoku trackera

```
┌──────────────────────────────────────────────────────────────────────┐
│  WFRP Combat Tracker               Runda: 3   [Nowa walka] [Zapisz] │
├─────────────────────────────────────┬────────────────────────────────┤
│  Przewaga BG:  [−]  2  [+]  [ℹ]   │  Przewaga BN:  [−]  0  [+] [ℹ]│
├──────┬──────────────────┬───────┬───┴──────────────┬───────────────┤
│  #   │  Postać          │  Ini  │  Żywotność       │  Akcje        │
├──────┼──────────────────┼───────┼──────────────────┼───────────────┤
│  ▶1  │ 🟢 Ragnar Ż.P.  │  42   │ ████░░  11/14 [M✓]│ [Kond.▾] [↓] │
│   2  │ 🔴 Wojow. Chaosu│  38   │ ██░░░░   5/12 [M✗]│ [Kond.▾] [↓] │
│   3  │ 🟢 Elspeth v.D. │  35   │ █████░   9/9  [M✓]│ [Kond.▾] [↓] │
│   4  │ ⚫ Szczuroludź   │  29   │ ░░░░░░   0/8  [M✗]│ [Kond.▾] [↓] │
├──────┴──────────────────┴───────┴──────────────────┴───────────────┤
│  [+ Dodaj uczestnika]           [Reset przewag]  [Następna tura ▶] │
└──────────────────────────────────────────────────────────────────────┘

[M✓] = postać posiada Momentum (tooltip z dostępnymi akcjami)
[M✗] = postać nie posiada Momentum
```

---

## 7. API — lista endpointów

Zasady:
- Wszystkie endpointy pod prefixem `/api/`
- Odpowiedzi w formacie JSON
- Kody HTTP: 200 OK, 201 Created, 404 Not Found, 422 Validation Error, 401 Unauthorized

Szczegółowa tabela w `AGENTS.md` sekcja „API Endpoints".

---

## 8. Plan wdrożenia — etapy

### Etap 0 — Fundament ✅
- [x] Struktura projektu, Git, virtualenv
- [x] FastAPI z endpointem `/health`
- [x] Połączenie z PostgreSQL (Supabase)
- [x] Schemat bazy danych (migration_v1.sql)
- [x] Podstawowe modele Pydantic

### Etap 1 — Karty postaci 🔄
- [x] Modele Pydantic (CharacterCard, CharacterStats, itd.)
- [x] CharacterService (zapis/odczyt JSON)
- [x] Endpointy GET /api/characters/, GET /api/characters/{id}
- [x] Endpoint POST /api/characters/
- [ ] Endpoint PUT /api/characters/{id}
- [ ] Endpoint DELETE /api/characters/{id}

### Etap 2 — Słownik i tooltips
- [ ] migration_v2.sql (momentum_actions, for_combat, requires_momentum)
- [ ] Wypełnienie bazy: umiejętności, talenty, cechy broni, akcje Momentum
- [ ] Endpointy słownikowe
- [ ] System tooltipów w Alpine.js z cachowaniem

### Etap 3 — Tracker walki
- [ ] Schemat JSON sesji walki (z group_advantage i momentum per postać)
- [ ] Endpointy sesji (`/api/combat/sessions`)
- [ ] Widok trackera z inicjatywą i żywotnością
- [ ] Znacznik Momentum per postać z tooltipem
- [ ] Liczniki przewagi grupowej BG/BN

### Etap 4 — Polish i deployment
- [ ] Dark theme, responsywność
- [ ] Kondycje (dodawanie/usuwanie statusów)
- [ ] Deploy na Render.com
- [ ] Panel admina
- [ ] README i dokumentacja

---

## 9. Zależności zewnętrzne

| Usługa | Plan | Koszt | Do czego |
|--------|------|-------|---------|
| Supabase | Free tier | 0 PLN | PostgreSQL (słowniki) |
| Render.com | Free tier | 0 PLN | Hosting backendu |
| GitHub | Free | 0 PLN | Repozytorium, CI/CD |
| Alpine.js | CDN | 0 PLN | Frontend |

---

## 10. Otwarte pytania

1. Czy kondycje mają być predefiniowaną listą czy dowolnym tekstem?
2. Czy tracker ma pamiętać historię obrażeń w ramach sesji?
3. Czy szablony przeciwników mają być dostępne publicznie (w bazie)?
4. Czy aplikacja ma obsługiwać walki z wieloma grupami przeciwników?
5. Czy wspierać przełącznik edycji (4ed / 5ed) w ustawieniach sesji?
