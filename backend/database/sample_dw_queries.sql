-- =============================================================================
-- sample_dw_queries.sql — Sample analytical queries on the data warehouse
-- =============================================================================
-- Shows the benefits of the star schema compared to an OLTP model.
-- Run on database: football_dw
-- =============================================================================

-- =============================================================================
-- 1. Number of matches and average goals per season
-- =============================================================================
-- WAREHOUSE (simple: 1 fact table + 1 dimension):
SELECT
    s.season_name,
    COUNT(*)                          AS matches_count,
    AVG(f.ft_home_goals + f.ft_away_goals) AS avg_goals_per_match
FROM fact_matches f
JOIN dim_season s ON f.season_key = s.season_key
GROUP BY s.season_name
ORDER BY s.season_name;

-- =============================================================================
-- 2. Team statistics in a given season (matches, wins, draws, losses, goals)
-- =============================================================================
-- WAREHOUSE (denormalized team dimension — no JOIN with country):
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
-- 3. Average bookmaker odds per league (1X2)
-- =============================================================================
-- WAREHOUSE (league dimension with denormalized country):
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
-- 4. Results by day of the week
-- =============================================================================
-- WAREHOUSE (date dimension with ready-made attributes):
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
-- 5. Elo vs match result (do favourites win?)
-- =============================================================================
-- WAREHOUSE (Elo as a measure in the fact table):
SELECT
    CASE
        WHEN f.home_elo > f.away_elo + 20 THEN 'Strong favourite (home)'
        WHEN f.home_elo > f.away_elo THEN 'Slight favourite (home)'
        WHEN f.away_elo > f.home_elo + 20 THEN 'Strong favourite (away)'
        WHEN f.away_elo > f.home_elo THEN 'Slight favourite (away)'
        ELSE 'Even'
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
-- 6. Weekend vs weekday — are the odds different?
-- =============================================================================
-- WAREHOUSE (ready-made is_weekend / is_weekday flags in dim_date):
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
-- 7. Top 10 teams by goals scored (all seasons)
-- =============================================================================
-- WAREHOUSE (denormalized dimension — country name in dim_team):
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
-- 8. Quarterly aggregation — goals and shots per quarter
-- =============================================================================
-- WAREHOUSE (ready-made quarter field in dim_date):
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
-- 9. Over/Under 2.5 — how accurate are the odds
-- =============================================================================
-- WAREHOUSE (odds and results in a single fact table):
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
-- 10. Season + league — full statistics table
-- =============================================================================
-- WAREHOUSE (classic OLAP query — slice & dice):
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
