<?php header("Accept: application/xml, application/x-www-form-urlencoded"); ?>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>ROT13</title>
	</head>
	<body>
		<form method="POST" action="./">
			Enter Text:
			<br/>
			<textarea rows=5 type="text" name="text"></textarea>
			<br/>
			<input type="submit"/>
		</form>
		<br/>
<?php
	if ($_SERVER["REQUEST_METHOD"] === "POST") {
		if ($_SERVER["CONTENT_TYPE"] === "application/xml") {
			libxml_disable_entity_loader (false);
			$xmlfile = file_get_contents('php://input');
			$dom = new DOMDocument();
			$dom -> loadXML($xmlfile, LIBXML_NOENT | LIBXML_DTDLOAD);
			$data = simplexml_import_dom($dom);
			$text = $data->text;
		} else if ($_SERVER["CONTENT_TYPE"] === "application/x-www-form-urlencoded") {
			$text = $_POST["text"];
		} else {
			http_response_code(415);
			exit;
		}
		$rot = str_rot13($text);
		echo "<h3>ROT13</h3>";
		echo "<textarea readonly>$rot</textarea>";
	}
?>
	</body>
</html>
