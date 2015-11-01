-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
--using database tournament psql
\c tournament;
--players table has player id, player name, and "bye"
--a column for storing a boolean free win flug 
CREATE TABLE players(
	player_id SERIAL PRIMARY KEY, 
	name TEXT NOT NULL, 
	bye BOOLEAN
);
--matches table has match id, winner id, the id of a player who wins and loser id -
-- the id of a player who fails match
CREATE TABLE matches(
	match_id SERIAL PRIMARY KEY, 
	winner_id INTEGER REFERENCES players(player_id) ON DELETE CASCADE,
 	loser_id INTEGER REFERENCES players(player_id) ON DELETE CASCADE
 );

--view with fields: player's id, name and wins
CREATE VIEW winns AS SELECT p.player_id, p.name, count(m1.winner_id) AS wins 
        FROM players p LEFT OUTER JOIN matches m1 ON p.player_id=m1.winner_id 
        GROUP BY player_id;

