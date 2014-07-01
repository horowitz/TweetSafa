# -*- coding: utf-8 -*-
from __future__ import division
import ReadData as read
import PreprocessTweets as preprocess
import CrossValidation as cv
import UtilsTweetSafa as utils
import Smoothing_old as linear
import CrossValidation as cv
import numpy as np

import sys
maxNgram = 3
# 1-. Read dataset and create tweetList fullfilled of Tweet object*

dataset = "../Dataset/output.txt"

tweetList = read.read_tweets_dataset(dataset)

# 2-. Pre-process state

tweetListPreProcessed = preprocess.main(tweetList)
corpusNgrams, arrayLanguages, arrayLanguagesFull=utils.obtainNgrams(tweetListPreProcessed, maxNgram+1)
arrayLanguagesFull = utils.orderVector(arrayLanguagesFull)
    # Raw data -> tweetList
    # Clean data -> tweetListPreProcessed

#utils.printTweets(tweetListPreProcessed)

# 3-. Algorithms
#
# 3.1-. OBTAIN N-GRAMS
#
# corpusNgrams, arrayLanguages = utils.obtainNgrams(tweetListPreProcessed)
#

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
print linearCoefficients
max = 0;
tweetEN = "Tomorrow is going to be a good day to go to the beach"
tweetPT = "Amanhã será um dia muito bom, como ir para a praia."
tweetCA = "Demà farà un dia molt bo, com per anar a la platja."
tweetEU = "Bihar egun oso ona egingo du, hondartzara joateko modukoa."
tweetGL = "Mañá será un día moi bo, como ir á praia."
tweetES = "Mañana hará un dia muy bueno, como para ir a la playa."

tweet = "hola caracola"
text = preprocess.preprocessText(tweetEN)

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
#
#
#
# prob = 1.0;
# for i in range(0,len(text)-3):
#     x = text[i]; y = text[i+1]; z = text[i+2]
#     probability = linear.probability(corpusNgrams, linearCoefficients, x, y, z)
#     prob = prob * probability
#
# sys.stdout.write("Sequence probability: "+str(prob)+"\n")


# 3.2-. Algorithms: Bayesian Networks

# 3.3-. Algorithms: Ranking Methods
# print(arrayLanguagesFull)
# cv.nestedCrossValidation(tweetListPreProcessed,5,5,[0,0,0],arrayLanguagesFull)
 # 3.4-. Out-of-place Measure