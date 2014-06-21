
import nltk as nk
import PreprocessTweets as preprocess

# This method concatenates tweets

def concatenateLanguageTweets(List):
    corpus=dict()
    languageArray=list()
    for tweet in List:
        if ~corpus.has_key(tweet.language) & (corpus.get(tweet.language) is None):
            corpus[tweet.language]= tweet.text
            languageArray.append(tweet.language)
        else:
            corpus[tweet.language] = corpus.get(tweet.language) + tweet.text
    return corpus,languageArray

# Separate by individual languages(en,es,eu,ca,gl,pt,und,other). Return a dictionary of individual languages

def separateIndividualLanguages(List):
    individualCopus=dict()
    languageArray=list()
    for key in List.keys():
        if (not '+' in key) and (not '/' in key):
            individualCopus[key]=List.get(key)
            for subKey in List.keys():
                if key in subKey and not key is subKey:
                    languageArray.append(key)
                    individualCopus[key]=individualCopus[key] + List.get(subKey)
    return individualCopus, languageArray

# N-gram Frequency distributions for all N and for all Languages.
# Returns Dictionary of maxNgrams dictionaries of each language.
# corpus.get(str(number)).get('language')

def freqDistributions(corpus,maxNgram):
    corpusNgrams=dict()
    for N in xrange(1,maxNgram):
        auxCorpus=dict()
        for key in corpus.keys():
            auxCorpus[key]=getFreqDist(corpus.get(key),N)
        corpusNgrams[str(N)]=auxCorpus
    return corpusNgrams

# returns N-gram distribution given a text

def getFreqDist(text,n):
    ngramsObject = nk.ngrams(text,n)
    freqDist = nk.FreqDist(ngramsObject)
    return freqDist

# Print tweets from an input list

def printTweets(tweetList):
    for tweet in tweetList:
        print tweet.text

def obtainNgrams(tweetListPreProcessed):

    # Join all the tweets in one language. Return one dictionary of languages
    corpus,arrayLanguages = concatenateLanguageTweets(tweetListPreProcessed)

    # Only individual languages(en,es,..): individualLanguage=true, mixed languages(en+es,pt+gl,..): individualLanguage=false
    individualLanguage = True

    if individualLanguage:
        corpus,arrayLanguages = separateIndividualLanguages(corpus)

    # clean dictionary of double spaces from concatenation
    for key in corpus.keys():
        corpus[key] = preprocess.remove_multiple_spaces(corpus.get(key))

    maxNgram=5

    corpusNgrams = freqDistributions(corpus, maxNgram)

    return corpusNgrams