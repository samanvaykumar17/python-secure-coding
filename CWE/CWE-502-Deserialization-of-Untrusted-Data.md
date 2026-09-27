**CWE-502: Deserialization of Untrusted Data** occurs when an application deserializes data from an untrusted source without sufficiently validating it first. In Python, a classic example is unsafe use of `pickle`.

### Vulnerable Python example

```python
import pickle

def load_data(user_data):
    # Vulnerable: user-controlled data is deserialized
    data = pickle.loads(user_data)
    return data
```

If `user_data` comes from an HTTP request, uploaded file, cookie, or other untrusted source, `pickle.loads()` can execute attacker-controlled behavior during deserialization.

For example, this is dangerous:

```python
from flask import Flask, request
import pickle

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    data = pickle.loads(request.data)  # CWE-502
    return str(data)

app.run()
```

The important issue isn't merely that the data is malformed. **Python pickle is capable of invoking code while reconstructing objects**, so treating an untrusted pickle as ordinary data can lead to remote code execution.

### Safer approach

If you only need structured data, use a data-only serialization format such as JSON:

```python
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400

    return jsonify(data)

app.run()
```

For example, JSON can represent:

```json
{
    "username": "alice",
    "age": 25
}
```

but it doesn't provide pickle's arbitrary Python-object reconstruction mechanism.

### Key rule

**Don't use `pickle.loads()` on data you don't completely trust.**

If pickle is required for an internal/trusted system, protect the serialized data with appropriate authentication/integrity controls and ensure the source is genuinely trusted. Even then, avoid treating signatures as a substitute for authorization or source validation.
