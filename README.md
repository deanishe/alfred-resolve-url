# Resolve HTTP Redirects — an Alfred 2 Workflow #

Follows any HTTP redirects and returns the canonical URL.

![](https://raw.githubusercontent.com/deanishe/alfred-resolve-url/master/demo.gif "demo.gif")

You can paste a URL into Alfred's query box or grab a URL directly from the clipboard.

## Usage ##

- `resolve URL` — Find and display the canonical URL after all redirects.
	+ `↩` — Copy the new URL to the clipboard
	+ `⌘+↩` — Open the new URL in your default browser
- `resolvepb` — Grab the URL from the clipboard and resolve any redirects as above.

If the URL has no redirects, a "No redirects" message will be displayed.

## Licence, thanks ##

This workflow is released under the [MIT licence](http://opensource.org/licenses/MIT). It uses [Alfred-Workflow](http://www.deanishe.net/alfred-workflow/index.html) for the plumbing and to resolve HTTP redirects.
