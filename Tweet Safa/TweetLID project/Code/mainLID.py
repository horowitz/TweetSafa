
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils

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

corpusNgrams = utils.obtainNgrams(tweetListPreProcessed)

print(corpusNgrams.get(str(4)).get('es'))

# Example:  print(corpusNgrams.get(str(3)).get('pt'))

# Clean data -> Algorithm

# 3.2-. Algorithms: Bayesian Networks

# 3.3-. Algorithms: Ranking Methods

# 3.4-.. Out-of-place Measure