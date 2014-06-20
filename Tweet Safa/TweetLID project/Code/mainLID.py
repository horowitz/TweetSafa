
import ReadData as read
import PreprocessTweets as preprocess

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

# Only individual languages(en,es,..): individualLanguage=true, mixed languages(en+es,pt+gl,..): individualLanguage=false
individualLanguage=True

# Join all the tweets in one language. Return one dictionary of languages
corpus=dict()
for tweet in tweetListPreProcessed:
    if ~corpus.has_key(tweet.language) & (corpus.get(tweet.language) is None):
        corpus[tweet.language]= tweet.text
    else:
        corpus[tweet.language] = corpus.get(tweet.language) + tweet.text

# clean dictionary of double spaces from concatenation
individualCopus={}
if individualLanguage==True:
    for key in corpus.keys():
        if not "+" in corpus.keys():
            individualCopus[key]=corpus.get(key)

print (len(individualCopus))
for key in corpus.keys():
    corpus[key]=preprocess.remove_multiple_spaces(corpus.get(key))

print(corpus)


# Clean data -> Algorithm

# 3-1. Algorithms: Bayesian Networks


# 3-2. Algorithms: Ranking Methods
# 3-2-1. Out-of-place Measure

