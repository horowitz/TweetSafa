from __future__ import division
__author__ = 'danielhorowitz'
import math
import numpy as np
def nestedCrossValidation(tweetList, k, c,models):
    dataset = np.array(tweetList)
    for i in xrange(k-1):
        trainAndValidationSet,testSet = divideDataset(dataset,k,i)
        for j in xrange(c-1):
            trainSet,validationSet = divideDataset(trainAndValidationSet,c,j)
            for m in xrange(models):
                pass
            pass
    pass


def divideDataset(dataset,k,index):
    mask = np.ones(len(dataset), dtype=bool)
    indexes = range(int(math.ceil(len(dataset)*index/k)),int(math.ceil(len(dataset)*(index+1)/k)))
    mask[indexes] = False
    testSet = dataset[indexes]
    trainSet = dataset[mask]
    return (trainSet,testSet)

# # Divide the dataset into k chunks
# def chunks(l, k):
#     n = int(math.ceil(len(l)/k))
#     return [l[i:i + n] for i in range(0, len(l), n)]

