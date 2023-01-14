CREATE TABLE Roster (
	ID int,
	Team varchar(255),
	Year SMALLINT,
	PRIMARY KEY (ID, Team, Year),
	FOREIGN KEY (ID) REFERENCES Athletes(ID)
);