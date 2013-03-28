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
choose = [1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,5,5,6,6,7,7,8]


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

def makeHaiku():
    s = ""
    s = s + makeLine(5) + '<br/>'
    s = s + makeLine(7) + '<br/>'
    s = s + makeLine(5)
    return s

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

sylls = getDict()

###################################

#fours = sylls['4']
#parts = nltk.pos_tag(fours)

#nouns = getNouns()
#verbs = getVerbs()
#adjectives = getAdjectives()
#adverbs =getAdverbs()
#prepositions = getPrepositions()

print makeHaiku()


##################################

def getRhymes(word):
    url = "http://rhymebrain.com/talk?function=getRhymes&word=%s"%(word)
    result = json.loads(urllib2.urlopen(url).read())
    words = [[x['syllables'], x['word']] for x in result]
    words =  words[:len(words)/2]
    return words

def getRhyme(num, words):
    x = [word for word in words if word[0] == str(num)]
    if len(x) == 0:
        return ""
    else:
        return choice(x)[1]

#x is num of syllables for the line, word is word to rhyme on
def makeRhymingLine(x, word):
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
                makeRhymingLine(orig,w)
                break
        #not last word
        else:
            line+= choice(sylls[str(num)])
            line+= " "
        x = x - num
    return line

def makeFakeSonnet(word):
    line = ""
    #print getRhymes(word)
    for i in range(0,10):
        line += makeRhymingLine(10,word) + '\n'
    return line
    


#print makeFakeSonnet('good')

