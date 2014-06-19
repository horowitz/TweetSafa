
import ReadData as read


# Read dataset
dataset = "..\Dataset\output.txt"
tweetList = read.read_tweets_dataset(dataset)

for tweet in tweetList:
    print tweet.text


print tweetList.__len__()
# Pre-process state


# Clean data ->