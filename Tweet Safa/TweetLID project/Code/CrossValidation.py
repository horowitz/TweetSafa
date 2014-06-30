from __future__ import division
import nltk as nk
import math
import Smoothing as linear
import UtilsTweetSafa as utils

# def nestedCrossValidation(tweetList, k, c,models,arrayLanguagesFull):
#     m=80
#     n=50
#     for i in xrange(k-1):
#         trainAndValidationSet,testSet = divideDataset(tweetList,k,i)
#         for j in xrange(c-1):
#             trainSet,validationSet = divideDataset(trainAndValidationSet,c,j)
#             trainDist = utils.obtainNgrams(trainSet,6)
#             confidenceDict=utils.learnNgramConfidencefromData(trainDist,validationSet)
#             predicted,true=utils.evaluateNgramRakingSet(validationSet,trainDist, confidenceDict,m,n)
#             print(predicted+true)
#
#             # DANI PON AQUI EL SCRIPT. EL PREDICTED ES UN VECTOR QUE TIENE LAS PREDICTED LABELS I EL TRUE TIENE LOS VERDADEROS

def crossValidation(tweetList, k,models,arrayLanguagesFull,maxNgram):
    m=80
    n=50
    for i in xrange(k):

        trainSet,testSet = divideDataset(tweetList,k,i)
        trainDist = utils.obtainNgrams(trainSet,maxNgram)
        confidenceDict=utils.learnNgramConfidencefromData(trainDist,trainSet)
        predicted,true=utils.evaluateNgramRakingSet(testSet,trainDist, confidenceDict,m,n)
        print(predicted+true)
            # DANI PON AQUI EL SCRIPT. EL PREDICTED ES UN VECTOR QUE TIENE LAS PREDICTED LABELS I EL TRUE TIENE LOS VERDADEROS
        utils.printResults(testSet, predicted, i)


def divideDataset(dataset, k, index):
    testSet = dataset[int(math.ceil(len(dataset)*index/k)):int(math.ceil(len(dataset)*(index+1)/k))]
    trainSet = dataset[0:int(math.ceil(len(dataset)*index/k))] + dataset[int(math.ceil(len(dataset)*(index+1)/k)):len(dataset)]
    return (trainSet,testSet)

# def accuracy(true,predicted,order):
#     matrix=0
#     for i in xrange(0,len(predicted)):
#         if(not '+' in predicted[i] and not '/' in predicted[i]):
#             print (predicted[i])
#         else:
#             if('+' in predicted[i]):
#
#             else:
#     return matrix

def crossValidationLinearInterpolation(tweetList, k, maxNgram):
    for i in xrange(k):
        trainSet, testSet = divideDataset(tweetList, k, i)
        trainDist, arrayLanguages, languagesAll = utils.obtainNgrams(trainSet, maxNgram)
        linearCoefficients = linear.getlinearcoefficientsForLanguageArray(arrayLanguages, maxNgram, trainDist)
        print linearCoefficients
        count = 0
        tot = 0
        for tweet in testSet:
            predictedLanguage, probability = linear.getPredictedLanguageForTweet(linearCoefficients, tweet.text, maxNgram, trainDist)
            utils.printResultTXT(predictedLanguage, tweet)
            # print(predictedLanguage + tweet.language)
            if(predictedLanguage==tweet.language):
                count = count + 1;
                print count
            tot = tot +1
        print 'correct tweets fold '+str(i)+' = '+str(count)+'/'+str(tot)
