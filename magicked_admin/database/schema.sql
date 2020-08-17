CREATE TABLE meta(
    version INTEGER DEFAULT 1
)

CREATE TABLE players(
    player_id INTEGER PRIMARY KEY,
    steam_id VARCHAR(64) UNIQUE,
    username VARCHAR(256),
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
    map_id INTEGER PRIMARY KEY,
    title VARCHAR(256) UNIQUE,
    name VARCHAR(256) DEFAULT "Unknown",
    plays_survival INTEGER DEFAULT 0,
    plays_weekly INTEGER DEFAULT 0,
    plays_endless INTEGER DEFAULT 0,
    plays_survival_vs INTEGER DEFAULT 0,
    plays_other INTEGER DEFAULT 0,
    highest_wave INTEGER DEFAULT 0
);

CREATE TABLE map_records(
    map_title VARCHAR(256) PRIMARY KEY,
    game_time DOUBLE DEFAULT 0.0,

    -- long, normal, short
    game_length INTEGER DEFAULT -1,
    game_difficulty VARCHAR(64),
    game_wave INTEGER DEFAULT 0,
    game_victory INTEGER DEFAULT 0,
    player_count INTEGER DEFAULT 0
);

CREATE TABLE match (
    map_id INTEGER PRIMARY KEY
);

CREATE TABLE session (
    session_id INTEGER PRIMARY KEY,

    -- Sessions
    player_id INTEGER NOT NULL,

    -- Play time
    start_date INTEGER NOT NULL,
    end_date INTEGER DEFAULT NULL,
    -- Session was left open due to force close or crash
    end_date_dirty INTEGER DEFAULT 0,

    kills INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    dosh INTEGER DEFAULT 0,
    dosh_spent INTEGER DEFAULT 0,
    damage_taken INTEGER DEFAULT 0
);