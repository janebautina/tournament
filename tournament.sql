-- Table definitions for the tournament project.


CREATE DATABASE tournament;
--using database tournament psql
\c tournament;
--players table has player id, player name, and "bye"
--a column for storing a boolean free win flug 
CREATE TABLE players(player_id serial primary key, name text not null, bye boolean);
--matches table has match id, winner id, the id of a player who wins and loser id -
-- the id of a player who fails match
CREATE TABLE matches(match_id serial primary key, winner_id integer references players(player_id) not null, loser_id integer references players(player_id));


