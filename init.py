import nltk, re, nltk.data, curses, random, shelve
from curses.ascii import isdigit
from nltk.corpus import cmudict

words = open("words.text").readlines()
words = [x.strip().lower() for x in words]
words = list(set(words))
words.sort()
d = cmudict.dict()
sylls = {'0':[]}

regexp = "[A-Za-z]+"
apos = ".*'.*"
exp = re.compile(regexp)
exp2 = re.compile(apos)


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
        if x > 8:
            num = random.randint(1,8)
        else:
            num = random.randint(1,x)
        #print num
        #get random index
        y = random.randint(0,len(sylls[str(num)]))
        #print y
        line+= " "
        line+= sylls[str(num)][y]
        x = x - num
    return line


sylls = getDict()

fours = sylls['4']
parts = nltk.pos_tag(fours)

print makeLine(5)
print makeLine(7)
print makeLine(5)
