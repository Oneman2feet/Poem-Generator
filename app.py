from flask import Flask, render_template, request, redirect, session
import mongo, init

app = Flask(__name__)
app.secret_key = "blah"

global user
global poem
poem = "" 

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
    global poem
    made = False
    if request.method == "POST":
        print request.form
        button = request.form['button']
        if button == "Generate":
            typer = request.form['type']
            rhyme1 = request.form['rhyme1']
            rhyme2 = request.form['rhyme2']
            if typer != "":
                 made = True
            if typer == "haiku":
                poem = init.makeHaiku()
                print poem
                #addPoem()
            if typer == "sonnet":
                if rhyme1 == "":
                    rhyme1 = "word"
                if rhyme2 == "":
                    rhyme2 = "place"
                poem = init.makeBetterSonnet(rhyme1,rhyme2)
                #addPoem()
            if typer == "free verse":
                if rhyme1 == "":
                    rhyme1 = "word"
                if rhyme2 == "":
                    rhyme2 = "place"
                lines = request.form['lines']
                if lines == "":
                    poem = init.makeFreeVerse(rhyme1,rhyme2,8)
                else:
                    poem = init.makeFreeVerse(rhyme1,rhyme2,int(lines))
            return render_template("makepoem.html",poem=poem,made=made)
        if button == "Add Poem":
            mongo.addPoem(user, poem)
            return render_template("makepoem.html",poem=["Would you like to make a new poem?"],made=False)
    return render_template("makepoem.html",poem="",made=made)


@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user',None)
    user = None
    print "LOGGED OUT"
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 7999)



