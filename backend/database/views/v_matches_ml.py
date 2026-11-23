"""
v_matches_ml.py — Subset of columns for ML model (29 columns).
 
Used by: ml_exploratory_analysis/prepare_data.py.
Contains features for HomeNoLose classification: Elo, form, odds, handicaps, probabilities.
"""

SQL = """
CREATE OR REPLACE VIEW v_matches_ml AS
SELECT
    dv.division_code      AS Division,
    ht.name               AS HomeTeam,
    at.name               AS AwayTeam,
    m.home_elo            AS HomeElo,
    m.away_elo            AS AwayElo,
    m.form3_home          AS Form3Home,
    m.form5_home          AS Form5Home,
    m.form3_away          AS Form3Away,
    m.form5_away          AS Form5Away,
    m.ft_result           AS FTResult,
    m.odd_home            AS OddHome,
    m.odd_draw            AS OddDraw,
    m.odd_away            AS OddAway,
    m.max_home            AS MaxHome,
    m.max_draw            AS MaxDraw,
    m.max_away            AS MaxAway,
    m.odd_over_25         AS Over25,
    m.odd_under_25        AS Under25,
    m.max_over_25         AS MaxOver25,
    m.max_under_25        AS MaxUnder25,
    m.handi_size          AS HandiSize,
    m.handi_home          AS HandiHome,
    m.handi_away          AS HandiAway,
    m.c_lth               AS C_LTH,
    m.c_lta               AS C_LTA,
    m.c_vhd               AS C_VHD,
    m.c_vad               AS C_VAD,
    m.c_htb               AS C_HTB,
    m.c_phb               AS C_PHB,
    d.full_date           AS MatchDate
FROM fact_matches m
JOIN dim_date d ON m.date_key = d.date_key
JOIN dim_division dv ON m.division_key = dv.division_key
JOIN dim_team ht ON m.home_team_key = ht.team_key
JOIN dim_team at ON m.away_team_key = at.team_key
"""
