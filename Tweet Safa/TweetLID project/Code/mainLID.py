
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils

# 1-. Read dataset and create tweetList fullfilled of Tweet object
dataset = "../Dataset/emoticons.txt"

tweetList = read.read_tweets_dataset(dataset)

# 2-. Pre-process state
tweetListPreProcessed = preprocess.main(tweetList)

#for tweet in tweetListPreProcessed:
    # print tweet.text
# print tweetList.__len__()


# Clean data -> tweetListPreProcessed

# 3-. Algorithms OBTAIN N-GRAMS

# Join all the tweets in one language. Return one dictionary of languages
corpus,arrayLanguages = utils.concatenateLanguageTweets(tweetListPreProcessed)

# Only individual languages(en,es,..): individualLanguage=true, mixed languages(en+es,pt+gl,..): individualLanguage=false
individualLanguage = True

if individualLanguage:
    corpus,arrayLanguages = utils.separateIndividualLanguages(corpus)

# clean dictionary of double spaces from concatenation
for key in corpus.keys():
    corpus[key]=preprocess.remove_multiple_spaces(corpus.get(key))

maxNgram=5

corpusNgrams = utils.freqDistributions(corpus, maxNgram)
#print(corpusNgrams.get(str(4)).get('pt'))

# Example:  print(corpusNgrams.get(str(3)).get('pt'))

# Clean data -> Algorithm

# 3-1. Algorithms: Bayesian Networks

# 3-2. Algorithms: Ranking Methods


# 3-2-1. Out-of-place Measure