# PRD — WFRP Combat Tracker
# Product Requirements Document

**Wersja:** 1.0  
**Data:** 2026-06  
**Autor:** Paweł Puszka  
**Status:** Draft  

---

## 1. Cel produktu

WFRP Combat Tracker to aplikacja webowa wspierająca Mistrzów Gry prowadzących
sesje w systemie Warhammer Fantasy Roleplay 4. edycja (WFRP 4e). Walka w WFRP
jest mechanicznie złożona — wymaga jednoczesnego śledzenia inicjatywy, punktów
żywotności, punktów przewagi oraz cech broni i umiejętności wielu postaci naraz.
Aplikacja ma zastąpić kartki, kostki i tablice przy stole, dając MG jedno, szybkie
i czytelne narzędzie.

**Główny cel:** Skrócić czas obsługi walki i zmniejszyć liczbę błędów mechanicznych
podczas sesji.

---

## 2. Użytkownicy

| Persona | Opis | Główna potrzeba |
|---------|------|-----------------|
| **MG (Mistrz Gry)** | Doświadczony gracz RPG, prowadzi sesje WFRP 4e, ma ekran między sobą a graczami lub używa laptopa | Szybki dostęp do statystyk wszystkich uczestników walki na jednym ekranie |
| **Gracz (opcjonalnie)** | Może używać aplikacji do podglądu własnej postaci | Przeglądanie karty postaci, śledzenie żywotności |

**Uwaga:** Priorytetem jest widok MG. Widok gracza (single character) jest opcjonalnym rozszerzeniem.

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
- Licznik przewag oddzielnie dla BG i BN
- Na każdym wierszy uczestnika widoczne:
  - Nazwa postaci
  - Wynik inicjatywy
  - Aktualne / maksymalne punkty żywotności z paskiem postępu
  - Lista aktywnych kondycji (Ogłuszony, Ranny itd.)
  - Przycisk rozwinięcia do pełnej karty postaci

**Wskaźniki kolorystyczne żywotności:**

| Stan | Zakres | Kolor |
|------|--------|-------|
| Sprawny | >50% max Żyw | Zielony |
| Ranny | 25–50% max Żyw | Pomarańczowy |
| Krytyczny | <25% max Żyw | Czerwony |
| Obezwładniony | 0 Żyw | Szary |

### 3.2 Moduł: Punkty przewagi

Każda grupa biorąca udział w walce posiada licznik punktów przewagi (Advantage).

**Funkcjonalności:**

- Przycisk `+` i `−` przy grupie BG i BN
- Licznik nie schodzi poniżej 0
- Panel / tooltip „Co mogę zrobić za X punktów przewagi?" — wyświetla dostępne
  akcje na podstawie bieżącej liczby punktów (dane z bazy danych)
- Przycisk zbiorowego resetu przewagi dla wszystkich uczestników

**Mechanika WFRP 4e (dla dewelopera):**
- Przewaga ustalana jest ręcznie na podstawie przebiegu walki
- Traci się ją całkowicie koniec rundy

### 3.3 Moduł: Karta postaci

Uproszczona karta postaci — tylko informacje przydatne w walce. Nie jest to pełna
karta z systemu.

**Sekcja: Charakterystyki**

| Charakterystyka | Skrót | Opis |
|----------------|-------|------|
| Walka wręcz | WW | Testy ataków bronią białą |
| Ustrzelenie | US | Testy ataków dystansowych |
| Siła | S | Modyfikator obrażeń |
| Wytrzymałość | Wt | Odporność na obrażenia |
| Inicjatywa | I | Kolejność w walce |
| Zwinność | Zw | Uniki i testy ruchowe |
| Zręczność | Zr | Testy manualne |
| Inteligencja | Int | Umiejętność pojmowania i zapamiętywania |
| Siła Woli | SW | Możliwośći przeciwstawienia się złym wpływom |
| Ogłada | Ogd | W oczach innych BN |

**Sekcja: Żywotność**
- Maksymalna i bieżąca wartość (edytowalna)
- Pasek postępu z kolorem

**Sekcja: Umiejętności**
- Lista umiejętności z liczbą rozwinięć
- Na jakiej cesze oparta jest umiejętność
- Wartość końcowa umiejętności (wartość cechy + liczba rozwinięć)
- Po najechaniu kursorem na nazwę: tooltip z opisem (z bazy danych)

**Sekcja: Talenty**
- Lista talentów postaci
- Poziom talentu
- Po najechaniu kursorem na nazwę: tooltip z opisem (z bazy danych)

**Sekcja: Broń**
- Tabela broni z kolumnami: Nazwa, Grupa, Obrażenia, Zasięg/Długość, Cechy
- Po najechaniu na nazwę cechy broni: tooltip z opisem cechy (z bazy danych)

**Sekcja: Pancerz**
- Lista lokalizacji z wartością AP

### 3.4 Moduł: Zarządzanie postaciami (ładowanie sesji)

Ekran startowy / zarządzanie postaciami przed walką.

**Funkcjonalności:**

- Lista dostępnych postaci (z plików JSON na dysku)
- Wyszukiwanie po nazwie
- Filtrowanie: Bohaterowie Graczy / Przeciwnicy / Szablony
- Wybór postaci do bieżącej sesji walki
- Tworzenie nowej postaci (formularz → zapis do JSON)
- Edycja istniejącej postaci
- Usunięcie postaci
- Import postaci z szablonu (klonowanie z nową nazwą)

### 3.5 Moduł: Baza słownikowa (tylko admin)

Interfejs administracyjny dostępny tylko dla właściciela aplikacji.

**Funkcjonalności:**

- Przeglądanie umiejętności, talentów, cech broni, akcji przewagi w bazie
- Dodawanie i edycja wpisów (przez panel lub bezpośrednio w PostgreSQL)
- Eksport wybranej postaci z JSON do PostgreSQL (do dzielenia z innymi MG)

---

## 4. Zakres — czego aplikacja NIE robi

- ❌ Nie jest pełną kartą postaci (brak: rasy, profesji, języków, ekwipunku ogólnego, reputacji)
- ❌ Nie rzuca kośćmi automatycznie (MG rzuca fizycznie, wpisuje wynik)
- ❌ Nie obsługuje systemu magii (moduł przyszłościowy)
- ❌ Nie ma trybu dla graczy z edycją w czasie rzeczywistym (brak WebSocket na v1)
- ❌ Nie przechowuje danych postaci BG/BN w chmurze (tylko lokalnie)
- ❌ Nie wymaga rejestracji / logowania

---

## 5. Wymagania niefunkcjonalne

| Kategoria | Wymaganie |
|-----------|-----------|
| **Wydajność** | Tooltips ładują się <300ms; dane słownikowe cache'owane lokalnie |
| **Dostępność** | Aplikacja działa lokalnie bez internetu (poza tooltipami z DB) |
| **Skalowalność** | Każdy MG trzyma swoje dane lokalnie — brak kosztów skalowania |
| **Bezpieczeństwo** | Endpointy `/admin/*` chronione nagłówkiem `X-Admin-Secret` |
| **Czytelność kodu** | Kod komentowany po angielsku, zrozumiały dla początkującego Pythonisty |
| **Deployment** | Automatyczny deploy na Render.com po pushu do `main` |

---

## 6. Architektura danych

### 6.1 Podział odpowiedzialności

```
JSON (lokalny dysk)                 PostgreSQL (Supabase)
─────────────────────────────────   ─────────────────────────────────
Karty postaci BG i BN               Słownik umiejętności
Stan aktywnej walki (sesja)         Słownik talentów
Historia sesji                      Słownik cech broni
Szablony przeciwników               Tabela akcji przewagi

ZAPIS: aplikacja, zawsze            ZAPIS: tylko admin export
ODCZYT: zawsze lokalny              ODCZYT: tooltips, lista słownikowa
```

### 6.2 Format pliku postaci

Szczegółowy schemat JSON w `AGENTS.md` sekcja „Data Schemas".

---

## 7. API — lista endpointów

Szczegółowa tabela w `AGENTS.md` sekcja „API Endpoints".

Zasady:
- Wszystkie endpointy pod prefixem `/api/`
- Odpowiedzi w formacie JSON
- Kody HTTP: 200 OK, 201 Created, 404 Not Found, 422 Validation Error, 401 Unauthorized

---

## 8. UI / UX — wytyczne

### Główny widok walki (tracker)

```
┌─────────────────────────────────────────────────────────────────┐
│  WFRP Combat Tracker          Runda: 3    [Nowa walka] [Zapisz] │
├──────┬────────────────┬───────┬──────────┬────────┬────────────┤
│  #   │  Postać        │  Ini  │  Żyw     │ Przew. │  Akcje     │
├──────┼────────────────┼───────┼──────────┼────────┼────────────┤
│  ▶1  │ Ragnar Ż.P.    │  42   │ ████░ 11/14 │  [2] ─ + │ [↓] │
│   2  │ Wojownik Chaosu│  38   │ ██░░░  5/12 │  [0] ─ + │ [↓] │
│   3  │ Elspeth v.D.   │  35   │ █████  9/9  │  [1] ─ + │ [↓] │
│   4  │ Szczuroludź    │  29   │ ░░░░░  0/8  │  [0] ─ + │ [↓] │
├──────┴────────────────┴───────┴──────────┴────────┴────────────┤
│  [+ Dodaj uczestnika]                    [Reset przewagi]       │
└─────────────────────────────────────────────────────────────────┘
```

### Wytyczne wizualne

- Ciemny motyw (dark theme) — wygodny przy grze przy stole przy słabym oświetleniu
- Duże, czytelne przyciski `+` i `−` dla żywotności i przewagi
- Tooltip pojawia się po 200ms od najechania, znika po opuszczeniu
- Widok responsywny — działa na tablecie GM (min. 768px szerokości)
- Kondycje jako kolorowe badge (np. „Ogłuszony" na żółto)

---

## 9. Plan wdrożenia — etapy

### Etap 0 — Fundament (tydzień 1)
- [ ] Struktura projektu, Git, virtualenv
- [ ] FastAPI z pierwszym endpointem `/health`
- [ ] Połączenie z PostgreSQL (Supabase)
- [ ] Schemat bazy danych (migracja SQL)
- [ ] Podstawowe modele Pydantic

### Etap 1 — Karty postaci (tydzień 2–3)
- [ ] Schemat JSON postaci
- [ ] Endpointy CRUD dla postaci (`/api/characters`)
- [ ] Formularz tworzenia postaci (frontend)
- [ ] Wyświetlanie karty postaci

### Etap 2 — Słownik i tooltips (tydzień 3–4)
- [ ] Wypełnienie bazy: umiejętności, talenty, cechy broni
- [ ] Endpointy słownikowe (`/api/skills`, `/api/talents`, `/api/weapon-traits`)
- [ ] System tooltipów w Alpine.js z cachowaniem

### Etap 3 — Tracker walki (tydzień 5–6)
- [ ] Schemat JSON sesji walki
- [ ] Endpointy sesji (`/api/combat/sessions`)
- [ ] Widok trackera z inicjatywą i żywotnością
- [ ] System punktów przewagi z tabelą akcji

### Etap 4 — Polish i deployment (tydzień 7–8)
- [ ] Dark theme, responsywność
- [ ] Kondycje (dodawanie/usuwanie statusów)
- [ ] Deploy na Render.com
- [ ] Panel admina — eksport do PostgreSQL
- [ ] README i dokumentacja

---

## 10. Zależności zewnętrzne

| Usługa | Plan | Koszt | Do czego |
|--------|------|-------|---------|
| Supabase | Free tier | 0 PLN | PostgreSQL (słowniki) |
| Render.com | Free tier | 0 PLN | Hosting backendu |
| GitHub | Free | 0 PLN | Repozytorium, CI/CD |
| Alpine.js | CDN | 0 PLN | Frontend (brak build step) |

---

## 11. Otwarte pytania

1. Czy kondycje (Stunned, Bleeding itd.) mają być predefiniowaną listą czy dowolnym tekstem?
2. Czy tracker ma pamiętać historię obrażeń (kto ile zadał) w ramach sesji?
3. Czy szablony przeciwników mają być dostępne publicznie (w bazie) czy tylko lokalnie?
4. Czy aplikacja ma obsługiwać walki z wieloma grupami przeciwników (np. 3 Zbrojnych + 1 Mistrz Chaosu)?
