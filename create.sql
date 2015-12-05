DROP DATABASE project;
CREATE DATABASE project;
USE project;

CREATE TABLE Employees(
	id INTEGER,
	age INTEGER,
	salary LONGBLOB NOT NULL, # Bob Loblaw's LONGBLOB
	PRIMARY KEY(id)
);
