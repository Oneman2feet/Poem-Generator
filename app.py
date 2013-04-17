from flask import Flask, render_template, request, redirect, session
import init, mongo

app = Flask(__name__)
app.secret_key = "blah"


@app.route("/", methods = ["GET", "POST"])
def home():
    #change this to 10 of most recent poems
    poems = [str(init.makeHaiku()) for x in range(0,10)]

    if request.method == "POST":
        button = request.form['button']
        if button == 'Login':
            username = request.form.get("username")
            password = request.form.get("password")
            if mongo.exists(username, password):
                session['user'] = username
                return redirect("profile.html")
            else:
                return "Username is taken"
        elif button == "Register":
            return redirect("register.html")
    return render_template("home.html", poems=poems)

@app.route("/profile", methods = ["GET"])
def profile():
    if 'user' in session:
        return render_template("profile.html")
    else:
        print "User Not Logged In"
        return redirect("home.html")

@app.route("/generate", methods = ["GET","POST"])
def generate():
    return render_template("makepoem.html", user = user)

@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        mongo.addUser(username,password)
        session['user'] = username
        return redirect("profile")
    
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 5000)



####Fix buttons
####
