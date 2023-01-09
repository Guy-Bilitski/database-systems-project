CREATE TABLE Teams (
	ID int NOT NULL,
	School varchar(255),
	Venue_id int,
	PRIMARY KEY(ID),
	FOREIGN KEY (Venue_id) REFERENCES Venues(ID)
);