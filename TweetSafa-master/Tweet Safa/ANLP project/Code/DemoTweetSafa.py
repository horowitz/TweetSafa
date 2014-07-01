from __future__ import division

import UtilsTweetSafa as utils
import LidstonLanguageClassification as llc
import sys
import RankingModelClassification as rmc
from collections import Counter


# sentence = 'Once upon a time there was a cat who wore boots'
#sentence = 'It is known for being the first to print many English manuscripts, including Cotton Nero A.x, which contains Pearl, Sir Gawain and the Green Knight, and other poems.'
# sentence = 'O portugues foi usado, naquela epoca,'
# sentence = "una frase en espanol, es una prueba de que el programa funcione"
# sentence = 'La France metropolitaine possede une grande variete de paysages, entre des plaines agricoles ou boisees, des chaines de montagnes plus ou moins erodees, des littoraux diversifies et des vallees melant villes et espaces neo-naturels.'
# sentence = 'today i will go home with my brother and sister because i like it, the mountain is a thing in english'

dataSet = utils.createDataSet("datasets/en_tweets.txt","datasets/es_tweets.txt","datasets/fr_tweets.txt","datasets/pt_tweets.txt")


allTexts = utils.getAllLanguagesSet(dataSet)
allTexts = utils.formatDataset(allTexts)

sentence = sys.argv[1]
sentence = utils.cleanTweets(sentence)

language = llc.lidstoneLanguageClassification(sentence, allTexts)

predictedLabel = list()
m = 80
n = 100

for nGramSize in xrange(2,5):
    # allTexts = utils.getAllLanguagesSet(allTexts)
    allFreq = utils.returnNgramFreqSetRanking(allTexts,nGramSize)
    probList = rmc.outofplaceMeasureSet(m,n,allFreq,sentence,nGramSize)
    predictedLabel.append(probList.index(max(probList)))

k=[]
k = [k for k,v in Counter(predictedLabel).items() if v>1]

if not k:
    predictedLabelTotal = predictedLabel[1]
else:
    predictedLabelTotal = k[0]

#print 'tweet: ' + str(testSet[0])
# print 'predicted: ' + langArray[predictedLabelTotal] + "\ttarget: " + testSet[1]


# print language

print 'Language predicted with Lidstone smoothing = '+str(language)

print 'Language predicted with ranking = '+str(predictedLabelTotal)