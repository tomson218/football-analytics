"""
dim_date.py — Date dimension (full date dimension).
 
Contains attributes: year, quarter, month, day, day of week, season, weekend/weekday.
Key is YYYYMMDD (e.g. 20200815).
"""

SQL = """
CREATE TABLE IF NOT EXISTS dim_date (
    date_key           INT          NOT NULL PRIMARY KEY,  -- YYYYMMDD
    full_date          DATE         NOT NULL,
    year               INT          NOT NULL,
    quarter            INT          NOT NULL,
    month              INT          NOT NULL,
    day                INT          NOT NULL,
    day_of_week        INT          NOT NULL,              -- 0=Mon, 6=Sun
    day_name           VARCHAR(20)  NOT NULL,
    month_name         VARCHAR(20)  NOT NULL,
    season_name        VARCHAR(10),                        -- np. '2020/21'
    is_weekend         TINYINT(1)   NOT NULL,              -- 1 = sob/niedz
    is_weekday         TINYINT(1)   NOT NULL               -- 1 = pon-pt
) ENGINE=InnoDB;
"""
