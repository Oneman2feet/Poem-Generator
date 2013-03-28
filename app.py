from flask import Flask, render_template, request
import init

app = Flask(__name__)
app.secret_key = "blah"

@app.route("/", methods = ["GET"])
def home():
    poems = [str(init.makeHaiku()) for x in range(0,10)]
    return render_template("home.html",poems=poems)

@app.route("/profile", methods = ["GET"])
def profile():
    return render_template("profile.html")

@app.route("/generate", methods = ["GET","POST"])
def generate():
    return render_template("makepoem.html")

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 5000)
