```
---> Challenge 5  : WebPage would state that "Wrong Information, Our Community Members use Old Windows Laptop, You are using <Windows/Linux>"
					Version would be parsed from the User Agent.

					Task is to Curl to the WebPage or Send the Get request using custom Referer Header / Agent like : "Mozilla 4.0 Windows 7"

					Doing this would result in the flag being sent as resposne / displayed on the WebPage.
```

The solution will be like

`curl localhost:8000 -A "Mozilla/4.0 (Windows NT 6.1)"`
