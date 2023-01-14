CREATE TABLE Records (
	Year SMALLINT,
	Team varchar(255),
	Expected_wins FLOAT,
	Total_games TINYINT,
	Wins TINYINT,
	Losses TINYINT,
	Ties TINYINT,
	PRIMARY KEY (Year, Team)
);