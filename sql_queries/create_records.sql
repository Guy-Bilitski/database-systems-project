CREATE TABLE Records (
	Year SMALLINT,
	Team_id int,
	Expected_wins FLOAT,
	Total_games TINYINT,
	Wins TINYINT,
	Losses TINYINT,
	Ties TINYINT,
	PRIMARY KEY (Year, Team_id),
	FOREIGN KEY (Team_id) REFERENCES Teams(ID)
);