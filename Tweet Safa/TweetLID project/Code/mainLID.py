# -*- coding: utf-8 -*-
from __future__ import division
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils
import Smoothing as linear
import numpy as np

import sys

# 1-. Read dataset and create tweetList fullfilled of Tweet object
dataset = "../Dataset/output.txt"

tweetList = read.read_tweets_dataset(dataset)

# 2-. Pre-process state

tweetListPreProcessed = preprocess.main(tweetList)

    # Raw data -> tweetList
    # Clean data -> tweetListPreProcessed

#utils.printTweets(tweetListPreProcessed)

# 3-. Algorithms
#
# 3.1-. OBTAIN N-GRAMS

corpusNgrams, arrayLanguages = utils.obtainNgrams(tweetListPreProcessed)


#print(corpusNgrams.get(str(4)).get('es'))

# Example:  print(corpusNgrams.get(str(3)).get('pt'))

# Clean data -> Algorithm

# 3.2-. Linear interpolation
#   Generate linear coefficients: input (n-grams and language)
#   Smooth data

# print corpusNgrams.get('3').get('en')

linearCoefficients = linear.getlinearcoefficients(corpusNgrams)

print str(linearCoefficients[0])+" "+str(linearCoefficients[1])+" "+str(linearCoefficients[2])+"\n"

text = "més val que sigui bó"
label='ca'
prob = 1.0;
# for i in range(0,len(text)-3):
#     x = text[i]; y = text[i+1]; z = text[i+2]
#     probability = linear.probability(corpusNgrams, linearCoefficients, x, y, z)
#     prob = prob * probability
#
# sys.stdout.write("Sequence probability: "+str(prob)+"\n")

# 3.2-. Algorithms: Bayesian Networks

# 3.3-. Algorithms: Ranking Methods

# 3.4-.. Out-of-place Measure


def outofplaceMeasure(FDLenght, TTLenght, freqDist,freqDistTest):
    outofplaceResult = list()

    FDLenght=min(len(freqDist),FDLenght)
    TTLenght=min(len(freqDistTest),TTLenght)
    # Get m x n items
    topFDItems = freqDist.items()[:FDLenght]
    topTTItems = freqDistTest.items()[:TTLenght]

    totalDistance = 0
    for i in xrange(0,TTLenght):
        # print(testText + "\t" + str(TTLenght) + "\t" +str(len(topTTItems)))
        lp = topTTItems[i]
        distance = FDLenght
        for j in xrange(0,FDLenght):
            tp = topFDItems[j]
            if lp[0] == tp[0] or j == FDLenght-1:
                distance = abs(i-j)
                totalDistance += distance
                break
    return totalDistance/(FDLenght*TTLenght)

acc=0
tot=0
ngramPredictedLanguage=list()
for key in corpusNgrams.keys():
    predictedLanguage=list()
    languagesList=list()
    print('N: '+ key)
    languagesList=corpusNgrams.get(key).keys()
    for subkey in corpusNgrams.get(key).keys():
        languagesList.append(subkey)
        # print ('Length' + str(len(corpusNgrams.get(key).get(subkey)) ))
        if key == '1':
            print(subkey)
        predictedLanguage.append(outofplaceMeasure(80,50,corpusNgrams.get(key).get(subkey),utils.getFreqDist(text,int(float(key)))))
    predicted=languagesList[predictedLanguage.index(min(predictedLanguage))]
    if label == predicted:
        acc=acc+1
    tot=tot+1
    print('True: '+label+' Predicted: '+predicted)
print(str(acc/tot))