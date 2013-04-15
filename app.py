from flask import Flask, render_template, request, redirect, session
import init, mongo

app = Flask(__name__)
app.secret_key = "blah"

global current_user

@app.route("/", methods = ["GET", "POST"])
def home():
    #this is the code for using session when db is written
    mongo.conn()

    #if request.method == "GET":
    global current_user
    button = str(request.form["button"])
    if button == "Login":
        username = request.form.get("username")
        password = request.form.get("password")
        if mongo.exists(username, password):
            poems = mongo.get_poems(current_user)
            return redirect("/"+current_user) #might change
        else:
            return "Username is taken"
       
    poems = [str(init.makeHaiku()) for x in range(0,10)]
    return render_template("home.html", poems=poems)

@app.route("/profile", methods = ["GET"])
def profile():
    return render_template("profile.html")

@app.route("/generate", methods = ["GET","POST"])
def generate():
    return render_template("makepoem.html", user = user)

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 5000)
