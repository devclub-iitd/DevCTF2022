<?php

	$category = "";

	if (strpos($_SERVER['HTTP_USER_AGENT'], "Mozilla/4.0") === false) {
		$category .= "New";
	} else {
		$category .= "Old";
	}
	
	$category .= " ";

	if (strpos($_SERVER['HTTP_USER_AGENT'], "Linux") !== false) {
		$category .= "Linux";
	} else if (strpos($_SERVER['HTTP_USER_AGENT'], "Windows NT 10.0") !== false) {
		$category .= "Windows 10";
	} else if (strpos($_SERVER['HTTP_USER_AGENT'], "Windows") !== false) {
		$category .= "Windows";
	} else if (strpos($_SERVER['HTTP_USER_AGENT'], "Macintosh") !== false) {
		$category .= "Mac";
	} else {
		$category .= "Other OS";
	}
	
	if (
		(strpos($_SERVER['HTTP_USER_AGENT'], "Mozilla/4.0") !== false)
		&& 
		(strpos($_SERVER['HTTP_USER_AGENT'], "Windows NT") !== false)
		&&
		(strpos($_SERVER['HTTP_USER_AGENT'], "Windows NT 10.0") === false)
	) {
		echo getenv("RAW_FLAG");
	} else {
		echo "Wrong Information, Our Community Members use Old Windows Laptops. You are using a $category";
	}

?>
