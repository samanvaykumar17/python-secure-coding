**CWE-77: Improper Neutralization of Special Elements used in a Command ('Command Injection')** occurs when untrusted input is incorporated into an operating-system command without proper separation or validation.

### Vulnerable Python example

```python
from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/ping")
def ping():
    host = request.args.get("host")

    # Vulnerable: user input is directly included in a shell command
    result = os.popen("ping -c 1 " + host).read()

    return result

app.run()
```

The problem is that `host` is interpreted by the shell as part of the command rather than simply as data.

### Safer version

Avoid invoking a shell and pass arguments separately:

```python
from flask import Flask, request
import subprocess
import ipaddress

app = Flask(__name__)

@app.route("/ping")
def ping():
    host = request.args.get("host")

    try:
        ipaddress.ip_address(host)
    except ValueError:
        return "Invalid IP address", 400

    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True,
        timeout=5,
        check=False
    )

    return result.stdout

app.run()
```

### Key difference

**Vulnerable:**

```python
os.system("some-command " + user_input)
```

**Safer:**

```python
subprocess.run(["some-command", user_input], shell=False)
```

For CWE-77, the main defenses are **avoid shell execution when possible, use argument arrays with `shell=False`, validate input against an allowlist/expected format, and apply appropriate timeouts and privileges**.
