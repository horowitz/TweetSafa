__author__ = 'Iosu'

import matplotlib.pyplot as plt
import numpy as np
import nltk



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


#English

file = open("datasets\eng_tweets.txt", "r")
en_text= file.read()
en_text = en_text.lower()

#Spanish

file = open("datasets\es_tweets.txt", "r")
es_text= file.read()
es_text = es_text.lower()

#French

file = open("datasets\fr_tweets.txt", "r")
fr_text= file.read()
fr_text = fr_text.lower()

#Portuguese

file = open("datasets\pt_tweets.txt", "r")
pt_text= file.read()
pt_text = pt_text.lower()

# Concatenate in a vector
allTexts = [en_text, es_text,fr_text,pt_text]

#Training
# allTexts=cleanTraining(allTexts)
# printBigramObjects(freqDistSet)

freqDistSetUni = returnNgramFreqSet(allTexts, 1)
freqDistSetBi = returnNgramFreqSet(allTexts, 2)
freqDistSetTri = returnNgramFreqSet(allTexts, 3)

ctr = {}    # Trigram absolute counts (xyz)
cbr = {}    # Bigram absolute counts (xy)
cur = {}    # Unigram absolute counts (x)
ntr = 0     # total observations
nbr = 0     # total observations

# language  = 0
#
# for i in xrange(0, len(freqDistSetBi[language].items())):
#     cbr[freqDistSetBi[language].items()[i][0][0] + freqDistSetBi[language].items()[i][0][1]] = freqDistSetBi[language].items()[i][1]
#     for j in xrange(0, len(freqDistSetTri[language].items())):
#         ctr[freqDistSetTri[language].items()[j][0][0] + freqDistSetTri[language].items()[j][0][1] + freqDistSetTri[language].items()[j][0][2]] = freqDistSetTri[language].items()[j][1]
#         ntr = ntr + freqDistSetTri[language].items()[j][1]

alphab = list()
frequencies = list()

language  = 0
n = 3

if n == 2:
    for a in freqDistSetTri[language].items()[0:9]:
        if(a[0][0] == ' '):
            alphab.append('#'+a[0][1])
        elif(a[0][1] == ' '):
            alphab.append(a[0][0]+'#')
        else:
            alphab.append(a[0][0]+a[0][1])

    for a in freqDistSetTri[language].items()[0:9]:
        frequencies.append(a[1])
elif n == 3:
    for a in freqDistSetTri[language].items()[0:9]:
        if(a[0][0] == ' '):
            alphab.append('#'+a[0][1]+a[0][2])
        elif(a[0][2] == ' '):
            alphab.append(a[0][0]+a[0][1]+'#')
        elif(a[0][1] == ' '):
            alphab.append(a[0][0]+'#'+a[0][2])
        else:
            alphab.append(a[0][0]+a[0][1]+a[0][2])

    for a in freqDistSetTri[language].items()[0:9]:
        frequencies.append(a[1])

pos = np.arange(len(alphab))
width = 1.0     # gives histogram aspect to the bar diagram

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(alphab)

plt.bar(pos, frequencies, width, color='r')
plt.show()






# import nltk
#
# f = open('eng_tweets.txt')
# raw = f.read()
# en_text = raw.lower()
#
# print en_text
# #Create your bigrams
# ugs = nltk.ngrams(en_text,1)
# bgs = nltk.ngrams(en_text,2)
# tgs = nltk.ngrams(en_text,3)
# fgs = nltk.ngrams(en_text,4)
#
# #compute frequency distribution for all the bigrams in the text
# fdist = nltk.FreqDist(bgs)
#
#
# for k,v in fdist.items():
#     ngrams = ''
#     for i in k:
#         ngrams= ngrams + i
#     print ngrams + '\t' + str(v)