from __future__ import division
import nltk as nk
__author__ = 'danielhorowitz'
import math
import UtilsTweetSafa as utils
def nestedCrossValidation(tweetList, k, c,models):
    m,n=80,50
    for i in xrange(k-1):
        trainAndValidationSet,testSet = divideDataset(tweetList,k,i)
        for j in xrange(c-1):
            trainSet,validationSet = divideDataset(trainAndValidationSet,c,j)
            trainDist = utils.obtainNgrams(trainSet,6)
            validationSetFreq=utils.obtainNgrams(validationSet,6)
            confidenceDict=utils.learnNgramConfidencefromData(trainDist,validationSet)
            predicted,true=utils.evaluateNgramRakingSet(validationSet,trainDist, confidenceDict,m,n)
            print(nk.ConfusionMatrix(predicted,true))


def divideDataset(dataset,k,index):
    testSet = dataset[int(math.ceil(len(dataset)*index/k)):int(math.ceil(len(dataset)*(index+1)/k))]
    trainSet = dataset[0:int(math.ceil(len(dataset)*index/k))] + dataset[int(math.ceil(len(dataset)*(index+1)/k)):len(dataset)]
    return (trainSet,testSet)

