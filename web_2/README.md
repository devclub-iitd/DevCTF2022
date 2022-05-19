```
--> Challenge 2  : Candidate will have to exploit IDOR in the Profile Section Password Reset and escalate to admin priveleges. Credentials for User1 will be provided.

					Example :

					http://ctfchallenge.awesome/dashboard/user/resetpassword?user=admin

This would result in changing the password for the ADMIN user, Candidate would Login after & get the second flag on the Admin page.
```

Put database credentials with permission to `SELECT` and `UPDATE` in `config.php` for production. `$TBL` is the table name.


`.setup.php` contains code to setup the database. Set a strong password (`$PASS`) for admin initially.

`credentials.txt` will then contain the credentials for the users which can be shared either through mail or CTFd.
In future, we can also read the names from a file and set them instead of using "Participant" for all.

Solution is to edit the hidden `<input>` tag's `value` from the given user id to `admin` to reset the password.

