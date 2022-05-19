```
---> Challenge 6  : Challenge would host an endpoint on port 6666 (this port is restricted in the modern webbrowsers such as CHrome and Firefox).
					Candidtae will have to explicitly configure the WebBrowser to connect this port (this is a part of the challenge)

					Then after a webpage will display an input box will title "I am Pandoc, Send me something to Eat !"

					This will be hosting a Pandoc Server https://github.com/jgm/pandoc

					The candidate can run markdown / haskel using the provided input box on the WebServer, Now using file:// scheme he/she can read the flag at /flag.txt.
```

expolit :

<script src="file:///usr/share/man/man1/pandoc.1.gz"></script>
