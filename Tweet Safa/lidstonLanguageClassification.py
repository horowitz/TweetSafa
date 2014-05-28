import re
import nltk
import sys
import time


# ________________________________________________________
#
#                   Definitions
#
#
# ________________________________________________________


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

def plidstone (trig, cbr, ctr, ntr,l, n) :
    if n == 1:
        px = lidstone(trig[0], cbr, 1600, ntr, l)
        pxy = lidstone(trig, ctr, 64000, ntr, l) #64000 = 40**3 number of posible trigrams with 40 symbols.
        return pxy / px
    else:
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




# _____________________________________________________
#
#                       MAIN
#
# _____________________________________________________


## ----------------------------------
## Global variables
ptr = {}    # Trigram probabilities P(z|xy)
ctr = {}    # Trigram absolute counts (xyz)
cbr = {}    # Bigram absolute counts (xy)
cur = {}    # Unigram absolute counts (x)
ntr = 0     # total observations
nbr = 0     # total observations


def lidstoneLanguageClassification(sentence):

    nbr = 0
    ntr = 0

    t0 = time.clock();

    # Read tweets files

    #English

    file = open("eng_tweets.txt", "r")
    en_text= file.read()
    en_text = en_text.lower()

    #Spanish

    file = open("es_tweets.txt", "r")
    es_text= file.read()
    es_text = es_text.lower()

    #French

    file = open("fr_tweets.txt", "r")
    fr_text= file.read()
    fr_text = fr_text.lower()

    #Portuguese

    file = open("pt_tweets.txt", "r")
    pt_text= file.read()
    pt_text = pt_text.lower()

    # Concatenate in a vector
    allTexts = [en_text, es_text,fr_text,pt_text]

    #Training
    allTexts=cleanTraining(allTexts)
    # printBigramObjects(freqDistSet)

    freqDistSetUni = returnNgramFreqSet(allTexts, 1)
    freqDistSetBi = returnNgramFreqSet(allTexts, 2)
    freqDistSetTri = returnNgramFreqSet(allTexts, 3)



    # Different sentences: Real application read tweet.

    #sentence = 'Once upon a time there was a cat who wore boots'
    #sentence = 'this is a foo bar sentences and i want to ngramize it'
    #sentence = 'O portugues foi usado, naquela epoca,'
    # sentence = "una frase en espanol, es una mierda de programa"
    #sentence = 'La France metropolitaine possede une grande variete de paysages, entre des plaines agricoles ou boisees, des chaines de montagnes plus ou moins erodees, des littoraux diversifies et des vallees melant villes et espaces neo-naturels.'


    # Language
    #   0 = English
    #   1 = Spanish
    #   2 = French
    #   3 = Portuguese

    results = []
    filas = 4
    columnas = 2

    for i in range(filas):
        results.append([0]*columnas)

    for language in range(0, 4):

        # Count Unigrams (CUR), bigrams (CBR) and total observations (NBR)


        for i in xrange(0,len(freqDistSetUni[language].items())):
            cur[freqDistSetUni[language].items()[i][0][0]] = freqDistSetUni[language].items()[i][1]
        for j in xrange(0,len(freqDistSetBi[language].items())):
            cbr[freqDistSetBi[language].items()[j][0][0]+freqDistSetBi[language].items()[j][0][1]] = freqDistSetBi[language].items()[j][1]
            nbr = nbr + freqDistSetBi[language].items()[j][1];


        ## Compute input probability Bigram

        prob = 1.0;
        for i in range(0,len(sentence)-1):
            x = sentence[i]; y=sentence[i+1];
            pt = plidstone(x+y,cur, cbr,nbr,0.1, 1)
            prob = prob * pt
            #sys.stdout.write((x+y).encode("utf-8")+" "+str(pt)+" "+str(prob)+"\n")

        #sys.stdout.write(str(language)+"language Sequence probability: "+str(prob)+"\n")

        results[language][0] = float(prob)

        # Count Bigrams (CBR), trigrams (CTR) and the total observations (NTR)

        for i in xrange(0, len(freqDistSetBi[language].items())):
            cbr[freqDistSetBi[language].items()[i][0][0] + freqDistSetBi[language].items()[i][0][1]] = freqDistSetBi[language].items()[i][1]
        for j in xrange(0, len(freqDistSetTri[language].items())):
            ctr[freqDistSetTri[language].items()[j][0][0] + freqDistSetTri[language].items()[j][0][1] + freqDistSetTri[language].items()[j][0][2]] = freqDistSetTri[language].items()[j][1]
            ntr = ntr + freqDistSetTri[language].items()[j][1]

        ## Compute input probability Trigram

        prob = 1.0;
        for i in range(0,len(sentence)-2):
            x=sentence[i]; y=sentence[i+1]; z=sentence[i+2]
            pt = plidstone(x+y+z,cbr, ctr,ntr, 0.1, 0)
            prob = prob * pt
            #sys.stdout.write((x+y+z).encode("utf-8")+" "+str(pt)+" "+str(prob)+"\n")

        #sys.stdout.write(str(language)+"language Sequence probability: "+str(prob)+"\n")

        results[language][1] = float(prob)

    max = results[0][0]
    maxi = 0
    maxj = 0
    for i in range(0, filas):
        for j in range(0, columnas):
            if(results[i][j] > max):
                max = results[i][j]
                maxi = i
                maxj = j
            if j == 0:
                sys.stdout.write(str(i)+"language Sequence probability bigrams: "+str(results[i][j])+"\n")
            else:
                sys.stdout.write(str(i)+"language Sequence probability trigrams: "+str(results[i][j])+"\n")

    print results[maxi][maxj]

    print maxi
    print time.clock()

    return maxi