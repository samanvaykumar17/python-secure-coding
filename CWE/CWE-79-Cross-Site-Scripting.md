**CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting', or XSS)** occurs when untrusted input is included in HTML without proper output encoding.

### Vulnerable Python example

Using Flask:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/hello")
def hello():
    name = request.args.get("name", "")

    # Vulnerable: user input is inserted directly into HTML
    return f"<h1>Hello, {name}!</h1>"

app.run()
```

The application expects:

```text
/hello?name=Alice
```

But an attacker could supply HTML/JavaScript as the `name` value. Because the application places the value directly into the HTML response, the browser may interpret it as markup or script.

### Safer version

Use Flask/Jinja2's HTML escaping rather than constructing HTML with an f-string:

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/hello")
def hello():
    name = request.args.get("name", "")

    return render_template_string(
        "<h1>Hello, {{ name }}!</h1>",
        name=name
    )

app.run()
```

Jinja2's autoescaping converts HTML-sensitive characters in `name` into safe representations before putting them into the page.

### Even better: use a template

`templates/hello.html`:

```html
<!doctype html>
<html>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
```

Python:

```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/hello")
def hello():
    return render_template(
        "hello.html",
        name=request.args.get("name", "")
    )

app.run()
```

### Key point

Avoid:

```python
return f"<p>{user_input}</p>"
```

Prefer:

```python
return render_template("page.html", value=user_input)
```

with the template engine's **context-appropriate output escaping** enabled.

**CWE-79 vs CWE-22:** CWE-79 concerns untrusted input being interpreted in a web page, while CWE-22 concerns untrusted input escaping an intended filesystem directory.
