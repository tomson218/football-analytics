"""
raw_matches.py — Raw table: Matches (source match data).
 
Preserves raw match data in the warehouse as a source before transformation.
"""

SQL = """
CREATE TABLE IF NOT EXISTS raw_Matches (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    Division    VARCHAR(10),
    MatchDate   DATE,
    MatchTime   VARCHAR(20),
    HomeTeam    VARCHAR(255),
    AwayTeam    VARCHAR(255),
    HomeElo     DECIMAL(10, 2),
    AwayElo     DECIMAL(10, 2),
    Form3Home   DECIMAL(5, 1),
    Form5Home   DECIMAL(5, 1),
    Form3Away   DECIMAL(5, 1),
    Form5Away   DECIMAL(5, 1),
    FTHome      DECIMAL(5, 1),
    FTAway      DECIMAL(5, 1),
    FTResult    VARCHAR(5),
    HTHome      DECIMAL(5, 1),
    HTAway      DECIMAL(5, 1),
    HTResult    VARCHAR(5),
    HomeShots   INT,
    AwayShots   INT,
    HomeTarget  INT,
    AwayTarget  INT,
    HomeFouls   INT,
    AwayFouls   INT,
    HomeCorners INT,
    AwayCorners INT,
    HomeYellow  INT,
    AwayYellow  INT,
    HomeRed     INT,
    AwayRed     INT,
    OddHome     DECIMAL(6, 2),
    OddDraw     DECIMAL(6, 2),
    OddAway     DECIMAL(6, 2),
    MaxHome     DECIMAL(6, 2),
    MaxDraw     DECIMAL(6, 2),
    MaxAway     DECIMAL(6, 2),
    Over25      DECIMAL(6, 2),
    Under25     DECIMAL(6, 2),
    MaxOver25   DECIMAL(6, 2),
    MaxUnder25  DECIMAL(6, 2),
    HandiSize   DECIMAL(6, 2),
    HandiHome   DECIMAL(6, 2),
    HandiAway   DECIMAL(6, 2),
    C_LTH       DECIMAL(6, 2),
    C_LTA       DECIMAL(6, 2),
    C_VHD       DECIMAL(6, 2),
    C_VAD       DECIMAL(6, 2),
    C_HTB       DECIMAL(6, 2),
    C_PHB       DECIMAL(6, 2)
) ENGINE=InnoDB;
"""
