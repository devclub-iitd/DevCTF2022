<?php

	include("config.php");
	session_start();
	error_reporting(E_ALL);
	ini_set('display_errors', '1');	
	if($_SERVER["REQUEST_METHOD"] === "POST") {
		$username = $_POST['username'];
		$password = md5($_POST['password'], false); // hex 
		$query = "SELECT firstname, lastname FROM tbl_users WHERE username = '$username' AND password = '$password'";
		if(! mysqli_query($db, $query)){
			echo("Error description: " . $db -> error);
		}

		$clean_username = mysqli_real_escape_string($db, $username);
		$clean_query = "SELECT firstname, lastname FROM tbl_users WHERE username = '$clean_username' AND password = '$password'";
		$clean_result = mysqli_query($db, $clean_query);

		$row = $clean_result->fetch_array(MYSQLI_BOTH);

		if ($row === null) {
			http_response_code(400);
			echo "Incorrect credentials";
		} else {
			$name = $row[0] . " "  . $row[1];
			$_SESSION['login_username'] = $username;
			$_SESSION['login_name'] = $name;
			header("location: profile.php");
		}
	}
?>

<html>
	<head>
		<title>Login</title>
	</head>
	<body>
		<h1>Login</h1>
		<form method="POST">
			Username: <input type="text" name="username"/>
			<br/>
			Password: <input type="password" name="password"/>
			<input type="submit"/>
		</form>
	</body>
</html>
