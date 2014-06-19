import ReadData as read
import re
import string

def lower_case(tweet):
    return tweet.decode('utf-8').lower()

def remove_multiple_spaces(tweet):
    tweet = ' ' + tweet + ' '
    tweet = re.sub(' +',' ',tweet)
    return tweet

def remove_puntuation(tweet):
    return reduce(lambda tweet, c: tweet.replace(c, ' '), string.punctuation, tweet)

def remove_url(tweet):
    #p = re.compile('/((?:https?\:\/\/|www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i')

    #a = re.compile('/(pic.twitter+.# *)/i')
    #tweet = re.sub(a,'',tweet)

    return re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)

    #return re.sub(p,'', tweet)

def main(tweetList):
    tweetListPreprocessed = []
    tweetPreprocessed = ""

    for tweet in tweetList:
        tweetPreprocessed = lower_case(tweet.text)
        tweetPreprocessed = remove_url(tweetPreprocessed)
        tweetPreprocessed = remove_puntuation(tweetPreprocessed)
        tweetPreprocessed = remove_multiple_spaces(tweetPreprocessed)

        # Save in new object
        tweetPre = read.make_tweet(tweet.id, tweet.name, tweet.language, tweetPreprocessed)
        tweetListPreprocessed.append(tweetPre)

    return tweetListPreprocessed
