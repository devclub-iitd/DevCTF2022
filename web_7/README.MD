```
---> Challeneg 7  : Challenge will host a PHP Webpage http://CTF_URL/admin.php and the source-file for admin.php willbe displayed on the page, main task is Source Code Analysis.
					(Loose Comparision Vulnerability).


					Sample PHP Code :

					<?php
  							require_once('flag.php');
  							$password_hash = "0e902564435691274142490923013038";  ----> Should be Changed, This is a Sample
  							$salt = "f789bbc328a3d1a3";  						  ----> Should be Changed, This is a Sample
  							if(isset($_GET['password']) && md5($salt . $_GET['password']) == $password_hash)
  							  echo $flag; # If true is returned the give the flag
  							}
  							echo highlight_file(__FILE__, true);
					?>

					Candidate will need to find a string, that when combined with the salt and then md5 hashed it returns 0e + 30 digits.

					For Example, In this case abr1R is the string which passed as input will result in validation and flag would be printed.


```

# Instructions

1. ``` $ docker-compose up ```
2. Open localhost:8080 if running without CTFd, localhost/web/7 otherwise.

