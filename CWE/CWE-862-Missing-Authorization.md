**CWE-862: Missing Authorization** occurs when an application authenticates a user but fails to check whether that user is actually authorized to perform a requested action.

### Vulnerable Python example

```python
from flask import Flask, session, request

app = Flask(__name__)

@app.route("/admin/delete-user", methods=["POST"])
def delete_user():
    # User is authenticated, but there is no authorization check
    if "user_id" not in session:
        return "Login required", 401

    user_id = request.form["user_id"]

    delete_user_from_database(user_id)

    return "User deleted"

def delete_user_from_database(user_id):
    print(f"Deleting user {user_id}")

app.run()
```

Here, a normal authenticated user can potentially call `/admin/delete-user` because the application checks only:

```python
"user_id" in session
```

It does **not** check whether that user has administrator privileges.

### Safer version

```python
from flask import Flask, session, request, abort

app = Flask(__name__)

@app.route("/admin/delete-user", methods=["POST"])
def delete_user():
    current_user_id = session.get("user_id")

    if current_user_id is None:
        abort(401, "Authentication required")

    if not is_admin(current_user_id):
        abort(403, "Authorization required")

    user_id = request.form["user_id"]

    delete_user_from_database(user_id)

    return "User deleted"

def is_admin(user_id):
    # Example: retrieve role from your database
    return get_user_role(user_id) == "admin"

def get_user_role(user_id):
    # Placeholder
    return "admin"

def delete_user_from_database(user_id):
    print(f"Deleting user {user_id}")

app.run()
```

### Authentication vs. authorization

```text
Authentication
      ↓
"Who are you?"
      ↓
Authenticated user
      ↓
Authorization
      ↓
"Are you allowed to perform this action?"
      ↓
Allow / Deny
```

**CWE-862** is specifically about the missing authorization step.

### CWE-862 vs CWE-639

* **CWE-862:** The application doesn't properly check whether the authenticated user is allowed to perform an operation.
* **CWE-639:** The application uses a user-controlled object identifier and fails to verify that the authenticated user is authorized to access that particular object.

For example, allowing any logged-in user to call `/admin/delete-user` is a typical **CWE-862** pattern.

