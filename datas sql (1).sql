CREATE DATABASE football_data;
USE football_data;

DROP TABLE IF EXISTS appearances;
DROP TABLE IF EXISTS club_games;
DROP TABLE IF EXISTS clubs;
DROP TABLE IF EXISTS competitions;
DROP TABLE IF EXISTS game_events;
DROP TABLE IF EXISTS game_lineups;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS player_valuations;
DROP TABLE IF EXISTS players;

CREATE TABLE appearances (
    appearance_id VARCHAR(255) NOT NULL,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    player_club_id INT,
    player_current_club_id INT,
    date DATE,
    player_name VARCHAR(255),
    competition_id VARCHAR(255),
    yellow_cards INT,
    red_cards INT,
    goals INT,
    assists INT,
    minutes_played INT,
    PRIMARY KEY (appearance_id)
);

CREATE TABLE club_games (
    game_id INT NOT NULL,
    club_id INT NOT NULL,
    own_goals INT,
    own_position INT,
    own_manager_name VARCHAR(255),
    opponent_id INT,
    opponent_goals INT,
    opponent_position INT,
    opponent_manager_name VARCHAR(255),
    hosting VARCHAR(255),
    is_win INT
);

CREATE TABLE clubs (
    club_id INT NOT NULL,
    club_code VARCHAR(255),
    name VARCHAR(255),
    domestic_competition_id VARCHAR(255),
    total_market_value DECIMAL(20,2),
    squad_size INT,
    average_age DECIMAL(3,1),
    foreigners_number INT,
    foreigners_percentage DECIMAL(5,2),
    national_team_players INT,
    stadium_name VARCHAR(255),
    stadium_seats INT,
    net_transfer_record VARCHAR(255),
    coach_name VARCHAR(255),
    last_season INT,
    filename VARCHAR(255),
    url VARCHAR(255),
    PRIMARY KEY (club_id)
);

CREATE TABLE competitions (
    competition_id VARCHAR(255) NOT NULL,
    competition_code VARCHAR(255),
    name VARCHAR(255),
    sub_type VARCHAR(255),
    type VARCHAR(255),
    country_id INT,
    country_name VARCHAR(255),
    domestic_league_code VARCHAR(255),
    confederation VARCHAR(255),
    url VARCHAR(255),
    is_major_national_league BOOLEAN,
    PRIMARY KEY (competition_id)
);

CREATE TABLE game_events (
    game_event_id VARCHAR(255) NOT NULL,
    date DATE,
    game_id INT NOT NULL,
    minute INT,
    type VARCHAR(255),
    club_id INT,
    player_id INT,
    description VARCHAR(255),
    player_in_id INT,
    player_assist_id INT,
    PRIMARY KEY (game_event_id)
);

CREATE TABLE game_lineups (
    game_lineups_id VARCHAR(255) NOT NULL,
    date DATE,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    club_id INT NOT NULL,
    player_name VARCHAR(255),
    type VARCHAR(255),
    position VARCHAR(255),
    number VARCHAR(255),
    team_captain INT,
    PRIMARY KEY (game_lineups_id)
);

CREATE TABLE games (
    game_id INT NOT NULL,
    competition_id VARCHAR(255) NOT NULL,
    season INT,
    round VARCHAR(255),
    date DATE,
    home_club_id INT,
    away_club_id INT,
    home_club_goals INT,
    away_club_goals INT,
    home_club_position INT,
    away_club_position INT,
    home_club_manager_name VARCHAR(255),
    away_club_manager_name VARCHAR(255),
    stadium VARCHAR(255),
    attendance INT,
    referee VARCHAR(255),
    url VARCHAR(255),
    home_club_formation VARCHAR(255),
    away_club_formation VARCHAR(255),
    home_club_name VARCHAR(255),
    away_club_name VARCHAR(255),
    aggregate VARCHAR(255),
    competition_type VARCHAR(255),
    PRIMARY KEY (game_id)
);

CREATE TABLE player_valuations (
    player_id INT NOT NULL,
    date DATE,
    market_value_in_eur DECIMAL(20,2),
    current_club_id INT,
    player_club_domestic_competition_id VARCHAR(255)
);

CREATE TABLE players (
    player_id INT NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    name VARCHAR(255),
    last_season INT,
    current_club_id INT,
    player_code VARCHAR(255),
    country_of_birth VARCHAR(255),
    city_of_birth VARCHAR(255),
    country_of_citizenship VARCHAR(255),
    date_of_birth DATE,
    sub_position VARCHAR(255),
    position VARCHAR(255),
    foot VARCHAR(255),
    height_in_cm INT,
    contract_expiration_date DATETIME,
    agent_name VARCHAR(255),
    image_url VARCHAR(255),
    url VARCHAR(255),
    current_club_domestic_competition_id VARCHAR(255),
    current_club_name VARCHAR(255),
    market_value_in_eur DECIMAL(20,2),
    highest_market_value_in_eur DECIMAL(20,2),
    PRIMARY KEY (player_id)
);
SELECT * FROM appearances LIMIT 10;
SELECT * FROM club_games LIMIT 10;
SELECT * FROM clubs LIMIT 10;
SELECT * FROM competitions LIMIT 10;
SELECT * FROM game_events LIMIT 10;
SELECT * FROM game_lineups LIMIT 10;
SELECT * FROM games LIMIT 10;
SELECT * FROM player_valuations LIMIT 10;
SELECT * FROM players LIMIT 10;

-- código para comprobar estado de cada tabla

describe appearances;
describe club_games;
describe clubs;
describe competitions;
describe game_events;
describe game_lineups;
describe games;
describe player_valuations;
describe players;

-- crear las relaciones entre las tablas

-- 1 Relacionar la tabla appearances con games
ALTER TABLE appearances
ADD CONSTRAINT fk_appearances_games
FOREIGN KEY (game_id) REFERENCES games(game_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- 2 Relacionar la tabla club_games con games
ALTER TABLE club_games
ADD CONSTRAINT fk_club_games_games
FOREIGN KEY (game_id) REFERENCES games(game_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- 3 Relacionar la tabla game_events con games
ALTER TABLE game_events
ADD CONSTRAINT fk_game_events_games
FOREIGN KEY (game_id) REFERENCES games(game_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- 4 Relacionar la tabla game_lineups con games
ALTER TABLE game_lineups
DROP FOREIGN KEY fk_game_lineups_games;

ALTER TABLE game_lineups
ADD CONSTRAINT fk_game_lineups_games
FOREIGN KEY (game_id) 
REFERENCES games(game_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- 5 Relacionar la tabla games con competitions
ALTER TABLE games
ADD CONSTRAINT fk_games_competitions
FOREIGN KEY (competition_id) REFERENCES competitions(competition_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

-- 6 Relacionar la tabla player_valuations con players
ALTER TABLE player_valuations
ADD CONSTRAINT fk_player_valuations_players
FOREIGN KEY (player_id) REFERENCES players(player_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

select * from player_valuations;
ALTER TABLE players 
            CHANGE COLUMN current_club_id club_id INT;
ALTER TABLE players RENAME COLUMN name TO player_name;

ALTER TABLE player_valuations RENAME COLUMN player_club_domestic_competition_id to domestic_league_code
