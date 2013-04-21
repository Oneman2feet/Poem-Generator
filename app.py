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

    #If the user is in the session
    if 'user' in session:
        print "USER IN SESSION"
        if request.method == "GET":
            return render_template("home.html"
                                   ,poems=poems
                                   ,loggedin=True
                                   ,error=error)

    #If the user is not in the session
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        button = request.form['button']

        #If the button pressed is Login
        if button=='Login':
            if mongo.checkUser(username, password):
                session['user'] = username
                poems = mongo.getPoems(username)
                return render_template("profile.html"
                                       ,user=username
                                       ,poems=poems)
            else:
                error = "Incorrect username or password"
                return render_template("home.html"
                                       ,poems=poems
                                       ,loggedin=False
                                       ,error=error)

        #If the button pressed is Register
        elif button=='Register':
            if not mongo.exists(username, password):
                session['user'] = username
                mongo.addUser(username, password)
                poems = []
                return render_template("profile.html"
                                       ,user=username
                                       ,poems=poems)
            else:
                error = "Username already exists"
                return render_template("home.html"
                                       ,poems=poems
                                       ,loggedin=False
                                       ,error=error)
        
    return render_template("home.html",poems=poems,loggedin=False,error=error)


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

    #If something happens
    if request.method == "POST":
        button = request.form['button']

        #If the button pressed is Generate
        if button == "Generate":
            typer = request.form['type']
            rhyme1 = request.form['rhyme1']
            rhyme2 = request.form['rhyme2']

            #Makes sure there is a type selected
            if typer != "":
                 made = True
            #Makes a Haiku
            if typer == "haiku":
                poem = init.makeHaiku()
            #Makes a sonnet, checks both rhyming boxes
            if typer == "sonnet":
                if rhyme1 == "" or rhyme2 == "":
                    poem = ["Error, blank rhyming box."
                            ,"Please fill in both boxes for rhyming words"]
                    return render_template("makepoem.html",poem=poem,made=False)
                poem = init.makeBetterSonnet(rhyme1,rhyme2)
            #Makes a free verse, checks both rhyming boxes, checks # of lines   
            if typer == "free verse":
                if rhyme1 == "" or rhyme2 == "":
                    poem = ["Error, blank rhyming box."
                            ,"Please fill in both boxes for rhyming words"]
                    return render_template("makepoem.html",poem=poem,made=False)
                lines = request.form['lines']
                if lines == "":
                    poem = ["Error, blank number of lines"
                            ,"Please enter a number of lines"]
                    return render_template("makepoem.html",poem=poem,made=False)
                else:
                    poem = init.makeFreeVerse(rhyme1,rhyme2,int(lines))
            
            return render_template("makepoem.html",poem=poem,made=made)
        #After generating the poem, adds it to the user's poems
        if button == "Add Poem":
            mongo.addPoem(user, poem)
            poem = ["Would you like to make a new poem?"]
            return render_template("makepoem.html",poem=poem,made=False)

    return render_template("makepoem.html",poem="",made=made)


@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user',None)
    user = None
    print "LOGGED OUT"
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 7999)



