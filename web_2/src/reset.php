<html>
	<head>
		<title>Change Password</title>
	</head>
	<body>

<?php 
	include("config.php");

	session_start();
	if (isset($_SESSION['login_user_id'])) {
		echo "Change password for " . $_SESSION['login_user_id'];
	} else {
		header('location: login.php');
	}
	
	if ($_SERVER["REQUEST_METHOD"] === "POST") {
		$user_id = mysqli_real_escape_string($db, $_POST['user_id']);
		$pass = mysqli_real_escape_string($db, $_POST['pass']);
		$h = md5($pass, false);
		
		$result = $db -> query("UPDATE $TBL SET hash='$h' WHERE user_id='$user_id';");
		
		if ($db -> affected_rows === 0) {
			http_response_code(400);
			echo "<p>Invalid Request!</p>";
		} else {
			session_destroy();	
			echo "<script>";
			echo "	window.alert('Password has been reset for $user_id ! Please login again with new credentials');";
			echo "	window.location='login.php';";
			echo "</script>";
		}
	}
?>
	<br/>
	<form method="POST">
		<input type="hidden" value="<?php echo $_SESSION['login_user_id']; ?>" name="user_id"/>
		New Password: <input type="password" name="pass"/>
		<input type="submit"/>
	</form>
	</body>
</html>

