from __future__ import division

import LidstonLanguageClassification as llc
import RankingModelClassification as rmc

import re
import nltk
import time
import goslate


from collections import Counter




#_____________________________________________________
#
#
#                   Utils class
#
#
#
#_____________________________________________________

langArray = ['en','es','fr','pt']

##
#   CreateDataSet method
#
#       Input: engFilePath = English dataset path.
#              esFilePath = Spanish dataset path.
#              frFilePath = French dataset path.
#              ptFilePath = Portuguese dataset path.
#
#       Output: dataSet

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


def formatDataset(allTexts):
    dataSet = list()

    for textList in allTexts:
        text_string=''
        for sentence in textList:
            text_string+=str(sentence[0])
        dataSet.append(text_string)
    return dataSet


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

def crossValidationLidstone(dataSet):

    error = 0.0
    iter = 0
    step = 5

    while iter < len(dataSet):
        trainSet = dataSet

        testSet = trainSet.pop(iter)

        allTexts = getAllLanguagesSet(dataSet)

        allTexts = formatDataset(allTexts)

        t0 = time.time()

        preditectedLang = llc.lidstoneLanguageClassification(testSet[0], allTexts)

        print time.time()-t0


        if testSet[1] == 'en':
            language = 0
        elif(testSet[1] == 'es'):
            language = 1
        elif(testSet[1] == 'fr'):
            language = 2
        elif(testSet[1] == 'pt'):
            language = 3

        iter += step
        if preditectedLang == language:
            error += 0
        else:
            error += 1
        print 'error'+str(error)
    iter = (iter - step)/step+1
    error = error/iter
    print error
    return error

def crossValidationRanking(m,n,dataSet):
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
            allFreq = returnNgramFreqSetRanking(allTexts,nGramSize)
            probList = rmc.outofplaceMeasureSet(m,n,allFreq,testSet[0],nGramSize)
            predictedLabel.append(probList.index(max(probList)))
        k=[]
        k = [k for k,v in Counter(predictedLabel).items() if v>1]

        if not k:
           predictedLabelTotal = predictedLabel[1]
        else:
            predictedLabelTotal = k[0]

        #print 'tweet: ' + str(testSet[0])
        print 'predicted: ' + langArray[predictedLabelTotal] + "\ttarget: " + testSet[1]

        iter += 5
        if langArray[predictedLabelTotal] == testSet[1]: error += 0
        else: error += 1

    iter = (iter - 5)/5
    error = error / iter
    return error



# Gets string, removes URLs and returns the string
def cleanDataset(dataSet):
    for dsItem in dataSet:
        dsItem[0] = cleanTweets(dsItem[0])
    return dataSet


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


# Gets text returns ngrams
def getBigramFreqForSingleLang(text,n):
    bigramsObject = nltk.ngrams(text,n)
    freqDist = nltk.FreqDist(bigramsObject)
    return freqDist

#Get set of texts and returns their respective set of frequencies
def returnNgramFreqSetRanking(allTexts,n):
    allFreq = []
    text_string=''
    for textList in allTexts:
        for sentence in textList:
            text_string+=str(sentence[0])
        allFreq.append(getBigramFreqForSingleLang(text_string,n))
        text_string=''
    return allFreq




#Get set of texts and returns their respective set of frequencies
def returnNgramFreqSet(allTexts, n):
    allFreq=[]
    for text in allTexts:
        allFreq.append(returnNgramList(text, n))
    return allFreq

# Gets text returns n-grams
def returnNgramList(text, n):
    grams = nltk.ngrams(text, n)
    freqDist=nltk.FreqDist(grams)
    return freqDist