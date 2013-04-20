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
    error = ""
    if 'user' in session:
        print "USER IN SESSION"
        if request.method == "GET":
            return render_template("home.html",poems=poems,loggedin=True,error=error)
    
    elif request.method == "POST":
        print "HI THERE PEOPLE"
        username = request.form.get("username")
        password = request.form.get("password")
        button = request.form['button']
        if button=='Login':
            if mongo.checkUser(username, password):
                session['user'] = username
                poems = mongo.getPoems(username)
                return render_template("profile.html",user=username,poems=poems)
            else:
                error = "Incorrect username or password"
                return render_template("home.html",poems=poems,loggedin=False,error=error)
        elif button=='Register':
            print mongo.exists(username,password)
            if not mongo.exists(username, password):
                session['user'] = username
                mongo.addUser(username, password)
                poems = []
                return render_template("profile.html",user=username,poems=poems)
            else:
                error = "Username already exists"
                return render_template("home.html",poems=poems,loggedin=False,error=error)
        
    return render_template("home.html", poems=poems,loggedin=False,error=error)

@app.route("/profile", methods = ["GET","POST"])
def profile():
    if 'user' in session:
        user = session['user']
        poems = mongo.getPoems(user)
        poems.reverse()
        return render_template("profile.html", user=user,poems=poems)
    else:
        print "User Not Logged In"
        return redirect("/")

@app.route("/generate", methods = ["GET","POST"])
def generate():
    user = session['user']
    poem=""
    made = False
    if request.method == "POST":
        print request.form
        made = True
        button = request.form['button']
        if button == "Add Poem":
            print "HI"
            mongo.addPoem(user,poem)
            poem = ["Would you like to make another poem?"]
            made = False
            return render_template("makepoem.html",poem=poem,made=made)
        if button == "Generate":
            typer = request.form['type']
            if typer == "haiku":
                poem = init.makeHaiku()
            if typer == "sonnet":
                poem = init.makeBetterSonnet("me","you")
            if typer == "free verse":
                lines = request.form['lines']
                if lines == "":
                    poem = init.makeFreeVerse("me","you",8)
                else:
                    poem = init.makeFreeVerse("me","you",int(lines))
            return render_template("makepoem.html",poem=poem,made=made)
    return render_template("makepoem.html",poem=poem,made=made)

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user',None)
    user = None
    print "LOGGED OUT"
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 7999)



