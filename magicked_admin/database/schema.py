schema = """
    CREATE TABLE meta (
        version INTEGER DEFAULT 1
    );
    
    CREATE TABLE player (
        player_id INTEGER PRIMARY KEY
        server_id INTEGER, -- TODO: NOT NULL
        steam_id INTEGER UNIQUE NOT NULL,
        op INTEGER DEFAULT 0,
        insert_date INTEGER NOT NULL,
        
        -- Last seen username, could change
        username VARCHAR(256) NOT NULL
    );
    
    CREATE TABLE map (
        map_id INTEGER PRIMARY KEY,
        title VARCHAR(256) NOT NULL,
        name VARCHAR(256) NOT NULL,
    );
    
    CREATE TABLE match (
        match_id INTEGER PRIMARY KEY,
        server_id INTEGER, -- TODO: NOT NULL
        map_id INTEGER NOT NULL,
        game_mode VARCHAR(255) NOT NULL,
        -- 0.0, 1.0, 2.0, 3.0
        difficulty FLOAT NOT NULL,
        -- 4, 7, 10 for survival
        -- Might not be available
        length INTEGER DEFAULT NULL,
        
        start_date INTEGER NOT NULL,
        end_date INTEGER NOT NULL,
        
        -- Might not be available
        last_wave INTEGER DEFAULT NULL,
    );
    
    CREATE TABLE session (
        session_id INTEGER PRIMARY KEY,
        steam_id INTEGER NOT NULL, -- TODO: player_id
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
