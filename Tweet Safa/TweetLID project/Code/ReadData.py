import csv

# Create Tweet object to save all the necessary arguments of the tweets:
#   Arguments:
#       + id = username id
#       + name = username name
#       + languange = language of the tweet
#       + text = tweet text

class Tweet(object):
    id = 0
    name = ""
    language = ""
    text = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, id, name, language, text):
        self.id = id
        self.name = name
        self.language = language
        self.text = text

def make_tweet(id, name, language, text):
    tweet = Tweet(id, name, language, text)
    return tweet


# Read the tweet from the input dataset and get the values separated by the tab

def read_tweets_dataset(dataset):
    # Read TweetLID dataset
    tweetList = []
    with open(dataset) as file:
        for line in csv.reader(file, dialect="excel-tab"):
            tweet = make_tweet(line[0], line[1], line[2], line[3])
            tweetList.append(tweet)

    return tweetList