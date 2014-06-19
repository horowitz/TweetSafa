
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

#for tweet in tweetListPreProcessed:
#    print tweet.text
print tweetList.__len__()


# Clean data -> Algorithm