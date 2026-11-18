"""
raw_elo_ratings.py — Raw table: Elo Ratings (source Elo data).
 
Preserves raw Elo data in the warehouse as a source before transformation.
"""

SQL = """
CREATE TABLE IF NOT EXISTS raw_eloRatings (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    date    DATE,
    club    VARCHAR(255),
    country VARCHAR(10),
    elo     DECIMAL(10, 2)
) ENGINE=InnoDB;
"""
