import ReadData as read
import re

def lower_case(tweet):
    return tweet.decode('utf-8').lower()

def remove_multiple_spaces(tweet):
    return re.sub(' +',' ',tweet)

def main(tweetList):
    tweetListPreprocessed = []
    tweetPreprocessed = ""

    for tweet in tweetList:
        tweetPreprocessed = lower_case(tweet.text)
        tweetPreprocessed = remove_multiple_spaces(tweetPreprocessed)

        # Save in new object
        tweetPre = read.make_tweet(tweet.id, tweet.name, tweet.language, tweetPreprocessed)
        tweetListPreprocessed.append(tweetPre)

    return tweetListPreprocessed
