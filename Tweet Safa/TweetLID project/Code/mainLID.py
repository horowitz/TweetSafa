
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils

# 1-. Read dataset
dataset = "../Dataset/output.txt"

tweetList = read.read_tweets_dataset(dataset)

# Print tweets and the quantity of tweets
#for tweet in tweetList:
    #print tweet.text
#print tweetList.__len__()


# 2-. Pre-process state
tweetListPreProcessed = preprocess.main(tweetList)

# for tweet in tweetListPreProcessed:
#     print tweet.text
# print tweetList.__len__()


# Clean data ->

# 3-. Algorithms OBTAIN N-GRAMS

# Join all the tweets in one language. Return one dictionary of languages
corpus = utils.concatenateLanguageTweets(tweetListPreProcessed)

# Only individual languages(en,es,..): individualLanguage=true, mixed languages(en+es,pt+gl,..): individualLanguage=false
individualLanguage = True
if individualLanguage:
    corpus = utils.separateIndividualLanguages(corpus)

# clean dictionary of double spaces from concatenation
for key in corpus.keys():
    corpus[key] = preprocess.remove_multiple_spaces(corpus.get(key))

maxNgram = 5
# N-gram Frequency distributions for all N and for all Languages.
# Returns Dictionary of maxNgrams dictionaries of each language.
# corpus.get(str(number)).get('language')
corpusNgrams = utils.freqDistributions(corpus, maxNgram)
print(corpusNgrams.get(str(4)).get('pt'))
# Example:  print(corpusNgrams.get(str(3)).get('pt'))

# Clean data -> Algorithm

# 3-1. Algorithms: Bayesian Networks

# 3-2. Algorithms: Ranking Methods

# 3-2-1. Out-of-place Measure