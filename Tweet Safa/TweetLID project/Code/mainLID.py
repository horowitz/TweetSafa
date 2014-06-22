
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils
import Smoothing as linear
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

text = "my name is james"
prob = 1.0;
for i in range(0,len(text)-3):
    x = text[i]; y = text[i+1]; z = text[i+2]
    probability = linear.probability(corpusNgrams, linearCoefficients, x, y, z)
    prob = prob * probability

sys.stdout.write("Sequence probability: "+str(prob)+"\n")

# 3.2-. Algorithms: Bayesian Networks

# 3.3-. Algorithms: Ranking Methods

# 3.4-.. Out-of-place Measure