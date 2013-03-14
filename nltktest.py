import nltk


"""
ADJ	adjective	
ADV	adverb	        
CNJ	conjunction	
DET	determiner	
EX	existential	
FW	foreign word	
MOD	modal verb	
N	noun	        
NP	proper noun	
NUM	number	        
PRO	pronoun	        
P	preposition	
TO	the word to	
UH	interjection	
V	verb	        
VD	past tense	
VG	present participle	
VN	past participle	
WH	wh determiner	
"""



sentence = "Everyday each one of you will be E-mailed a name. That is the name of the person whom you are to seek out and try to mark with a marker or highlighter. Once you have successfully marked that person, he/she should tell you the name of his/her target, which now becomes your new target. The person whom you just marked is eliminated from the game. Remember that while you are on the lookout for your target, you yourself are also being searched for. Your objective is to remain unmarked and become the last man standing in which case you win!  If you see yourself or another person about to be marked, you may say the word Assassin, and you or that person will be immune for the duration of that class period, ONLY from the person who tried to mark you or another person at the time you said Assassin."

tokens = nltk.word_tokenize(sentence)

tagged = nltk.pos_tag(tokens)

print tagged

verbs = [x for x in tagged if x[1] == 'VB']
#print verbs

PRP = [x for x in tagged if x[1] == 'PRP']
print PRP
