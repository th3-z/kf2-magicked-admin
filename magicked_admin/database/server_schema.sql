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
    title VARCHAR(64) PRIMARY KEY,
    name VARCHAR(64) DEFAULT "kf-default",
    plays INTEGER DEFAULT 0,
    votes INTEGER DEFAULT 0,
    resets INTEGER DEFAULT 0
);
