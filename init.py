import nltk, re, nltk.data, curses, random, shelve, urllib2, json
from curses.ascii import isdigit
from nltk.corpus import cmudict
from random import choice


words = open("words.text").readlines()
words = [x.strip().lower() for x in words]
words = list(set(words))
words.sort()
d = cmudict.dict()
sylls = {'0':[]}

nouns = {}
verbs = {}
adjectives = {}
adverbs = {}
prepositions = {}

regexp = "[A-Za-z]+"
apos = ".*'.*"
exp = re.compile(regexp)
exp2 = re.compile(apos)

####Making it more even probability wise
choose = []
for x in range(0,22):
    choose.append(1)
for x in range(0,63):
    choose.append(2)
for x in range(0,42):
    choose.append(3)
for x in range(0,18):
    choose.append(4)
for x in range(0,5):
    choose.append(5)
choose.append(6)
choose.append(7)
choose.append(8)
######

def nysl(word):
    try:
        return [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]
    except:
        return "word is not in cmudict"




def makeSyllablesDict():
    sylls = shelve.open("syl")
    for a in words:
        key = str(nysl(a)[0])
        if exp.match(a) and not exp2.match(a):
            if key in sylls:
                l = sylls[key]
                l.append(a)
                sylls[key] = l
            else:
                sylls[key] = [a]
        #print a +" " + str(nysl(a)[0])  
   # print sylls
    return sylls

def getDict():
    syl = shelve.open("syl")
    return syl


#make a line of 10 syllables
def makeLine(x = 10):
    line = ""
    while x > 0:
        #get num of syllables
        num = choice([s for s in choose if s <= x])
        line+= choice(sylls[str(num)])
        line+= " "
        x = x - num
    return line



####### Making shelves
def makePreps():
    syl = shelve.open("syl")
    preps = shelve.open("prepositions")
    x = {}
    for item in syl:
        l = nltk.pos_tag(syl[item])
        x[item] = l
    #print x
    
    for item in x:
        preps[item] = []
        for word in x[item]:
            print word
            if word[1] == "P" or word[1] == "PRP" or word[1] == "IN":
                l = preps[item]
                l.append(word)
                preps[item] = l
    return adverbs
        
def getNouns():
    nouns = shelve.open("nouns")
    return nouns

def getVerbs():
    verbs = shelve.open("verbs")
    return verbs

def getAdjectives():
    adjectives = shelve.open("adjectives")
    return adjectives

def getAdverbs():
    adverbs = shelve.open("adverbs")
    return adverbs

def getPrepositions():
    preps = shelve.open("prepositions")
    return preps

##########

def getNoun(x):
    nouns = shelve.open("nouns")
    n = nouns[str(x)]
    return choice(n)

def getVerb(x):
    verbs = shelve.open("verbs")
    v = verbs[str(x)]
    return choice(v)[0]

def getAdverb(x):
    adverbs = shelve.open("adverbs")
    a = adverbs[str(x)]
    return choice(a)[0]

def getAdjective(x):
    adjectives = shelve.open("adjectives")
    a = adjectives[str(x)]
    return choice(a)[0]

sylls = getDict()

###################################

#fours = sylls['4']
#parts = nltk.pos_tag(fours)

#nouns = getNouns()
#verbs = getVerbs()
#adjectives = getAdjectives()
#adverbs =getAdverbs()
#prepositions = getPrepositions()

#print makeHaiku()


##################################

def getRhymes(word):
    url = "http://rhymebrain.com/talk?function=getRhymes&word=%s"%(word)
    result = json.loads(urllib2.urlopen(url).read())
    words = [[x['syllables'], x['word']] for x in result]
    if len(words) > 15:
        words =  words[:len(words)/3]
    words.append(word)
    return words

def getRhyme(num, words):
    x = [word for word in words if word[0] == str(num)]
    if len(x) == 0:
        return ""
    else:
        return choice(x)[1]

#x is num of syllables for the line, word is word to rhyme on
def makeRhymingLine(word, x=10):
    orig = x
    w = word
    words = getRhymes(word)
    line = ""
    while x > 0:
        #get num of syllables
        num = choice([s for s in choose if s <= x])
        
        #last word
        if x == num:
            r = getRhyme(num,words)
            if r != "":
                line+= r
            elif x > 1:
                line+= choice(sylls['1'])
                line+= " "
                num = 1
            else:
                line = ""
                x = orig
                num = 0                
        #not last word
        else:
            line+= choice(sylls[str(num)])
            line+= " "
        x = x - num
    return line

    
def makeLineSense(x):
    line = ""
    n = 0
    while x > 0:
        #get num of syllables
        num = choice([s for s in choose if s <= x])
        if n > 2:
            if x == 1:
                n = 0
                num = 0
            else:
                line+= "and"
                num = 1
                n = 0
        elif n == 2:
            line+= getVerb(num)
            n+= 1
        elif n == 1:
            line+= getAdjective(num)
            n+= 1
        elif n == 0:
            r = getNoun(num)
            if r[1] == "NNS" and x > 1:
                line += "the " + r[0]
                num = num + 1
            else:
                line+= r[0]
            n+= 1
        line+= " "
        x = x - num
    return line

def makeLineRhymeSense(x,word):
    line = ""
    orig = x
    w = word
    words = getRhymes(word)
    n = 0
    while x > 0:
        #get num of syllables
        num = choice([s for s in choose if s <= x])
        #last word
        if x == num:
            r = getRhyme(num,words)
            if r != "":
                line+= r
            elif x > 1:
                line+= choice(sylls['1'])
                line+= " "
                num = 1
            else:
                line = ""
                x = orig
                num = 0  
                n = 0
        #not last word 
        else:
            if n > 2:
                if x == 1:
                    n = 0
                    num = 0
                else:
                    line+= "and"
                    num = 1
                    n = 0
            elif n == 2:
                line+= getVerb(num)
                n+= 1
            elif n == 1:
                line+= getAdjective(num)
                n+= 1
            elif n == 0:
                g = getNoun(num)
                if g[1] == "NNS" and x > 1:
                    line += "the " + g[0]
                    num = num + 1
                elif g[1] == "NNS":
                    line+= getNoun(num)[0]
                    n+= 1
                else:
                    line+= g[0]
                    n+= 1
        line+= " "
        x = x - num
    return line




#print makeBetterSonnet("see","good")


##Poems

def makeHaiku():
    s = []
    s.append(makeLine(5))
    s.append(makeLine(7))
    s.append(makeLine(5))
    return s

def makeBetterSonnet(word1, word2):
    line = []
    #print getRhymes(word)
    for i in range(0,10):
        if i%2 == 0:
            line.append(makeLineRhymeSense(10,word1))
        else:
            line.append(makeLineRhymeSense(10,word2))
    return line

def makeFreeVerse(word1,word2,lines):
    line = []
    for i in range (0,lines):
        if i%2 == 0:
            line.append(makeLineRhymeSense(8,word1))
        else:
            line.append(makeLineRhymeSense(8,word2))
    return line
        
