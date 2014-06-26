from __future__ import division
from __future__ import division
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

    for N in xrange(1, maxNgram+1):
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
def obtainNgrams(tweetListPreProcessed,maxNgram):
    # Join all the tweets in one language. Return one dictionary of languages
    corpus, arrayLanguagesFull = concatenateLanguageTweets(tweetListPreProcessed)
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
    corpusNgrams = freqDistributions(corpus, maxNgram)
    return corpusNgrams, arrayLanguages,arrayLanguagesFull

# Calculates out of place measure
def outofplaceMeasure(FDLenght, TTLenght, freqDist, freqDistTest):
    outofplaceResult = list()

    FDLenght = min(len(freqDist), FDLenght)
    TTLenght = min(len(freqDistTest), TTLenght)
    # Get m x n items
    topFDItems = freqDist.items()[:FDLenght]
    topTTItems = freqDistTest.items()[:TTLenght]

    totalDistance = 0
    for i in xrange(0, TTLenght):
        # print(testText + "\t" + str(TTLenght) + "\t" +str(len(topTTItems)))
        lp = topTTItems[i]
        distance = FDLenght
        for j in xrange(0, FDLenght):
            tp = topFDItems[j]
            if lp[0] == tp[0] or j == FDLenght - 1:
                distance = abs(i - j)
                totalDistance += distance
                break
    return totalDistance / (FDLenght * TTLenght)
# returns confidence of each N-gram to be a good guesser.
def learnNgramConfidences(confidenceDict,corpusNgrams,tweet,m,n):
    acc=0
    tot=0
    label=tweet.language
    ngramPredictedLanguage=list()
    for key in corpusNgrams.keys():
        predictedLanguage=list()
        languagesList= None
        print('N: '+ key)
        languagesList=corpusNgrams.get(key).keys()
        for subkey in languagesList:
            # print ('Length' + str(len(corpusNgrams.get(key).get(subkey)) ))
            predictedLanguage.append(outofplaceMeasure(m,n,corpusNgrams.get(key).get(subkey),getFreqDist(tweet.text,int(float(key)))))
        predicted=languagesList[predictedLanguage.index(min(predictedLanguage))]
        if label == predicted:
            confidenceDict[key]=confidenceDict[key]+1
            acc=acc+1
        tot=tot+1
    return confidenceDict,tot

# returns confidence of each N-gram to be a good guesser for a whole train set.
def learnNgramConfidencefromData(trainDist,validationSet):
    confidenceDict=dict((el,0) for el in trainDist[0].keys())
    tot=0
    for tweet in validationSet:
        confidenceDict , totAux = learnNgramConfidences(confidenceDict,trainDist[0],tweet,80,50)
        tot=tot+totAux
    confidenceDict = dict((el,confidenceDict.get(el)/tot) for el in confidenceDict.keys())
    return confidenceDict

# evaluate test Set
def evaluateNgramRakingSet(validationSet, trainFreq,confidenceNgrams,m,n):
    predictedLanguage=list()
    trueLanguage=list()
    for tweet in validationSet:
        trueLanguage.append(tweet.language)
        predictedLanguage.append(evaluateNgramRanking(tweet, trainFreq,confidenceNgrams,m,n))
    return predictedLanguage, trueLanguage

# evaluate single tweet
def evaluateNgramRanking(tweet,trainFreq,confidenceDict,m,n):
    acc=0
    tot=0
    label=tweet.language
    predictedDict=dict()
    for key in trainFreq[0].keys():
        predictedLanguage=list()
        languagesList=trainFreq[0].get(key).keys()
        for subkey in languagesList:
            predictedLanguage.append(outofplaceMeasure(m,n,trainFreq[0].get(key).get(subkey),getFreqDist(tweet.text,int(float(key)))))
        predicted=languagesList[predictedLanguage.index(min(predictedLanguage))]
        if label == predicted:
            acc=acc+1
        tot=tot+1
        if not predictedDict.has_key(predicted):
            predictedDict[predicted] = confidenceDict.get(key)
        else:
            predictedDict[predicted] = predictedDict.get(predicted) + confidenceDict.get(key)
    predictedL=chooseLanguages(predictedDict,0.01)
    return predictedL

# choose best languages
def chooseLanguages(predictedDict,threshold):
    items = [(v, k) for k, v in predictedDict.items()]
    items.sort()
    items.reverse()
    items = [(k, v) for v, k in items]
    language,value = items.pop(0)
    count = 0
    if not language=='other' or not language=='und':
        for k,v in items:
            count += 1
            if count == 1:
                continue
            else:
                if value-v < threshold and not count > 2 :
                    if not k=='other' and not k=='und':
                        language = language+'+'+k
                else:
                    break
    return language

# order vector
def orderVector(arrayLanguagesFull):
    orderedVector=list()
    for el in arrayLanguagesFull:
        if(not '+' in el and not '/' in el and not 'other' in el and not 'und' in el):
            orderedVector.append(el)
    orderedVector.append('other')
    orderedVector.append('und')
    for el in arrayLanguagesFull:
        if('+' in el):
            orderedVector.append(el)
    for el in arrayLanguagesFull:
        if('/' in el):
            orderedVector.append(el)
    return orderedVector

