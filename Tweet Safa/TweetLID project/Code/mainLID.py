# -*- coding: utf-8 -*-
from __future__ import division
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils
import Smoothing as linear
import numpy as np

import sys

# 1-. Read dataset and create tweetList fullfilled of Tweet object*

dataset = "../Dataset/output_complete.txt"

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

linearCoefficients = list()

for language in arrayLanguages:
    unigrams = corpusNgrams.get('1').get(language)
    bigrams = corpusNgrams.get('2').get(language)
    trigrams = corpusNgrams.get('3').get(language)
    linearCoefficients.append(linear.getlinearcoefficients(language, unigrams, bigrams, trigrams))

max = 0;
tweetEN = "Tomorrow is going to be a good day to go to the beach"
tweetPT = "Amanhã será um dia muito bom, como ir para a praia."
tweetCA = "Demà farà un dia molt bo, com per anar a la platja."
tweetEU = "Bihar egun oso ona egingo du, hondartzara joateko modukoa."
tweetGL = "Mañá será un día moi bo, como ir á praia."
tweetES = "Mañana hará un dia muy bueno, como para ir a la playa."

text = preprocess.preprocessText(tweetES)

print text

for linearCoefficients in linearCoefficients:
    # print str(linearCoefficients[0])+" "+str(linearCoefficients[1])+" "+str(linearCoefficients[2]) + " " + str(linearCoefficients[3])+"\n"

    prob = 1.0;
    for i in range(0,len(text)-3):
        x = text[i]; y = text[i+1]; z = text[i+2]
        probability = linear.probability(corpusNgrams, linearCoefficients, x, y, z)
        # print probability
        prob = prob * probability

    if prob >= max:
        language = linearCoefficients[0]
        max = prob


    sys.stdout.write("Sequence probability in "+str(linearCoefficients[0])+": "+str(prob)+"\n")


sys.stdout.write("\n    Tweet:  "+str(text.encode("utf-8")))
sys.stdout.write("\n    Tweet language:   "+str(language)+"\n    Probability of:  "+str(max)+"\n")



prob = 1.0;
# for i in range(0,len(text)-3):
#     x = text[i]; y = text[i+1]; z = text[i+2]
#     probability = linear.probability(corpusNgrams, linearCoefficients, x, y, z)
#     prob = prob * probability
#
# sys.stdout.write("Sequence probability: "+str(prob)+"\n")


# 3.2-. Algorithms: Bayesian Networks

# 3.3-. Algorithms: Ranking Methods

# 3.4-. Out-of-place Measure
textHOLA = "més val que sigui bó"
label='ca'
testFreq = utils.getFreqDist(textHOLA,int(float(key)))

confidenceDict=dict((el,0) for el in corpusNgrams.keys())
m=80
n=50
confidenceDict,tot = learnNgramConfidences(confidenceDict,corpusNgrams,testFreq,m,n)
confidenceDict,tot = learnNgramConfidences(confidenceDict,corpusNgrams,testFreq,m,n)

confidenceProbabilityDict=dict((el,confidenceDict[el]/tot) for el in corpusNgrams.keys())