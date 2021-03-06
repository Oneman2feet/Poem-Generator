from flask import Flask, render_template, request, redirect, session
import mongo, init, markov

app = Flask(__name__)
app.secret_key = "blahbbb"

#global user
#global poem
#poem = "" 

@app.route("/", methods = ["GET", "POST"])
def home():
    print "HOME PAGE ###"
    #global poem
    poem = []
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
        print "USER NOT IN SESSION"
        username = request.form.get("username")
        password = request.form.get("password")
        button = request.form['button']

        #If the button pressed is Login
        if button=='Login':
            print "LOGGING IN #############"
            if mongo.exists(username,password):
                if mongo.checkUser(username, password):
                    session['user'] = username
                    poems = mongo.getPoems(username)
                    poems.reverse()
                    return render_template("profile.html"
                                       ,user=username
                                       ,poems=poems)
                else:
                    error = "Incorrect password"
                    return render_template("home.html"
                                       ,poems=poems
                                       ,loggedin=False
                                       ,error=error)
            else:
                error = "Username does not exist"
                return render_template("home.html"
                                       ,poems=poems
                                       ,loggedin=False
                                       ,error=error)

        #If the button pressed is Register
        elif button=='Register':
            print "ADDING USER ########"
            if not mongo.exists(username, password):
                session['user'] = username
                mongo.addUser(username, password)
                poem = []
                print "ADDED USER"
                return redirect("/generate")
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
    print "GENERATE PAGE"
    if 'user' not in session:
        return redirect("/")
    
    #global user
    user = session['user']
    print "USER"
    print user
    
    #global poem
    #print "POEM"
    #print poem
    if 'poem' in session.keys():
        poem=session['poem']
    else:
        poem=""
    made = False
    added = False

    #If something happens
    if request.method == "POST":
        print "SOMETHING HAPPENED"
        button = request.form['button']
        
        #If the button pressed is Generate
        if button == "Generate":
            typer = request.form['type']
            rhyme1 = request.form['rhyme1']
            rhyme2 = request.form['rhyme2']

            print "MAKING POEM"

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
                    return render_template("makepoem.html",poem=poem,made=False,added=False)
                poem = init.makeBetterSonnet(rhyme1,rhyme2)
            #Makes a free verse, checks both rhyming boxes, checks # of lines   
            if typer == "free verse":
                if rhyme1 == "" or rhyme2 == "":
                    poem = ["Error, blank rhyming box."
                            ,"Please fill in both boxes for rhyming words"]
                    return render_template("makepoem.html",poem=poem,made=False,added=False)
                lines = request.form['lines']
                if lines == "":
                    poem = ["Error, blank number of lines"
                            ,"Please enter a number of lines"]
                    return render_template("makepoem.html",poem=poem,made=False,added=False)
                else:
                    poem = init.makeFreeVerse(rhyme1,rhyme2,int(lines))
            if typer == "shakespeare":
                lines = int(request.form['lines'])
                poem = markov.makepoem(lines,'shakespeare')
            if typer == "dickinson":
                lines = int(request.form['lines'])
                poem = markov.makepoem(lines,'dickinson')
            if typer == "poe":
                lines = int(request.form['lines'])
                poem = markov.makepoem(lines,'poe')
            if typer == "whitman":
                lines = int(request.form['lines'])
                poem = markov.makepoem(lines,'whitman')

            #poem = poem
            print "MADE POEM"
            print poem
            session['poem']=poem
            return render_template("makepoem.html",poem=poem,made=made,added=False)

        #After generating the poem, adds it to the user's poems
        if button == "Add Poem":
            print "ADDING POEM"
            print poem
            mongo.addPoem(user, poem)
            return render_template("makepoem.html",poem=poem,made=False,added=True)
    try:    
        print poem
    except:
        poem=""
        print poem
    return render_template("makepoem.html",poem="",made=made,added=added)


@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user',None)
    user = None
    print "LOGGED OUT"
    return redirect("/")

@app.route("/<poemid>")
def poempage(poemid=None):
    if poemid == None:
        return redirect("/")
    else:
        poem = mongo.getPoemByID(poemid)
        url = "http://ml7.stuycs.org:7999/%s"%(str(poemid))
        return render_template("poempage.html",poem=poem,url=url)

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 7999)



