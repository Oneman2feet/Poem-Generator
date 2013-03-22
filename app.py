from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "blah"

@app.route("/", methods = ["GET"])
def home():
    return render_template("home.html")

