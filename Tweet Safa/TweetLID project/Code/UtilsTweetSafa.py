
import nltk as nk
import PreprocessTweets as preprocess

# This method concatenates tweets

def concatenateLanguageTweets(List):
    corpus = dict()
    languageArray = list()

    for tweet in List:
        if ~corpus.has_key(tweet.language) & (corpus.get(tweet.language) is None):
            corpus[tweet.language] = tweet.text
            languageArray.append(tweet.language)
        else:
            corpus[tweet.language] = corpus.get(tweet.language) + tweet.text
    return corpus, languageArray

# Separate by individual languages(en,es,eu,ca,gl,pt,und,other). Return a dictionary of individual languages

def separateIndividualLanguages(List):
    individualCorpus = dict()
    languageArray = list()

    for key in List.keys():
        if (not '+' in key) and (not '/' in key):
            individualCorpus[key] = List.get(key)
            languageArray.append(key)
            for subKey in List.keys():
                if key in subKey and not key is subKey:

                    individualCorpus[key] = individualCorpus[key] + List.get(subKey)

    return individualCorpus, languageArray

# N-gram Frequency distributions for all N and for all Languages.
# Returns Dictionary of maxNgrams dictionaries of each language.
# corpus.get(str(number)).get('language')

def freqDistributions(corpus, maxNgram):
    corpusNgrams = dict()

    for N in xrange(1, maxNgram):
        auxCorpus = dict()

        for key in corpus.keys():
            auxCorpus[key] = getFreqDist(corpus.get(key), N)

        corpusNgrams[str(N)] = auxCorpus

    return corpusNgrams

# returns N-gram distribution given a text

def getFreqDist(text, n):
    ngramsObject = nk.ngrams(text, n)
    freqDist = nk.FreqDist(ngramsObject)
    return freqDist

# Print tweets from an input list

def printTweets(tweetList):
    for tweet in tweetList:
        print tweet.text

# Obtain N-Grams from the tweet list

def obtainNgrams(tweetListPreProcessed):

    # Join all the tweets in one language. Return one dictionary of languages
    corpus, arrayLanguages = concatenateLanguageTweets(tweetListPreProcessed)

    # individualLanguage=true:
    #       Only individual languages(en,es,..)

    # individualLanguage=false:
    #       Mixed languages(en+es,pt+gl,..)

    individualLanguage = True

    if individualLanguage:
        corpus, arrayLanguages = separateIndividualLanguages(corpus)

    # clean dictionary of double spaces from concatenation
    for key in corpus.keys():
        corpus[key] = preprocess.remove_multiple_spaces(corpus.get(key))

    maxNgram = 5

    corpusNgrams = freqDistributions(corpus, maxNgram)

    return corpusNgrams, arrayLanguages

def outofplaceMeasure(FDLenght, TTLenght, freqDist,freqDistTest):
    outofplaceResult = list()

    FDLenght=min(len(freqDist),FDLenght)
    TTLenght=min(len(freqDistTest),TTLenght)
    # Get m x n items
    topFDItems = freqDist.items()[:FDLenght]
    topTTItems = freqDistTest.items()[:TTLenght]


    totalDistance = 0
    for i in xrange(0,TTLenght):
        # print(testText + "\t" + str(TTLenght) + "\t" +str(len(topTTItems)))
        lp = topTTItems[i]
        distance = FDLenght
        for j in xrange(0,FDLenght):
            tp = topFDItems[j]
            if lp[0] == tp[0] or j == FDLenght-1:
                distance = abs(i-j)
                totalDistance += distance
                break
    return totalDistance/(FDLenght*TTLenght)