
#parsed corpus in the form of a dictionary
#with keys being the seed words
#and data being the words that have come after that word

shakespeare = {}

def makecorpus():
    sonnets = open("sonnets.txt").readlines()
    sonnets = [ [word.lower().replace('(','').replace(')','')
                 for word in line.replace('\n',' \n').split(' ') if word!='']
                 for line in sonnets if line!='\n' ]

    for line in sonnets:
        for i in xrange(0,len(line)-1):
            if line[i] in shakespeare.keys():
                shakespeare[line[i]].append(line[i+1])
            else:
                shakespeare[line[i]] = [line[i+1]]

def makeline(startword):
    word = startword
    nextw = ""
    startword = startword[0:1].upper()+startword[1:]
    nextw = nextword(word)
    return startword + nextw + recursivemakeline(nextw)

def recursivemakeline(word):
    nextw = nextword(word)
    return word if nextw=='\n' else word + nextword(word)

def nextword(word):
    #return a random next word based on the corpus
    pass

if __name__ == '__main__':
    makecorpus()
    print shakespeare
    print makeline('thou')
