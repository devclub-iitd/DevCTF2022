<html>
	<head>
		<title>Profile</title>
	</head>
	<body>

<?php 
	session_start();
	
	if ($_SERVER["REQUEST_METHOD"] === "POST") {
		if (session_destroy()) {
			header("location: login.php");
		}
	}
	
	if (isset($_SESSION['login_name'])) {
		echo "Hello " . $_SESSION['login_name'];
	} else {
		header('location: login.php');
	}
?>

	<form method="POST">
		<input type="submit" value="Logout"/>
	</form>
	<p><a href="reset.php">Change Password</a>
	</body>
</html>

