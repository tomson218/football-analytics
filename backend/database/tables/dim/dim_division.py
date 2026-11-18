"""
dim_division.py — League/division dimension (code, name, country).
 
Denormalized with country data for easier analytical queries.
"""

SQL = """
CREATE TABLE IF NOT EXISTS dim_division (
    division_key      INT AUTO_INCREMENT PRIMARY KEY,
    division_code     VARCHAR(10) NOT NULL UNIQUE,
    name              VARCHAR(100),
    country_key       INT NOT NULL,
    country_code      VARCHAR(3),
    country_name      VARCHAR(100),
    FOREIGN KEY (country_key) REFERENCES dim_country(country_key)
) ENGINE=InnoDB;
"""
