-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c vagrant;
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Players Table
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name varchar(255)
);

CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	winner int REFERENCES Players(id),
	loser int REFERENCES Players(id)
);

CREATE VIEW wins AS
	SELECT players.id, COUNT(matches.id) AS n
	FROM players
	LEFT JOIN (SELECT * FROM matches) as matches
	ON players.id = matches.winner
	GROUP BY players.id;
	
CREATE VIEW count AS
	SELECT players.id, Count(matches.id) AS n 
	FROM players
	LEFT JOIN matches
	ON players.id = matches.winner OR players.id = matches.loser
	GROUP BY players.id;

CREATE VIEW standings AS 
	SELECT players.id,players.name,wins.n as wins,count.n as matches 
	FROM players, count, wins
	WHERE players.id = wins.id and wins.id = count.id;