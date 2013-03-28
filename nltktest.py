import nltk, re, nltk.data,curses, random
from curses.ascii import isdigit
from nltk.corpus import cmudict

"""
ADJ / JJ        adjective	
ADV / RB	adverb	     
CC              coordinating conjunction   
CNJ	        conjunction	
DET	        determiner	
EX	        existential	
FW	        foreign word	
MOD	        modal verb	
N / NN	        noun	        
NP	        proper noun	
NUM	        number	        
PRO	        pronoun	        
P / PRP / IN	preposition	
TO       	the word to	
UH      	interjection	
V / VB / VBP 	verb	        
VD      	past tense	
VG      	present participle	
VN      	past participle	
WH      	wh determiner	
"""



sentence = "Everyday each one of you will be Emailed a name. That is the name of the person whom you are to seek out and try to mark with a marker or highlighter. Once you have successfully marked that person, he/she should tell you the name of his/her target, which now becomes your new target. The person whom you just marked is eliminated from the game. Remember that while you are on the lookout for your target, you yourself are also being searched for. Your objective is to remain unmarked and become the last man standing in which case you win!  If you see yourself or another person about to be marked, you may say the word Assassin, and you or that person will be immune for the duration of that class period, ONLY from the person who tried to mark you or another person at the time you said Assassin."

tokens = nltk.word_tokenize(sentence)

tagged = nltk.pos_tag(tokens)

#print tagged

verbs = [x for x in tagged if x[1] == 'VB']
#print verbs

PRP = [x for x in tagged if x[1] == 'PRP']
#print PRP


words = open("words.text").readlines()
words = [x.strip() for x in words]
#print words
d = cmudict.dict()
#print d
sylls = {0:[]}


def nysl(word):
    try:
        return [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]
    except:
        return "word is not in cmudict"


regexp = "[A-Za-z]+"
apos = ".*'.*"
exp = re.compile(regexp)
exp2 = re.compile(apos)

def makeSyllablesDict():
    for a in words:
        a = a.lower()
        if exp.match(a) and not exp2.match(a):
            if nysl(a)[0] not in sylls:
                sylls[nysl(a)[0]] = [a]
            else:
                sylls[nysl(a)[0]].append(a)
            #print a +" " + str(nysl(a)[0])  
    return sylls


makeSyllablesDict()
print sylls.keys()
fours = sylls[4]
parts = nltk.pos_tag(fours)
print fours


#x = random.randint(5,50)
#print fours[x]
#text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
#print text.similar(fours[x])

#make a line of 10 syllables
def makeLine(x = 10):
    line = ""
    while x > 0:
        if x > 8:
            num = random.randint(1,8)
        else:
            num = random.randint(1,x)
        #print num
        y = random.randint(0,len(sylls[num]))
        line+= " "
        line+= sylls[num][y]
        x = x - num
    return line


print makeLine(5)
print makeLine(7)
print makeLine(5)
