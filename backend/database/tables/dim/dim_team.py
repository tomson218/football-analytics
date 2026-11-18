"""
dim_team.py — Team dimension (name, country, league, Elo).
 
Denormalized with country and Elo data. Supports SLOWL (Slowly Changing Dimensions)
for team history changes (e.g. league change).
"""

SQL = """
CREATE TABLE IF NOT EXISTS dim_team (
    team_key          INT AUTO_INCREMENT PRIMARY KEY,
    name              VARCHAR(100) NOT NULL,
    country_key       INT NOT NULL,
    country_code      VARCHAR(3),
    country_name      VARCHAR(100),
    current_elo       DECIMAL(6, 2),
    record_type       VARCHAR(10) DEFAULT 'current',  -- SLOWL: current / historical
    valid_from        DATE,
    valid_to          DATE,
    FOREIGN KEY (country_key) REFERENCES dim_country(country_key)
) ENGINE=InnoDB;
"""
