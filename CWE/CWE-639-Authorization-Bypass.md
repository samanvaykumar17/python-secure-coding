**CWE-639: Authorization Bypass Through User-Controlled Key** occurs when an application uses a user-controlled identifier—such as `user_id`, `account_id`, or `document_id`—to access an object without verifying that the authenticated user is authorized to access it.

### Vulnerable Python example

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
}

@app.route("/profile")
def profile():
    user_id = int(request.args["user_id"])

    # No authorization check
    user = users.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)

app.run()
```

If Alice is authenticated, she might normally request:

```text
/profile?user_id=1
```

But changing the parameter to:

```text
/profile?user_id=2
```

could expose Bob's information.

### Safer version

The server should derive the identity from the authenticated session/token and verify authorization before accessing the object:

```python
from flask import Flask, session, jsonify, abort

app = Flask(__name__)

users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
}

@app.route("/profile")
def profile():
    # Obtained from the authenticated session
    current_user_id = session.get("user_id")

    if current_user_id is None:
        abort(401)

    user = users.get(current_user_id)

    if not user:
        abort(404)

    return jsonify(user)
```

### Another common pattern

For resources where users can legitimately request an ID, perform an explicit authorization check:

```python
@app.route("/document/<int:document_id>")
def document(document_id):
    current_user_id = session.get("user_id")

    document = get_document(document_id)

    if document is None:
        abort(404)

    if document.owner_id != current_user_id:
        abort(403)

    return jsonify(document.to_dict())
```

The important distinction is:

> **Authentication:** “Who is the user?”
> **Authorization:** “Is this user allowed to access this particular object?”

CWE-639 commonly appears as an **IDOR (Insecure Direct Object Reference)** vulnerability when an attacker can change an object identifier and access another user's resource.
