from __future__ import  division
import re
import matplotlib
import nltk
from random import randrange
from sklearn.cross_validation import LeaveOneOut
import goslate
from collections import Counter
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

def cleanTraining(allTexts):
    for i in xrange(1, len(allTexts)):
        allTexts[i] = cleanTweets(allTexts[i])
    return allTexts


# Gets string, removes URLs and returns the string
def cleanDataset(dataSet):
    for dsItem in dataSet:
        dsItem[0] = cleanTweets(dsItem[0])

    return dataSet


def cleanTweets(text):
    # TODO remove numbers
    # remove urls
    p = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|[^A-Za-z0-9 ]')
    cleanText = re.sub(p, '', text)
    return cleanText.lower()

#Get set of texts and returns their respective set of frequencies
def returnNgramFreqSet(allTexts,n):
    allFreq = []
    text_string=''
    for textList in allTexts:
        for sentence in textList:
            text_string+=str(sentence[0])
        allFreq.append(getBigramFreqForSingleLang(text_string,n))
        text_string=''
    return allFreq

# Gets text returns ngrams
def getBigramFreqForSingleLang(text,n):
    bigramsObject = nltk.ngrams(text,n)
    freqDist = nltk.FreqDist(bigramsObject)
    return freqDist

# # Gets text returns bigrams
# def getBigramFreqForSingleLang(text):
#     bigramsObject = nltk.bigrams(text)
#     freqDist = nltk.FreqDist(bigramsObject)
#     return freqDist


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


def outofplaceMeasureSet(m, n, freqDistSet, testText,ngramSize):
    probList = list()
    # Get test freq Dist
    freqDistTest = getBigramFreqForSingleLang(testText,ngramSize)


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

def createDataSet(engFilePath,esFilePath,frFilePath,ptFilePath):
    dataSet =  list()
    for line in open(engFilePath, 'r'):
        dataSet.append([line,'en'])
    for line in open(esFilePath, 'r'):
        dataSet.append([line,'es'])
    for line in open(frFilePath, 'r'):
        dataSet.append([line,'fr'])
    for line in open(ptFilePath, 'r'):
        dataSet.append([line,'pt'])

    return dataSet

def crossValidation(m,n,dataSet):
    gs = goslate.Goslate()
    error = 0
    iter = 0
    predictedLabel = list()

    while iter < len(dataSet):
        trainSet = dataSet

        testSet = trainSet.pop(iter)

        predictedLabel = list()
        for nGramSize in xrange(2,5):
            allTexts = getAllLanguagesSet(trainSet)
            allFreq = returnNgramFreqSet(allTexts,nGramSize)
            probList = outofplaceMeasureSet(m,n,allFreq,testSet[0],nGramSize)
            predictedLabel.append(probList.index(max(probList)))
        k=[]
        k = [k for k,v in Counter(predictedLabel).items() if v>1]

        if not k:
           predictedLabelTotal = predictedLabel[1]
        else:
            predictedLabelTotal = k[0]

        # print 'tweet: ' + str(testSet[0])
        # print 'predicted: ' + langArray[predictedLabelTotal] + "\ttarget: " + testSet[1]

        iter += 5
        if langArray[predictedLabelTotal] == testSet[1]: error += 0
        else: error += 1

    iter = (iter - 5)/5
    error = error / iter
    return error

# file = open("eng_tweets.txt", "r")
# en_text = file.readline()
# en_text = en_text.lower()
#
# file = open("es_tweets.txt", "r")
# es_text = file.read()
# es_text = es_text.lower()
#
# file = open("fr_tweets.txt", "r")
# fr_text = file.read()
# fr_text = fr_text.lower()
#
# file = open("pt_tweets.txt", "r")
# pt_text = file.read()
# pt_text = pt_text.lower()

# allTexts = [en_text, es_text, fr_text, pt_text]

# tweet = allTexts.pop(randrange(len(allTexts)))
#
# #Training
# allTexts = cleanTraining(allTexts)
# freqDistSet = returnBigramFreqSet(allTexts)
# # printBigramObjects(freqDistSet)
# # Testing
# testText = cleanTweets(tweet.lower())
# freqDistEN = freqDistSet[0]
#
# items = freqDistEN.items()
#
# probList = outofplaceMeasureSet(100,5,freqDistSet,testText)
allTexts = createDataSet("eng_tweets.txt","es_tweets.txt","fr_tweets.txt","pt_tweets.txt")
cleanedDataSet = cleanDataset(allTexts)
error = crossValidation(100,50,cleanedDataSet)
print "Error: " + str(error)

