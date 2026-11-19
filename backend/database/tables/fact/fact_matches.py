"""
fact_matches.py — Central fact table of the data warehouse (match).
 
Contains all match metrics: Elo, form, goals, statistics, odds, handicaps,
model probabilities. Points to 5 dimensions via foreign keys.
"""

SQL = """
CREATE TABLE IF NOT EXISTS fact_matches (
    match_key          INT AUTO_INCREMENT PRIMARY KEY,
    date_key           INT NOT NULL,
    home_team_key      INT NOT NULL,
    away_team_key      INT NOT NULL,
    division_key       INT NOT NULL,
    season_key         INT NOT NULL,

    -- Measures: Elo
    home_elo           DECIMAL(6, 2),
    away_elo           DECIMAL(6, 2),

    -- Measures: Form
    form3_home         INT,
    form5_home         INT,
    form3_away         INT,
    form5_away         INT,

    -- Measures: Results (goals)
    ft_home_goals      INT,
    ft_away_goals      INT,
    ft_result          CHAR(1),                          -- H / D / A
    ht_home_goals      INT,
    ht_away_goals      INT,
    ht_result          CHAR(1),                          -- H / D / A

    -- Measures: Match statistics
    home_shots         INT,
    away_shots         INT,
    home_target        INT,
    away_target        INT,
    home_fouls         INT,
    away_fouls         INT,
    home_corners       INT,
    away_corners       INT,
    home_yellow        INT,
    away_yellow        INT,
    home_red           INT,
    away_red           INT,

    -- Measures: Odds (1X2)
    odd_home           DECIMAL(5, 2),
    odd_draw           DECIMAL(5, 2),
    odd_away           DECIMAL(5, 2),
    max_home           DECIMAL(5, 2),
    max_draw           DECIMAL(5, 2),
    max_away           DECIMAL(5, 2),

    -- Measures: Over/Under 2.5 odds
    odd_over_25        DECIMAL(5, 2),
    odd_under_25       DECIMAL(5, 2),
    max_over_25        DECIMAL(5, 2),
    max_under_25       DECIMAL(5, 2),

    -- Measures: Handicap
    handi_size         DECIMAL(3, 1),
    handi_home         DECIMAL(5, 2),
    handi_away         DECIMAL(5, 2),

    -- Measures: Model probabilities
    c_lth              DECIMAL(6, 4),
    c_lta              DECIMAL(6, 4),
    c_vhd              DECIMAL(6, 4),
    c_vad              DECIMAL(6, 4),
    c_htb              DECIMAL(6, 4),
    c_phb              DECIMAL(6, 4),

    -- Indexes for faster analytical queries
    INDEX idx_date (date_key),
    INDEX idx_season (season_key),
    INDEX idx_division (division_key),
    INDEX idx_home_team (home_team_key),
    INDEX idx_away_team (away_team_key),

    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (home_team_key) REFERENCES dim_team(team_key),
    FOREIGN KEY (away_team_key) REFERENCES dim_team(team_key),
    FOREIGN KEY (division_key) REFERENCES dim_division(division_key),
    FOREIGN KEY (season_key) REFERENCES dim_season(season_key)
) ENGINE=InnoDB;
"""
