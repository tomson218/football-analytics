-- =============================================================================
-- sample_dw_queries.sql — Przykładowe zapytania analityczne na hurtowni danych
-- =============================================================================
-- Plik pokazuje korzyści z modelu gwiazdy (Star Schema) w porównaniu do OLTP.
-- Uruchom na bazie: football_dw
-- =============================================================================

-- =============================================================================
-- 1. Liczba meczów i średnia goli na sezon
-- =============================================================================
-- HURTOWNIA (proste, 1 tabela faktów + 1 wymiar):
SELECT
    s.season_name,
    COUNT(*)                          AS matches_count,
    AVG(f.ft_home_goals + f.ft_away_goals) AS avg_goals_per_match
FROM fact_matches f
JOIN dim_season s ON f.season_key = s.season_key
GROUP BY s.season_name
ORDER BY s.season_name;

-- =============================================================================
-- 2. Statystyki drużyny w danym sezonie (mecze, wygrane, remisy, przegrane, gole)
-- =============================================================================
-- HURTOWNIA (denormalizowany wymiar drużyny — bez JOIN z krajem):
SELECT
    t.name                            AS team,
    s.season_name,
    COUNT(*)                          AS matches,
    SUM(CASE WHEN f.ft_result = 'H' AND f.home_team_key = t.team_key
             OR f.ft_result = 'A' AND f.away_team_key = t.team_key THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN f.ft_result = 'D' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN f.ft_result = 'A' AND f.home_team_key = t.team_key
             OR f.ft_result = 'H' AND f.away_team_key = t.team_key THEN 1 ELSE 0 END) AS losses,
    SUM(CASE WHEN f.home_team_key = t.team_key THEN f.ft_home_goals
             WHEN f.away_team_key = t.team_key THEN f.ft_away_goals END) AS goals_scored,
    SUM(CASE WHEN f.home_team_key = t.team_key THEN f.ft_away_goals
             WHEN f.away_team_key = t.team_key THEN f.ft_home_goals END) AS goals_conceded
FROM fact_matches f
JOIN dim_team t ON f.home_team_key = t.team_key OR f.away_team_key = t.team_key
JOIN dim_season s ON f.season_key = s.season_key
WHERE t.name = 'Manchester City'
  AND s.season_name = '2023/24'
GROUP BY t.name, s.season_name;

-- =============================================================================
-- 3. Średnie kursy bukmacherskie na ligę (1X2)
-- =============================================================================
-- HURTOWNIA (wymiar ligi z denormalizowanym krajem):
SELECT
    d.name                            AS division,
    d.country_name,
    COUNT(*)                          AS matches,
    AVG(f.odd_home)                   AS avg_odd_home,
    AVG(f.odd_draw)                   AS avg_odd_draw,
    AVG(f.odd_away)                   AS avg_odd_away
FROM fact_matches f
JOIN dim_division d ON f.division_key = d.division_key
GROUP BY d.name, d.country_name
ORDER BY matches DESC;

-- =============================================================================
-- 4. Analiza wyników w zależności od dnia tygodnia
-- =============================================================================
-- HURTOWNIA (wymiar daty z gotowymi atrybutami):
SELECT
    dd.day_name,
    COUNT(*)                          AS matches,
    AVG(f.ft_home_goals + f.ft_away_goals) AS avg_goals,
    AVG(f.home_shots + f.away_shots)  AS avg_shots,
    SUM(CASE WHEN f.ft_result = 'H' THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN f.ft_result = 'D' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN f.ft_result = 'A' THEN 1 ELSE 0 END) AS away_wins
FROM fact_matches f
JOIN dim_date dd ON f.date_key = dd.date_key
GROUP BY dd.day_name, dd.day_of_week
ORDER BY dd.day_of_week;

-- =============================================================================
-- 5. Porównanie Elo vs wynik meczu (czy faworyci wygrywają?)
-- =============================================================================
-- HURTOWNIA (Elo jako miara w tabeli faktów):
SELECT
    CASE
        WHEN f.home_elo > f.away_elo + 20 THEN 'Duży faworyt (dom)'
        WHEN f.home_elo > f.away_elo THEN 'Lekki faworyt (dom)'
        WHEN f.away_elo > f.home_elo + 20 THEN 'Duży faworyt (gość)'
        WHEN f.away_elo > f.home_elo THEN 'Lekki faworyt (gość)'
        ELSE 'Równe szanse'
    END AS elo_category,
    COUNT(*)                          AS matches,
    SUM(CASE WHEN f.ft_result = 'H' THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN f.ft_result = 'D' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN f.ft_result = 'A' THEN 1 ELSE 0 END) AS away_wins,
    ROUND(
        SUM(CASE
            WHEN f.home_elo > f.away_elo AND f.ft_result = 'H' THEN 1
            WHEN f.away_elo > f.home_elo AND f.ft_result = 'A' THEN 1
            ELSE 0 END
        ) * 100.0 / COUNT(*), 2
    ) AS favorite_win_rate
FROM fact_matches f
GROUP BY elo_category
ORDER BY matches DESC;

-- =============================================================================
-- 6. Weekend vs weekday — czy są inne kursy?
-- =============================================================================
-- HURTOWNIA (gotowe flagi is_weekend / is_weekday w dim_date):
SELECT
    CASE WHEN dd.is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS period,
    COUNT(*)                          AS matches,
    AVG(f.odd_home)                   AS avg_odd_home,
    AVG(f.odd_draw)                   AS avg_odd_draw,
    AVG(f.odd_away)                   AS avg_odd_away,
    AVG(f.ft_home_goals + f.ft_away_goals) AS avg_goals
FROM fact_matches f
JOIN dim_date dd ON f.date_key = dd.date_key
GROUP BY dd.is_weekend
ORDER BY period;

-- =============================================================================
-- 7. Top 10 drużyn pod względem strzelonych goli (wszystkie sezony)
-- =============================================================================
-- HURTOWNIA (denormalizowany wymiar — nazwa kraju w dim_team):
SELECT
    t.name                            AS team,
    t.country_name,
    t.current_elo,
    SUM(CASE WHEN f.home_team_key = t.team_key THEN f.ft_home_goals
             WHEN f.away_team_key = t.team_key THEN f.ft_away_goals END) AS total_goals_scored,
    COUNT(*)                          AS total_matches
FROM fact_matches f
JOIN dim_team t ON f.home_team_key = t.team_key OR f.away_team_key = t.team_key
GROUP BY t.name, t.country_name, t.current_elo
ORDER BY total_goals_scored DESC
LIMIT 10;

-- =============================================================================
-- 8. Agregacja kwartalna — gole i strzały na kwartał
-- =============================================================================
-- HURTOWNIA (gotowe pole quarter w dim_date):
SELECT
    dd.year,
    dd.quarter,
    COUNT(*)                          AS matches,
    SUM(f.ft_home_goals + f.ft_away_goals) AS total_goals,
    AVG(f.ft_home_goals + f.ft_away_goals) AS avg_goals_per_match,
    SUM(f.home_shots + f.away_shots)  AS total_shots
FROM fact_matches f
JOIN dim_date dd ON f.date_key = dd.date_key
GROUP BY dd.year, dd.quarter
ORDER BY dd.year, dd.quarter;

-- =============================================================================
-- 9. Analiza Over/Under 2.5 — skuteczność kursów
-- =============================================================================
-- HURTOWNIA (kursy i wyniki w jednej tabeli faktów):
SELECT
    d.division_code,
    COUNT(*)                          AS matches,
    SUM(CASE WHEN f.ft_home_goals + f.ft_away_goals > 2 THEN 1 ELSE 0 END) AS over_25_count,
    ROUND(SUM(CASE WHEN f.ft_home_goals + f.ft_away_goals > 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS over_25_pct,
    AVG(f.odd_over_25)                AS avg_odd_over_25,
    AVG(f.odd_under_25)               AS avg_odd_under_25
FROM fact_matches f
JOIN dim_division d ON f.division_key = d.division_key
GROUP BY d.division_code
ORDER BY over_25_pct DESC;

-- =============================================================================
-- 10. Sezon + liga — pełna tabela statystyk
-- =============================================================================
-- HURTOWNIA (klasyczne zapytanie OLAP — slice & dice):
SELECT
    s.season_name,
    d.division_code,
    d.country_name,
    COUNT(*)                          AS matches,
    SUM(f.ft_home_goals)              AS home_goals,
    SUM(f.ft_away_goals)              AS away_goals,
    AVG(f.ft_home_goals + f.ft_away_goals) AS avg_goals,
    AVG(f.home_shots)                 AS avg_home_shots,
    AVG(f.away_shots)                 AS avg_away_shots,
    AVG(f.home_elo)                   AS avg_home_elo,
    AVG(f.away_elo)                   AS avg_away_elo
FROM fact_matches f
JOIN dim_season s ON f.season_key = s.season_key
JOIN dim_division d ON f.division_key = d.division_key
GROUP BY s.season_name, d.division_code, d.country_name
ORDER BY s.season_name, d.division_code;
