CREATE TABLE tbl_users (
	username varchar(255),
	firstname varchar(63),
	lastname varchar(63),
	password CHAR(32)
);

INSERT INTO tbl_users (username, firstname, lastname, PASSWORD)
SELECT
	"as1605",
	"Aditya",
	"Singh",
	"386b8fe06ad1d01e027de7270f48822d"
WHERE
	NOT EXISTS (
		SELECT
			*
		FROM
			tbl_users);

