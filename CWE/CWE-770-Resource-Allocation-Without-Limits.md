**CWE-770: Allocation of Resources Without Limits or Throttling** occurs when a program allows users or inputs to consume excessive resources—such as memory, CPU, threads, files, or network connections—without enforcing reasonable limits.

### Vulnerable Python example

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/process")
def process():
    # User controls the size of the allocation
    size = int(request.args.get("size", 100))

    data = ["A" * 1024] * size
    return f"Allocated {len(data)} items"

app.run()
```

An attacker could request:

```text
/process?size=100000000
```

This can cause excessive memory consumption and potentially crash or degrade the server.

### Safer version

```python
from flask import Flask, request, abort

app = Flask(__name__)

MAX_ITEMS = 10_000
ITEM_SIZE = 1024

@app.route("/process")
def process():
    try:
        size = int(request.args.get("size", 100))
    except ValueError:
        abort(400, "Invalid size")

    if size < 0 or size > MAX_ITEMS:
        abort(400, "Size exceeds allowed limit")

    data = ["A" * ITEM_SIZE for _ in range(size)]

    return f"Allocated {len(data)} items"

app.run()
```

**Key mitigation:** never let untrusted input directly determine an unlimited resource allocation. Apply **maximum limits, quotas, timeouts, pagination, rate limiting, and concurrency limits** as appropriate.

A common real-world CWE-770 example is an API accepting an unlimited `limit`, file-upload size, batch size, or number of concurrent jobs.
