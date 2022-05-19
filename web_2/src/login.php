<?php

	include("config.php");

	if($_SERVER["REQUEST_METHOD"] === "POST") {
		$user_id = mysqli_real_escape_string($db, $_POST['user_id']);
		$password = mysqli_real_escape_string($db, $_POST['password']);
		$h = md5($password, false);

		$result = $db -> query("SELECT name FROM $TBL WHERE user_id = '$user_id' AND hash = '$h';");

		$row = $result->fetch_array(MYSQLI_BOTH);

		if ($row === null) {
			http_response_code(400);
			echo "Incorrect credentials";
		} else {
			$name = $row[0];
			
			session_start();
			$_SESSION['login_name'] = $name;
			$_SESSION['login_user_id'] = $user_id;
			$_SESSION['login_hash'] = $h;
			
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
			User ID: <input type="text" name="user_id"/>
			<br/>
			Password: <input type="password" name="password"/>
			<input type="submit"/>
		</form>
		<br/>
		No Account? <a href="signup.php">Sign Up!</a>
	</body>
</html>

