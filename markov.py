import random
#parsed corpus in the form of a dictionary
#with keys being the seed words
#and data being the words that have come after that word

shakespeare = {}

def makecorpus():
    sonnets = open("sonnets.txt").readlines()
    sonnets = [ [word.lower().replace('(','').replace(')','')
                 for word in line.replace('\n',' \n').split(' ')
                 if word!='' and word!='\n']
                 for line in sonnets if line!='\n' ]

    for line in sonnets:
        for i in xrange(0,len(line)-1):
            if line[i] in shakespeare.keys():
                shakespeare[line[i]].append(line[i+1])
            else:
                shakespeare[line[i]] = [line[i+1]]


def makeline(startword,corpus):
    word = startword.lower()
    startword = startword[0:1].upper()+startword[1:].lower()
    return startword + " " + recursivemakeline(word,corpus)

def recursivemakeline(word,corpus):
    nextw = nextword(word,corpus)
    return "" if nextw=='\n' else nextw + " " + recursivemakeline(nextw,corpus)

def nextword(word,corpus):
    #return a random next word based on the corpus
    if word not in corpus.keys():
        return '\n'
    return random.choice(corpus[word])

def getSeed(corpus):
    return random.choice(corpus.keys())

def makepoem(n,corpus):
    poem = ""
    for i in xrange(0,n):
        poem += makeline(getSeed(corpus),corpus) + '\n'
    return poem

if __name__ == '__main__':
    makecorpus()
    #print shakespeare
    print makepoem(8,shakespeare)
