CREATE TABLE players(
    username VARCHAR(64) PRIMARY KEY,
    kills INTEGER DEFAULT 0,
    dosh INTEGER DEFAULT 0,
    dosh_spent INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    logins INTEGER DEFAULT 0,
    health_lost INTEGER DEFAULT 0,
    time_online INTEGER DEFAULT 0
);

CREATE TABLE maps(
    name VARCHAR(64) PRIMARY KEY,
    title VARCHAR(64) DEFAULT "Unnamed",
    plays_survival INTEGER DEFAULT 0,
    plays_weekly INTEGER DEFAULT 0,
    plays_endless INTEGER DEFAULT 0,
    plays_survival_vs INTEGER DEFAULT 0,
    plays_other INTEGER DEFAULT 0,
    highest_wave INTEGER DEFAULT 0
);
