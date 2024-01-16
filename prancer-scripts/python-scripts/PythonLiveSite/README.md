# Using Live Site

The Live Site script will check if a given website is alive and returning a successful HTTP response.

- The script will first check for the correct syntax and look for the specified target URL.
- Next, it will send a Request to the target using `requests` library and check the HTTP status code from the Response.
- Based on the HTTP Reponse, it will determine the site is healthy and working properly or if it is down.
  - Note: This script will return successful responses for all HTTP status codes between 200-299. Any response outside of this range will state the site may not be live. For example, redirections (301) will get the same response as not found (404).

## Usage

`python livesite.py <targetURL>`

Successful response:
`Requested site <targetURL> is live. Status code 200`

Unsuccessful response:
`The site <targetURL> may not be live. Status code 301`
