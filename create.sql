DROP DATABASE project;
CREATE DATABASE project;
USE project;


CREATE FUNCTION MyTest
RETURNS INTEGER SONAME 'hello.so';


CREATE TABLE Employees(
	id INTEGER,
	age INTEGER,
	salary LONGBLOB NOT NULL, # Bob Loblaw's LONGBLOB
	PRIMARY KEY(id)
);

INSERT INTO Employees VALUES(666, 20, 60000);

SELECT age FROM Employees;

SELECT MyTest(age) FROM Employees;