CREATE TABLE Venues (
	ID int NOT NULL,
	Name varchar(255),
	Capacity int,
	Grass bool,
	City varchar(255),
	State varchar(255),
	PRIMARY KEY(ID)
);

CREATE TABLE Teams (
	ID int NOT NULL,
	School varchar(255),
	Venue_id int,
	PRIMARY KEY(ID),
	FOREIGN KEY (Venue_id) REFERENCES Venues(ID)
);

CREATE INDEX team_name ON Teams(school);

CREATE TABLE Games (
	ID int,
	Season SMALLINT,
	Week TINYINT,
	Neutral_site bool,
	Venue_id int,
	Home_id int,
	Home_points TINYINT,
	Away_id int,
	Away_points TINYINT,
	PRIMARY KEY (ID),
	FOREIGN KEY (Home_id) REFERENCES Teams(ID),
	FOREIGN KEY (Away_id) REFERENCES Teams(ID),
	FOREIGN KEY (Venue_id) REFERENCES Venues(ID)
);

CREATE INDEX away_id ON Games(Away_id);
CREATE INDEX home_id ON Games(Home_id);

CREATE TABLE Players (
	ID int,
	Name varchar(255),
	PRIMARY KEY (ID)
);

CREATE FULLTEXT INDEX player_name_index ON Players(Name);

CREATE TABLE Roster (
	ID int,
	Team varchar(255),
	Year SMALLINT,
	PRIMARY KEY (ID, Team, Year),
	FOREIGN KEY (ID) REFERENCES Players(ID)
);

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

