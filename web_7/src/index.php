<?php
  $flag = getenv('RAW_FLAG');
  $password_hash = "0e613616395461613372060186931760"; 
  $salt = "f789bbc328a3d1a3";  				
  header("Salt " . $salt);
  if($_SERVER["REQUEST_METHOD"] === "POST") {
    setcookie("Salt", $salt, time(), "/", NULL, NULL, true); // 86400 = 1 day

    if ( ! isset($_POST['password'])) {
			http_response_code(400);
			echo "No password entered";
		} else {
      $pass = $_POST['password'];
      if(md5($salt . $pass, false) == $password_hash) {
        $msg = $flag;
      } else {
        // http_response_code(400);
        $msg = "Incorrect password ... Hashes do not match";
      }
      echo "<script>window.alert('$msg');</script>";
		}
	}
?>
  
  <html>
    <head>
      <title>The Big Bang</title>
    </head>
    <body>
	<h1>Enter Password</h1>
  <p>Hint 1 : You seriously need to get some NaCl !!! 
    <br>
  Hint 2 : Is the number of valence electrons in 3p orbital of PHosPhorous (3+) "equal" to ZERO ??  </p>

  <br>
  <form method="POST">
    Password: <input type="password" name="password"/>
    <input type="submit"/>
  </form>
	</body>
