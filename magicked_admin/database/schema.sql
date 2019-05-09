CREATE TABLE players(
    steam_id VARCHAR(64) PRIMARY KEY,
    username VARCHAR(64),
    kills INTEGER DEFAULT 0,
    op INTEGER DEFAULT 0,
    dosh INTEGER DEFAULT 0,
    dosh_spent INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    sessions INTEGER DEFAULT 0,
    health_lost INTEGER DEFAULT 0,
    time_online INTEGER DEFAULT 0
);

CREATE TABLE maps(
    title VARCHAR(64) PRIMARY KEY,
    name VARCHAR(64) DEFAULT "Unknown",
    plays_survival INTEGER DEFAULT 0,
    plays_weekly INTEGER DEFAULT 0,
    plays_endless INTEGER DEFAULT 0,
    plays_survival_vs INTEGER DEFAULT 0,
    plays_other INTEGER DEFAULT 0,
    highest_wave INTEGER DEFAULT 0
);

CREATE TABLE map_records(
    map_title VARCHAR(64),
    game_time DOUBLE DEFAULT 0.0,
    game_length INTEGER DEFAULT -1,
    game_difficulty VARCHAR(64),
    game_wave INTEGER DEFAULT 0,
    game_victory INTEGER DEFAULT 0,
    player_count INTEGER DEFAULT 0
);
