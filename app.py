import logging

from flask import Flask, render_template, request, redirect, session
import hashlib

app = Flask(__name__)
app.secret_key = "secret_key"

# Store hashed passwords for demonstration purposes
user_database = {
    "user1": hashlib.sha256("password1".encode()).hexdigest(),
    "user2": hashlib.sha256("password2".encode()).hexdigest()
}

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)
logging.basicConfig(filename='login.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.route("/")
def index():
    if "username" in session:
        username = session["username"]
        return render_template("home.html", username=username)
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        if username in user_database and user_database[username] == password:
            session["username"] = username
            source_ip = request.remote_addr
            method = request.method
            url = request.base_url
            code = "200"
            message = "Successful login"
            logging.info(f"{source_ip} {username} {method} {url} {code} {message}")
            return redirect("/")
        else:
            source_ip = request.remote_addr
            method = request.method
            url = request.base_url
            code = "400"
            message = "Failed login attempt"
            logging.info(f"{source_ip} {username} {method} {url} {code} {message}")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
