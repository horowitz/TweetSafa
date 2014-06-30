# -*- coding: utf-8 -*-
from __future__ import division
from random import shuffle
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils
import Smoothing as linear
import numpy as np
import CrossValidation as cv

import sys

maxNgram = 3

# 1-. Read dataset and create tweetList fullfilled of Tweet object*

dataset = "../Dataset/output_complete.txt"

tweetList = read.read_tweets_dataset(dataset)
# 2-. Pre-process state

tweetListPreProcessed = preprocess.main(tweetList)
shuffle(tweetListPreProcessed)
    # Raw data -> tweetList
    # Clean data -> tweetListPreProcessed

#utils.printTweets(tweetListPreProcessed)

# 3-. Algorithms
#
# 3.1-. OBTAIN N-GRAMS

# corpusNgrams, arrayLanguages, arrayLanguagesFull = utils.obtainNgrams(tweetListPreProcessed, maxNgram+1)
# arrayLanguagesFull = utils.orderVector(arrayLanguagesFull)

# Example:  print(corpusNgrams.get(str(3)).get('pt'))


# 3.2-. Algorithms: Bayesian Networks
#   3.2.1-. Linear interpolation
#       Generate linear coefficients: input (n-grams and language)
#       Smooth data

cv.crossValidationLinearInterpolation(tweetListPreProcessed, 3, maxNgram)


# linearCoefficients = linear.getlinearcoefficientsForLanguageArray(arrayLanguages, maxNgram, corpusNgrams)
# for tweet in tweetListPreProcessed:
#     predictedLanguage, probability = linear.getPredictedLanguageForTweet(linearCoefficients, tweet.text, maxNgram, corpusNgrams)

# 3.3-. Algorithms: Ranking Methods
# print(arrayLanguagesFull)
# cv.nestedCrossValidation(tweetListPreProcessed,5,5,[0,0,0],arrayLanguagesFull)
# cv.crossValidation(tweetListPreProcessed, 3, [0,0,0], arrayLanguagesFull, maxNgram+1)
# 3.4-. Out-of-place Measure



# EVALUATION:

# PARA USAR EL tweetLID_eval.pl TENEMOS QUE CREAR UN FICHERO EN EL QUE LOS TWEETS ESTEN DE LA SIGUIENTE MANERA:

#   tweet_id<TAB>language
#
#   HE PUESTO UN EJEMPLO COGIENDO TWEETS DE OUTPUT_COMPLETE LOS HE GUARDADO EN EL FICHERO result.txt
#
#   Para probar el codigo ejecutar la siguiente linea:
#
#    perl tweetLID_eval.pl -d ../Dataset/result.txt -r ../Dataset/output_complete.txt ->../Dataset/evaluation_ouput.txt
#
#   LO QUE HACE ESTA LINEA ES MIRAR EL RESULT.TXT CREADO POR NOSOTROS, COMPARARLO CON EL OUTPUT_COMPLETE.TXT Y GUARDAR LOS
#       RESULTADOS EN EL EVALUATION_OUTPUT.TXT
#
#   AHI ESTA TODA LA INFORMACION DE LA PRECISION RECAL ETC... EXPLICADA.