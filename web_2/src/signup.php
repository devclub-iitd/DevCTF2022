<?php

	include("config.php");

	if($_SERVER["REQUEST_METHOD"] === "POST") {
		$name = mysqli_real_escape_string($db, $_POST['name']);
		$user_id = mysqli_real_escape_string($db, $_POST['user_id']);
		$password = mysqli_real_escape_string($db, $_POST['password']);
		$h = md5($password, false);
		
		$result = $db -> query("SELECT COUNT(user_id) FROM $TBL WHERE user_id='$user_id';");
		$row = $result->fetch_array(MYSQLI_BOTH);
		
		if ($row[0] != 0) { // Gives "0" as string
			http_response_code(400);
			echo "Account with user id $user_id already exists!";
		} else {
			$result = $db -> query("INSERT INTO $TBL VALUES ('$user_id', '$h', '$name');");
			if ($db -> affected_rows === 0) {
				http_response_code(500);
				echo "Some error occurred!";
			} else {
				echo "<script>";
				echo "	window.alert('Account successfully created!');";
				echo "	window.location = 'login.php';";
				echo "</script>";
			}
		}
	}
?>

<html>
	<head>
		<title>Sign Up</title>
	</head>
	<body>
		<h1>Sign Up</h1>
		<form method="POST">
			Name: <input type="text" name="name"/>
			<br/>
			User ID: <input type="text" name="user_id"/>
			<br/>
			Password: <input type="password" name="password"/>
			<br/>
			<input type="submit"/>
		</form>
	</body>
</html>

