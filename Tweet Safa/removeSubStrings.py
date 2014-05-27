from __future__ import  division
import re
import matplotlib
import nltk

#Clean set of texts
def cleanTraining(allTexts):
    for i in xrange(1, len(allTexts)):
        allTexts[i] = cleanTweets(allTexts[i])
    return allTexts


# Gets string, removes URLs and returns the string
def cleanTweets(text):
    # TODO remove numbers
    # remove urls
    p = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|[^A-Za-z0-9 ]')
    cleanText = re.sub(p, '', text)
    return cleanText


#Get set of texts and returns their respective set of frequencies
def returnBigramFreqSet(allTexts):
    allFreq = []
    for text in allTexts:
        allFreq.append(returnBigramList(text))
    return allFreq


# Gets text returns bigrams
def returnBigramList(text):
    bigramsObject = nltk.bigrams(text)
    freqDist = nltk.FreqDist(bigramsObject)
    return freqDist


#print a SET of freqDist objects
def printBigramObjects(freqDist):
    for elem in freqDist:
        printBigramObject(elem)


#print ONE freqDist object
def printBigramObject(freqDist):
    freqDist.plot(10, cumulative=False)
    for k, v in freqDist.items():
        big = ''
        for i in k:
            big = big + i
        print big, v


def outofplaceMeasureSet(m, n, freqDistSet, testText):
    probList = list()

    for freqDist in freqDistSet:
       probList.append(outofplaceMeasure(m, n, freqDist, testText))
    listSum=sum(probList)
    if listSum == 0:
        listSum = 1
    for i in xrange(0,len(probList)):
        probList[i] = probList[i]/listSum
    return probList


def outofplaceMeasure(FDLenght, TTLenght, freqDist, testText):
    outofplaceResult = list()
    freqDistTest = returnBigramList(testText)
    topFDItems = freqDist.items()[:FDLenght]
    topTTItems = freqDistTest.items()[:TTLenght]
    totalDistance = 0
    for i  in xrange(0,TTLenght):
        lp = topTTItems[i]
        distance = 0
        for j  in xrange(0,FDLenght):
            tp = topFDItems[j]
            if lp[0] == tp[0]:
                distance = j
                totalDistance += distance
    return totalDistance



file = open("eng_tweets.txt", "r")
en_text = file.read()
en_text = en_text.lower()

file = open("es_tweets.txt", "r")
es_text = file.read()
es_text = es_text.lower()

file = open("fr_tweets.txt", "r")
fr_text = file.read()
fr_text = fr_text.lower()

file = open("pt_tweets.txt", "r")
pt_text = file.read()
pt_text = pt_text.lower()

allTexts = [en_text, es_text, fr_text, pt_text]

tweet = 'Apparently I\'m a Lib Dem.. and a lot more centre than I thought! EUvox - England http://t.co/FyVRpJJC4N via @EUVOX 2014'

#Training
allTexts = cleanTraining(allTexts)
freqDistSet = returnBigramFreqSet(allTexts)
# printBigramObjects(freqDistSet)
# Testing
testText = cleanTweets(tweet.lower())
freqDistEN = freqDistSet[0]

items = freqDistEN.items()

probList = outofplaceMeasureSet(100,5,freqDistSet,testText)

print(items)

