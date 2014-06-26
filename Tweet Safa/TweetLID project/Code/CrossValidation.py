from __future__ import division
import nltk as nk
__author__ = 'danielhorowitz'
import math
import UtilsTweetSafa as utils
def nestedCrossValidation(tweetList, k, c,models,arrayLanguagesFull):
    m=80
    n=50
    for i in xrange(k-1):
        trainAndValidationSet,testSet = divideDataset(tweetList,k,i)
        for j in xrange(c-1):
            trainSet,validationSet = divideDataset(trainAndValidationSet,c,j)
            trainDist = utils.obtainNgrams(trainSet,6)
            confidenceDict=utils.learnNgramConfidencefromData(trainDist,validationSet)
            predicted,true=utils.evaluateNgramRakingSet(validationSet,trainDist, confidenceDict,m,n)
            print(predicted+true)
            # DANI PON AQUI EL SCRIPT. EL PREDICTED ES UN VECTOR QUE TIENE LAS PREDICTED LABELS I EL TRUE TIENE LOS VERDADEROS

def divideDataset(dataset,k,index):
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