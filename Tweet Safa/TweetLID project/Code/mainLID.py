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
#   Raw data -> tweetList
#   Clean data -> tweetListPreProcessed

tweetListPreProcessed = preprocess.main(tweetList)
shuffle(tweetListPreProcessed)

# 3-. Algorithms

# 3.1-. Algorithms: Bayesian Networks
#   3.2.1-. Linear interpolation
#       Generate linear coefficients: input (n-grams and language)
#       Smooth data

cv.crossValidationLinearInterpolation(tweetListPreProcessed, 3, maxNgram)

# 3.2-. Algorithms: Ranking Methods

# print(arrayLanguagesFull)
# cv.nestedCrossValidation(tweetListPreProcessed,5,5,[0,0,0],arrayLanguagesFull)
# cv.crossValidation(tweetListPreProcessed, 3, maxNgram+1)

# 3.3-. Out-of-place Measure
