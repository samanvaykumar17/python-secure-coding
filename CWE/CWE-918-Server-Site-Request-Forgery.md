**CWE-918: Server-Side Request Forgery (SSRF)** occurs when a server makes a network request to a URL controlled or influenced by an untrusted user, potentially allowing access to internal services or resources.

### Vulnerable Python example

```python
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/fetch")
def fetch():
    url = request.args.get("url")

    # Vulnerable: user controls the destination
    response = requests.get(url, timeout=5)

    return response.text

app.run()
```

The application might be intended to fetch public websites, but the attacker controls `url`. This can allow the server to make requests to destinations that the client cannot directly access, such as internal services.

### Safer approach

If the application only needs to retrieve files from a known set of external services, use an **allowlist** rather than accepting arbitrary URLs:

```python
from flask import Flask, request, abort
from urllib.parse import urlparse
import requests

app = Flask(__name__)

ALLOWED_HOSTS = {
    "api.example.com",
    "cdn.example.com",
}

@app.route("/fetch")
def fetch():
    url = request.args.get("url")

    parsed = urlparse(url)

    if parsed.scheme != "https":
        abort(400, "HTTPS required")

    if parsed.hostname not in ALLOWED_HOSTS:
        abort(403, "Host not allowed")

    response = requests.get(
        url,
        timeout=5,
        allow_redirects=False
    )

    return response.text

app.run()
```

### Important protections

For SSRF prevention:

* **Allowlist** permitted domains/hosts where possible.
* Restrict the URL scheme to expected protocols such as `https`.
* Don't allow arbitrary redirects.
* Validate the resolved destination, not just the original hostname, when arbitrary domains must be supported.
* Block access to internal/private network ranges where appropriate.
* Apply connection and response-size/time limits.
* Run the fetching component with minimal network privileges.

A common mistake is relying only on a check such as `url.startswith("https://example.com")`; URL parsing and redirects can make such checks unreliable.

