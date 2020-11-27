schema = """
    CREATE TABLE meta (
        version INTEGER DEFAULT 1
    );
    
    CREATE TABLE server (
        server_id INTEGER PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        insert_date INTEGER NOT NULL
    );
    
    CREATE TABLE player (
        player_id INTEGER PRIMARY KEY,
        server_id INTEGER NOT NULL,
        steam_id INTEGER NOT NULL,
        op INTEGER DEFAULT 0,
        insert_date INTEGER NOT NULL,
        
        -- Last seen username, could change
        username VARCHAR(255),
        
        UNIQUE(server_id, steam_id)
    );
    
    -- De-normalised due to query cost
    CREATE TABLE server_players_date (
        server_id INTEGER NOT NULL,
        players INTEGER NOT NULL,
        date INTEGER NOT NULL
    );
    
    -- 'map' conflicts with Python keyword
    CREATE TABLE level (
        level_id INTEGER PRIMARY KEY,
        server_id INTEGER NOT NULL,
        -- e.g. KF-BlackForest
        title VARCHAR(255) NOT NULL,
        -- e.g. Black Forest
        name VARCHAR(255) NOT NULL,
        
        UNIQUE(title, server_id)
    );
    
    CREATE TABLE match (
        match_id INTEGER PRIMARY KEY,
        server_id INTEGER, -- TODO: NOT NULL
        level_id INTEGER NOT NULL,
        game_type VARCHAR(255) NOT NULL,
        -- 0.0, 1.0, 2.0, 3.0
        difficulty FLOAT NOT NULL,
        -- 4, 7, 10 for survival
        -- Might not be available
        length INTEGER DEFAULT NULL,
        
        start_date INTEGER DEFAULT NULL,
        end_date INTEGER DEFAULT NULL,
        end_date_dirty INTEGER DEFAULT 0,
        
        -- Might not be available
        last_wave INTEGER DEFAULT NULL
    );
    
    CREATE TABLE session (
        session_id INTEGER PRIMARY KEY,
        player_id INTEGER NOT NULL,
        match_id INTEGER,
    
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
"""
