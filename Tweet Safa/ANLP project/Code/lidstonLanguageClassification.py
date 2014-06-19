from __future__ import division

import sys
import UtilsTweetSafa as utils

# ________________________________________________________
#
#                   Definitions
#
#
# ________________________________________________________


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

#_______________________________________________
#
# Input:
#         Sentence = test set
#         allTexts = training sets.
#            (format) allTexts = [en_text, es_text,fr_text,pt_text]
#
# Output:
#         Language
# __________________________________________________________________
def lidstoneLanguageClassification(sentence,allTexts):

    nbr = 0
    ntr = 0
    freqDistSetUni = utils.returnNgramFreqSet(allTexts, 1)
    freqDistSetBi = utils.returnNgramFreqSet(allTexts, 2)
    freqDistSetTri = utils.returnNgramFreqSet(allTexts, 3)


    # Language
    #   0 = English
    #   1 = Spanish
    #   2 = French
    #   3 = Portuguese

    results = []
    filas = 4
    columnas = 2
    lamda = 0.1

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
            pt = plidstone(x+y,cur, cbr,nbr,lamda, 1)
            prob = prob * pt
            # sys.stdout.write((x+y).encode("utf-8")+" "+str(pt)+" "+str(prob)+"\n")
        # sys.stdout.write(str(language)+"language Sequence probability: "+str(prob)+"\n")

        results[language][0] = float(prob)

        # Count Bigrams (CBR), trigrams (CTR) and the total observations (NTR)

        for i in xrange(0, len(freqDistSetBi[language].items())):
            cbr[freqDistSetBi[language].items()[i][0][0] + freqDistSetBi[language].items()[i][0][1]] = freqDistSetBi[language].items()[i][1]
        for j in xrange(0, len(freqDistSetTri[language].items())):
            ctr[freqDistSetTri[language].items()[j][0][0] + freqDistSetTri[language].items()[j][0][1] + freqDistSetTri[language].items()[j][0][2]] = freqDistSetTri[language].items()[j][1]
            ntr = ntr + freqDistSetTri[language].items()[j][1]

        ## Compute input probability Trigram

        prob = 1.0
        for i in range(0,len(sentence)-2):
            x=sentence[i]; y=sentence[i+1]; z=sentence[i+2]
            pt = plidstone(x+y+z,cbr, ctr,ntr, lamda, 0)
            prob = prob * pt
            # sys.stdout.write((x+y+z).encode("utf-8")+" "+str(pt)+" "+str(prob)+"\n")
        #  sys.stdout.write(str(language)+"language Sequence probability: "+str(prob)+"\n")
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
    return maxi