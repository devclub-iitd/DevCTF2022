<html>
	<head>
		<title>Profile</title>
	</head>
	<body>
<?php 
	session_start();
	echo $_SESSION["login_username"];
	if($_SERVER["REQUEST_METHOD"] === "POST") {
		session_start();
		if (session_destroy()) {
			header("location: login.php");
		}
	}
	session_start();
	if (isset($_SESSION['login_username'])) {
		echo "You are logged in!\n";
		echo getenv('RAW_FLAG');
	} else {
		header('location: login.php');
	}
?>
	<form method="POST">
		<input type="submit" value="Logout"/>
	</form>
	</body>
</html>


