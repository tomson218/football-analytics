"""
dim_country.py — Country dimension (code, name).
 
Base dimension in the hierarchy: country → league → team.
"""

SQL = """
CREATE TABLE IF NOT EXISTS dim_country (
    country_key       INT AUTO_INCREMENT PRIMARY KEY,
    country_code      VARCHAR(3)  NOT NULL UNIQUE,
    name              VARCHAR(100) NOT NULL
) ENGINE=InnoDB;
"""
