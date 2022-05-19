<?php
   define('DB_SERVER', 'localhost:3306');
   define('DB_USERNAME', getenv('MYSQL_USER_NAME'));
   define('DB_PASSWORD', getenv('MYSQL_USER_PASS'));
   define('DB_DATABASE', getenv('MYSQL_USER_DB'));
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE);
	
	$TBL = "tbl_users_2";
?>
