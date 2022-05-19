<?php

	include("config.php");
	
	$PASS = "aditya1234";

	$result = $db -> query("CREATE TABLE $TBL (user_id VARCHAR(32), hash CHAR(32), name VARCHAR(64));");
	assert($result !== false);

	$h = md5($PASS, false);

	$result = $db -> query("INSERT INTO $TBL VALUES ('admin', '$h', 'FLAG{i_am_a_flag}');");
	assert($result !== false);
	
	for ($i = 0; $i <= 500; $i++) {
		$seed = md5(microtime(false), false); //str, hex 32 characters
		$user_id = substr($seed, 0, 8);
		$pass = substr($seed, 20, 12);
		$name = "Participant";
		$h = md5($pass);
		$result = $db -> query("INSERT INTO $TBL VALUES ('$user_id', '$h', '$name');");

		if ($result !== false) {
			echo $user_id . ' ' . $pass . '<br>';
			fwrite(fopen("credentials.txt", "a"), $user_id . ',' . $pass . PHP_EOL);
		} else {
			echo $i;
		}
	}
?>
