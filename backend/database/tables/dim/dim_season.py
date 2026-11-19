"""
dim_season.py — Season dimension (e.g. 2020/21, 2021/22).
 
Allows filtering and aggregation of matches by competitive seasons.
"""

SQL = """
CREATE TABLE IF NOT EXISTS dim_season (
    season_key        INT AUTO_INCREMENT PRIMARY KEY,
    season_name       VARCHAR(10) NOT NULL UNIQUE,   -- e.g. '2020/21'
    start_year        INT NOT NULL,
    end_year          INT NOT NULL,
    start_date        DATE NOT NULL,
    end_date          DATE NOT NULL
) ENGINE=InnoDB;
"""
