CREATE DATABASE practice;

use practice;

CREATE TABLE employees (
    id INT,
    name VARCHAR(30),
    department VARCHAR(20),
    salary INT
);

INSERT INTO employees VALUES
(1,'Alice','HR',40000),
(2,'Bob','IT',60000),
(3,'Charlie','IT',55000),
(4,'David','Finance',50000),
(5,'Emma','HR',45000);