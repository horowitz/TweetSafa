import copy

def lower_case(tweet):
    return tweet.lower()


def main(tweetList):
    tweetListPreprocessed = []
    counter = 0
    for tweet in tweetList:
        counter = counter + 1
        tweetPreprocessed = lower_case(tweet.text)
        tweetList[counter].text = tweetPreprocessed
        print counter
        print tweetList[counter].text
