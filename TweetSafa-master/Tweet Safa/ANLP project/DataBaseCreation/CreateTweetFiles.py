import nltk
import unicodedata
import re
from parse_rest.datatypes import Object
from settings_local import APPLICATION_ID, REST_API_KEY, MASTER_KEY
from parse_rest.connection import register

register(APPLICATION_ID, REST_API_KEY)


class Tweet(Object):
    pass
# Gets string, removes URLs and returns the string
def cleanTweets(text):
   # remove urls
   p = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|[^A-Za-z0-9 ]')
   cleanText = re.sub(p,'', text)
   return cleanText

def writeFile(filename,language):

    engTweets = Tweet.Query.all().order_by("Text").limit(1000).skip(0).filter(Language=language)
    file = open(filename, "w")
    lastRow = ''
    for tweet in engTweets:
        text = tweet.Text
        text = text.enconde('utf-8')
        text = text.lower()

        if lastRow != text:
            file.write(text + "\n")
            lastRow = text

    file.close()


    #
    # f = open('a_text_file')
    # raw = f.read()
    #
    # tokens = nltk.word_tokenize(raw)
    #
    # #Create your bigrams
    # bgs = nltk.bigrams(tokens)
    #
    # #compute frequency distribution for all the bigrams in the text
    # fdist = nltk.FreqDist(bgs)
    # for k,v in fdist.items():
    #     print k,v