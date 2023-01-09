CREATE TABLE Games (
	ID int,
	Season varchar(255),
	Week TINYINT,
	Neutral_site bool,
	Attendance MEDIUMINT,
	Venue_id int,
	home_id int,
	home_points TINYINT,
	Home_post_win_prob FLOAT,
	Away_id int,
	Away_points TINYINT,
	Away_post_win_prob FLOAT,
	Excitement_index FLOAT,
	PRIMARY KEY (ID),
	FOREIGN KEY (Home_id) REFERENCES Teams(ID),
	FOREIGN KEY (Away_id) REFERENCES Teams(ID),
	FOREIGN KEY (Venue_id) REFERENCES Venues(ID)
);