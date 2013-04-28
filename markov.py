import random, shelve
#parsed corpus in the form of a dictionary
#with keys being the seed words
#and data being the words that have come after that word


def makecorpus(filename):
    name  = {}
    poems = open(filename).readlines()
    poems = [ [word.lower().replace('(','').replace(')','').replace('\r','').replace("--","").replace('"',"").replace('_',"")
                 for word in line.replace('\n',' \n').split(' ')
                 if word!='' and word!='\n']
                 for line in poems if line.strip()!="" ]

    for line in poems:
        for i in xrange(0,len(line)-1):
            if line[i] in name.keys():
                name[line[i]].append(line[i+1])
            else:
                name[line[i]] = [line[i+1]]
    return name


def makeline(startword,corpus):
    word = startword.lower()
    startword = startword[0:1].upper()+startword[1:].lower()
    return startword + " " + recursivemakeline(word,corpus,10)

def recursivemakeline(word,corpus,depth):
    nextw = nextword(word,corpus)
    return "" if (nextw=='\n' or depth == 0) else nextw + " " + recursivemakeline(nextw,corpus,depth-1)

def nextword(word,corpus):
    #return a random next word based on the corpus
    if word not in corpus.keys():
        return '\n'
    return random.choice(corpus[word])

def getSeed(corpus):
    return random.choice(corpus.keys())

def makepoem(n,corpus):
    poems = shelve.open("poems")
    c = poems[corpus]
    poem = []
    for i in xrange(0,n):
        poem.append(makeline(getSeed(c),c))
    return poem

def makeShelve(name,filename):
    poems = shelve.open("poems")
    if name in poems.keys():
        del poems[name]
    poems[name] = makecorpus(filename)
    print poems



if __name__ == '__main__':
    #shakespeare = makecorpus("sonnets.txt")
    #print shakespeare

    #makeShelve("shakespeare","sonnets.txt")
    #makeShelve("whitman","whitman.txt")
    #makeShelve("poe","poe.txt")
    #makeShelve("dickinson","dickinson.txt")
    
    poems = shelve.open("poems")

    #print makepoem(8,'poe')
