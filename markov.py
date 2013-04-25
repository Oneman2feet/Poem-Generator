#parsed corpus in the form of a dictionary
#with keys being the seed words
#and data being the words that have come after that word

shakespeare = { }

def parsecorpus():
    pass

def makeline(word):
    nextword = nextword(word)
    return word if nextword=='\n' else word + nextword(word)

def nextword(word):
    #return a random next word based on the corpus
    pass

if __name__ == '__main__':
    parsecorpus(shakespearesonnets)
    print makeline('thou')
