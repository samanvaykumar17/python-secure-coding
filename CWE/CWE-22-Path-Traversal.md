**CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')** occurs when user-controlled input is used to construct a filesystem path without ensuring that the resulting path stays within the intended directory.

### Vulnerable Python example

```python
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route("/download")
def download():
    filename = request.args.get("filename")

    # Vulnerable: user controls part of the filesystem path
    path = "/var/www/files/" + filename

    return send_file(path)

app.run()
```

The application intends to serve files from:

```text
/var/www/files/
```

But a request containing a traversal sequence such as:

```text
/download?filename=../../some-file
```

can cause the application to resolve a path outside the intended directory.

### Safer version

Use a fixed base directory and verify the **resolved** path:

```python
from flask import Flask, request, send_file, abort
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path("/var/www/files").resolve()

@app.route("/download")
def download():
    filename = request.args.get("filename", "")

    requested = (BASE_DIR / filename).resolve()

    # Ensure the resolved path remains inside BASE_DIR
    try:
        requested.relative_to(BASE_DIR)
    except ValueError:
        abort(403, "Invalid path")

    if not requested.is_file():
        abort(404)

    return send_file(requested)

app.run()
```

### Even safer when only filenames are needed

If users should only select files directly inside the directory, avoid accepting arbitrary path components:

```python
from pathlib import Path

filename = request.args["filename"]

if Path(filename).name != filename:
    abort(400, "Invalid filename")
```

Then resolve the resulting path against the known directory.

**Key point:** don't rely only on checking for strings such as `"../"`. Normalize/resolve the path and verify that the final location is within the permitted directory. Also consider symlinks and filesystem permissions when designing the file-serving mechanism.
