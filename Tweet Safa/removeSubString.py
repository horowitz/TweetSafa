import re
import matplotlib
import nltk
import sys
import codecs

from nltk.probability import LidstoneProbDist, WittenBellProbDist
from nltk.util import ngrams

## ----------------------------------
## Global variables
ptr={} # trigram probabilities P(z|xy)
ctr={} # trigram absolute counts (xyz)
cbr={} # bigram absolute counts (xy)
cur={} # unigram absolute counts (xy)
ntr=0   # total observations
# 0 = English
# 1 = Spanish
# 2 = French
# 3 = Portuguese
language = 1

#Clean set of texts
def cleanTraining(allTexts):
    for i in xrange(1,len(allTexts)):
        allTexts[i]=cleanTweets(allTexts[i])
    return allTexts

# Gets string, removes URLs and returns the string
def cleanTweets(text):
    # remove urls
    p = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|[^A-Za-z0-9 ]')
    cleanText = re.sub(p,'', text)
    return cleanText

#Get set of texts and returns their respective set of frequencies
def returnBigramFreqSet(allTexts):
    allFreq=[]
    for text in allTexts:
        allFreq.append(returnBigramList(text,20))
    return allFreq

# Gets text returns bigrams
def returnBigramList(text, numElements):
    bigramsObject = nltk.bigrams(text)
    freqDist=nltk.FreqDist(bigramsObject)
    return freqDist

#print a SET of freqDist objects
def printBigramObjects(freqDist):
    for elem in freqDist:
        printBigramObject(elem)
#print ONE freqDist object
def printBigramObject(freqDist):
    freqDist.plot( 10,cumulative=False)
    for k,v in freqDist.items():
        big=''
        for i in k:
            big=big+i
        print big,v


#Get set of texts and returns their respective set of frequencies
def returnNgramFreqSet(allTexts, n):
    allFreq=[]
    for text in allTexts:
        allFreq.append(returnNgramList(text, n, 20))
    return allFreq

# Gets text returns n-grams
def returnNgramList(text, grams, numElements):
    grams = nltk.ngrams(text, grams)
    freqDist=nltk.FreqDist(grams)
    return freqDist

## --------------------------
## Lidstone probabilities

def plidstone (trig, cbr, ctr, ntr,l) :
  pxy = lidstone(trig[0] + trig[1], cbr, 1600 , ntr, l)
  pxyz = lidstone(trig, ctr, 64000, ntr, l) #64000 = 40**3 number of posible trigrams with 40 symbols.
  return pxyz / pxy

## ---------------------------------
## Lidstone smoothing
def lidstone(ngram,counts,B,N,l) :
  if (ngram in counts) :
    c = counts[ngram]
  else :
    c = 0.0

  return (c+l)/(N+B*l)


file = open("eng_tweets.txt", "r")
en_text= file.read()
en_text = en_text.lower()

file = open("es_tweets.txt", "r")
es_text= file.read()
es_text = es_text.lower()

file = open("fr_tweets.txt", "r")
fr_text= file.read()
fr_text = fr_text.lower()

file = open("pt_tweets.txt", "r")
pt_text= file.read()
pt_text = pt_text.lower()

allTexts = [en_text, es_text,fr_text,pt_text]

#Training
allTexts=cleanTraining(allTexts)
# freqDistSet=returnBigramFreqSet(allTexts)
# printBigramObjects(freqDistSet)

freqDistSetBi=returnNgramFreqSet(allTexts, 2)
freqDistSetTri=returnNgramFreqSet(allTexts, 3)

print freqDistSetTri[language].items()


# sentence = 'this is a foo bar sentences and i want to ngramize it'
# sentence = 'O portugues foi usado, naquela epoca,'
sentence = 'una frase en espanol, es una mierda de programa'

sentence.encode('ascii', 'ignore')
n = 2
trigram = ngrams(sentence, n)
tri=list()
for grams in trigram:
  tri.append(grams[0] + grams[1] )#+grams[2])


for i in xrange(0,len(freqDistSetBi[language].items())):
    cbr[freqDistSetBi[language].items()[i][0]] = freqDistSetBi[language].items()[i][1]
for j in xrange(0,len(freqDistSetTri[language].items())):
    ctr[freqDistSetTri[language].items()[j][0]] = freqDistSetTri[language].items()[j][1]
    ntr = ntr + freqDistSetTri[language].items()[j][1];


## compute input probability
prob=1.0;
for i in range(0,len(sentence)-2):
   x=sentence[i]; y=sentence[i+1]; z=sentence[i+2]
   pt = plidstone(x+y+z,cbr, ctr,ntr,1)
   prob = prob * pt
   sys.stdout.write((x+y+z).encode("utf-8")+" "+str(pt)+" "+str(prob)+"\n")

sys.stdout.write(str(language)+"language Sequence probability: "+str(prob)+"\n")
