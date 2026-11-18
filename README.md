# Football Analytics

Hurtownia danych o meczach piłkarskich z pięciu czołowych lig europejskich, zasilana procesem ETL z surowych plików CSV do bazy MySQL, wraz z analizą statystyczną załadowanych danych.

## Zbiór danych

Projekt korzysta ze zbioru **[Club Football Match Data (2000–2025)](https://www.kaggle.com/datasets/adamgbor/club-football-match-data-2000-2025)** autorstwa Adama Gábora (licencja MIT). Do hurtowni trafiają mecze z lig I1, SP1, D1, F1 i N1 rozegrane od 1 sierpnia 2020 do 30 czerwca 2025.

## Proces ETL

1. **Extract** — wczytanie plików CSV do tabel `raw_eloRatings` i `raw_Matches`.
2. **Clean** — konwersja typów i uzupełnienie brakujących lub błędnych wartości.
3. **Load** — załadowanie 5 tabel wymiarów i tabeli faktów `fact_matches` w schemacie gwiazdy.
4. **Export** — zapis danych surowych do `backend/csv/raw/` i wymiarów do `backend/csv/clean/`.

| Tabela | Zawartość |
|---|---|
| `dim_country` | Kraje |
| `dim_division` | Ligi |
| `dim_team` | Drużyny i ich aktualny ranking Elo |
| `dim_season` | Sezony |
| `dim_date` | Kalendarz |
| `fact_matches` | Wyniki, statystyki, ranking Elo i kursy bukmacherskie |

## Analiza statystyczna

Analiza korzysta z widoku `v_matches_enriched`, który łączy tabelę faktów z wymiarami.

- **Statystyki opisowe** — minimum, maksimum, średnia, odchylenie standardowe, mediana i kwantyle.
- **Zależności** — korelacja Pearsona wyniku do przerwy z wynikiem końcowym, regresja liniowa strzałów celnych i goli oraz macierz korelacji zapisywana do `correlation_matrix.xlsx`.
- **Kursy bukmacherskie** — rozkład kursów, prawdopodobieństwo implikowane i marża.
- **9 wykresów** — liczba drużyn w ligach, kartki, ranking Elo w czasie i według lig, rozkład goli, faule oraz zależność goli od strzałów celnych.

## Uruchomienie

Wymagane są Python 3.13+ oraz Docker.

1. Umieść pliki `raw_Matches.csv` i `raw_eloRatings.csv` w katalogu `backend/csv/raw/`.
2. Utwórz plik `.env` w głównym katalogu projektu:

   ```env
   YOUR_HOST=127.0.0.1
   YOUR_PORT=3307
   YOUR_USER=root
   YOUR_PASSWORD=twoje_haslo
   YOUR_DB_NAME=football_dw
   ```

3. Uruchom bazę danych i proces ETL:

   ```bash
   docker compose up -d
   cd backend
   pip install -r requirements.txt
   python database/main_dw_db.py
   python database/etl/etl_raw_to_dw.py
   ```

Kroki instalacji i ETL można też wykonać skryptem `scripts/sh/run_etl.sh` lub `scripts/bat/run_etl.bat`, uruchomionym z katalogu `backend`.

Analizę statystyczną uruchomisz po zakończeniu ETL, również z katalogu `backend`:

```bash
python -m statistical_analysis.run_stats
python -m statistical_analysis.stats.run_odds_stats
python -m statistical_analysis.visualisation_data
```

Statystyki opisowe i wykresy można też uruchomić skryptem `scripts/sh/run_stats.sh` lub `scripts/bat/run_stats.bat`.

## Struktura projektu

```
football-analytics/
├── backend/
│   ├── common/          # Stałe konfiguracyjne
│   ├── csv/             # Pliki wejściowe i eksporty CSV
│   ├── database/
│   │   ├── etl/         # Proces ETL
│   │   ├── tables/      # Definicje tabel
│   │   └── views/       # Widoki SQL
│   ├── scripts/         # Skrypty uruchomieniowe
│   ├── statistical_analysis/  # Statystyki i wykresy
│   └── requirements.txt
├── docker-compose.yaml
└── README.md
```
