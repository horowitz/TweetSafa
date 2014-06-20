
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

# This method concatenates tweets
def concatenateLanguageTweets(List):
    corpus=dict()
    for tweet in List:
        if ~corpus.has_key(tweet.language) & (corpus.get(tweet.language) is None):
            corpus[tweet.language]= tweet.text
        else:
            corpus[tweet.language] = corpus.get(tweet.language) + tweet.text
    return corpus

# Separate by individual languages(en,es,eu,ca,gl,pt,und,other). Return a dictionary of individual languages
def separateIndividualLanguages(List):
    individualCopus={}
    for key in List.keys():
        if (not '+' in key) and (not '/' in key):
            individualCopus[key]=List.get(key)
            for subKey in List.keys():
                if key in subKey and not key is subKey:
                    individualCopus[key]=individualCopus[key] + List.get(subKey)
    return individualCopus





# Join all the tweets in one language. Return one dictionary of languages
corpus=concatenateLanguageTweets(tweetListPreProcessed)

# Only individual languages(en,es,..): individualLanguage=true, mixed languages(en+es,pt+gl,..): individualLanguage=false
individualLanguage=True
if individualLanguage==True:
    corpus=separateIndividualLanguages(corpus)

# clean dictionary of double spaces from concatenation
for key in corpus.keys():
    corpus[key]=preprocess.remove_multiple_spaces(corpus.get(key))



# Clean data -> Algorithm

# 3-1. Algorithms: Bayesian Networks


# 3-2. Algorithms: Ranking Methods
# 3-2-1. Out-of-place Measure

