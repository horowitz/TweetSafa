import ReadData as read

def lower_case(tweet):
    return tweet.decode('utf-8').lower()


def main(tweetList):
    tweetListPreprocessed = []
    tweetPreprocessed = ""

    for tweet in tweetList:
        tweetPreprocessed = lower_case(tweet.text)

        # Save in new object
        tweetPre = read.make_tweet(tweet.id, tweet.name, tweet.language, tweetPreprocessed)
        tweetListPreprocessed.append(tweetPre)

    return tweetListPreprocessed
