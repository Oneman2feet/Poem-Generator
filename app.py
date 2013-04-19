from flask import Flask, render_template, request, redirect, session
import mongo, init

app = Flask(__name__)
app.secret_key = "blah"

global user

@app.route("/", methods = ["GET", "POST"])
def home():
    poems = mongo.getAllPoems()
    poems.reverse()
    poems = poems[:10]

    if 'user' in session:
        if request.method == "GET":
            return render_template("home.html",poems=poems,loggedin=True)
        if request.method == "POST":
            print "LOGOUT"
            logout()
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if mongo.exists(username, password):
            session['user'] = username
            poems = mongo.getPoems(username)
            return render_template("profile.html",user=username,poems=poems)
        else:
            print "Incorrect username or password"
        
    return render_template("home.html", poems=poems,loggedin=False)

@app.route("/profile", methods = ["GET","POST"])
def profile():
    if 'user' in session:
        user = session['user']
        poems = mongo.getPoems(user)
        print poems
        return render_template("profile.html", user=user,poems=poems)
    else:
        print "User Not Logged In"
        return redirect("/")

@app.route("/generate", methods = ["GET","POST"])
def generate():
    user = session['user']
    poem=""
    if request.method == "POST":
        print request.form
        typer = request.form['type']
        if typer == "haiku":
            poem = init.makeHaiku()
            mongo.addPoem(user,poem)
        if typer == "sonnet":
            poem = init.makeBetterSonnet("me","you")
            mongo.addPoem(user,poem)
        if typer == "free verse":
            lines = request.form['lines']
            if lines == "":
                poem = init.makeFreeVerse("me","you",8)
            else:
                poem = init.makeFreeVerse("me","you",int(lines))
            mongo.addPoem(user,poem)
    return render_template("makepoem.html",poem=poem)

@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if mongo.exists(username,password):
            mongo.addUser(username,password)
            session['user'] = username
            poems = []
            return render_template("profile.html",user=username,poems=poems)
        else:
            print "This Username has already been taken"  
    return render_template("register.html")

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user',None)
    user = None
    print "LOGGED OUT"
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 7755)



