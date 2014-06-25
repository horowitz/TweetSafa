from __future__ import division
__author__ = 'danielhorowitz'
import math
import numpy as np
import UtilsTweetSafa as utils
def nestedCrossValidation(tweetList, k, c,models):
    # dataset = np.array(tweetList)
    for i in xrange(k-1):
        trainAndValidationSet,testSet = divideDataset(tweetList,k,i)
        for j in xrange(c-1):
            trainSet,validationSet = divideDataset(trainAndValidationSet,c,j)
            trainDist = utils.obtainNgrams(trainSet,5)
            confidenceDict=dict((el,0) for el in trainDist[0].keys())
            for tweet in validationSet:
                confidenceDict , tot = utils.learnNgramConfidences(confidenceDict,trainDist[0],tweet,80,50)
                print (confidenceDict)
                pass

            pass
    pass


# def divideDataset(dataset,k,index):
#     mask = np.ones(len(dataset), dtype=bool)
#     indexes = range(int(math.ceil(len(dataset)*index/k)),int(math.ceil(len(dataset)*(index+1)/k)))
#     mask[indexes] = False
#     testSet = dataset[indexes]
#     trainSet = dataset[mask]
#     return (trainSet,testSet)

def divideDataset(dataset,k,index):

    testSet = dataset[int(math.ceil(len(dataset)*index/k)):int(math.ceil(len(dataset)*(index+1)/k))]
    trainSet = dataset[0:int(math.ceil(len(dataset)*index/k))] + dataset[int(math.ceil(len(dataset)*(index+1)/k)):len(dataset)]
    return (trainSet,testSet)
# # Divide the dataset into k chunks
# def chunks(l, k):
#     n = int(math.ceil(len(l)/k))
#     return [l[i:i + n] for i in range(0, len(l), n)]

