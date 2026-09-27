**CWE-352: Cross-Site Request Forgery (CSRF)** occurs when a web application accepts a state-changing request without verifying that the request was intentionally made by the authenticated user.

### Vulnerable Python example

Using Flask:

```python
from flask import Flask, request, session

app = Flask(__name__)

@app.route("/change-email", methods=["POST"])
def change_email():
    # Vulnerable: no CSRF protection
    new_email = request.form["email"]

    update_email(session["user_id"], new_email)

    return "Email changed"

def update_email(user_id, email):
    print(f"Updating user {user_id} to {email}")

app.run()
```

If the user is logged in, their browser may automatically send their authentication cookie with a cross-site request. Without CSRF protection, another website could potentially cause the browser to submit the state-changing request.

### Safer version with Flask-WTF

Install Flask-WTF:

```bash
pip install flask-wtf
```

Then enable CSRF protection:

```python
from flask import Flask, request, session
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = "change-this-secret"

csrf = CSRFProtect(app)

@app.route("/change-email", methods=["POST"])
def change_email():
    new_email = request.form["email"]

    update_email(session["user_id"], new_email)

    return "Email changed"

def update_email(user_id, email):
    print(f"Updating user {user_id} to {email}")

app.run()
```

Your HTML form would include a CSRF token:

```html
<form method="POST" action="/change-email">
    <input type="hidden"
           name="csrf_token"
           value="{{ csrf_token() }}">

    <input type="email" name="email">
    <button type="submit">Change email</button>
</form>
```

The server verifies that the token came from the legitimate application before processing the request.

### For APIs

For cookie-authenticated APIs, use appropriate CSRF protections such as a CSRF token/header pattern and restrictive cookie settings. If an API uses an `Authorization: Bearer ...` header that JavaScript must explicitly supply, the traditional browser-cookie CSRF scenario is different, although other authorization and CORS issues still need consideration.

**Key idea:** authentication answers *“who is making the request?”*; CSRF protection helps verify *“did this authenticated user intentionally initiate this state-changing request?”*

