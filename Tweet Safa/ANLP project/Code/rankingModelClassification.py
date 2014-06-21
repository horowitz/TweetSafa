from __future__ import division

import nltk
from random import randrange
from sklearn.cross_validation import LeaveOneOut

import UtilsTweetSafa as utils

langArray = ['en','es','fr','pt']

#Clean set of texts
def getAllItemsByLanguage(dataSet,value):
    result = list()
    for item in dataSet:
        if item[1] == value:
            result.append(item)
    return result

def getAllLanguagesSet(dataSet):
    langSet=list()
    for lang in langArray:
        langSet.append(getAllItemsByLanguage(dataSet,lang))
    return langSet

def outofplaceMeasureSet(m, n, freqDistSet, testText,ngramSize):
    probList = list()
    # Get test freq Dist
    freqDistTest = utils.getBigramFreqForSingleLang(testText,ngramSize)
    for freqDist in freqDistSet:
        n = min(n,len(freqDistTest))
        m = min(m,len(freqDist))
        probList.append(outofplaceMeasure(m, n, freqDist,freqDistTest, testText,ngramSize))
    listSum=sum(probList)
    if listSum == 0:
        listSum = 1
    for i in xrange(0,len(probList)):
        probList[i] = probList[i]/listSum
    return probList

def outofplaceMeasure(FDLenght, TTLenght, freqDist,freqDistTest, testText,n):
    outofplaceResult = list()


    # Get m x n items
    topFDItems = freqDist.items()[:FDLenght]
    topTTItems = freqDistTest.items()[:TTLenght]

    totalDistance = 0
    for i  in xrange(0,TTLenght):
        # print(testText + "\t" + str(TTLenght) + "\t" +str(len(topTTItems)))
        lp = topTTItems[i]
        distance = FDLenght
        for j  in xrange(0,FDLenght):
            tp = topFDItems[j]
            if lp[0] == tp[0]:
                distance = abs(i-j)
                totalDistance += distance
                break
    return totalDistance

