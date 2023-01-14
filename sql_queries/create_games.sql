CREATE TABLE Games (
	ID int,
	Season SMALLINT,
	Week TINYINT,
	Neutral_site bool,
	Venue_id int,
	home_id int,
	home_points TINYINT,
	Away_id int,
	Away_points TINYINT,
	PRIMARY KEY (ID),
	FOREIGN KEY (Home_id) REFERENCES Teams(ID),
	FOREIGN KEY (Away_id) REFERENCES Teams(ID),
	FOREIGN KEY (Venue_id) REFERENCES Venues(ID)
);