**CWE-306: Missing Authentication for Critical Function** occurs when an application exposes a sensitive function or resource without first verifying that the requester is authenticated.

### Vulnerable Python example

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/admin/delete-user", methods=["POST"])
def delete_user():
    user_id = request.form["user_id"]

    # Vulnerable: no authentication check
    delete_user_from_database(user_id)

    return "User deleted"

def delete_user_from_database(user_id):
    print(f"Deleting user {user_id}")

app.run()
```

Anyone who can reach the endpoint could potentially invoke the critical operation:

```text
POST /admin/delete-user
user_id=123
```

There is **no check that the requester is logged in**.

### Safer version

```python
from flask import Flask, session, request, abort

app = Flask(__name__)

@app.route("/admin/delete-user", methods=["POST"])
def delete_user():
    # Authentication check
    if "user_id" not in session:
        abort(401, "Authentication required")

    user_id = request.form["user_id"]

    delete_user_from_database(user_id)

    return "User deleted"

def delete_user_from_database(user_id):
    print(f"Deleting user {user_id}")

app.run()
```

For an administrative function, authentication alone is usually **not enough**. You should also perform an authorization check:

```python
if "user_id" not in session:
    abort(401)

if not current_user_is_admin():
    abort(403)
```

### CWE-306 vs CWE-639

| CWE         | Problem                                                                                   |
| ----------- | ----------------------------------------------------------------------------------------- |
| **CWE-306** | No authentication before accessing a critical function                                    |
| **CWE-639** | User is authenticated, but can access another user's object by manipulating an identifier |

For example, `/admin/delete-user` with **no login check** is CWE-306, while a logged-in user changing `user_id=123` to `user_id=456` without an ownership/authorization check is more closely related to CWE-639.
