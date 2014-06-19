import ReadData as read
import re
import string

punctuation = '!\"#$%&()*+,-./:;<=>?[\]^`{|}~'

def lower_case(tweet):
    return tweet.decode('utf-8').lower()

def remove_multiple_spaces(tweet):
    tweet = ' ' + tweet + ' '
    tweet = re.sub(' +',' ',tweet)
    return tweet

def remove_puntuation(tweet):
    return reduce(lambda tweet, c: tweet.replace(c, ' '), punctuation, tweet)

def format_puntuation(tweet):
    return reduce(lambda tweet, c: tweet.replace(c, ' ' + c + ' '), punctuation, tweet)

def remove_url(tweet):

    URLless_string = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet)

    return URLless_string

def remove_usernames(tweet):

    usernameLess_string = re.sub('@[^\s]+', '', tweet)

    return usernameLess_string

def remove_pic_twitter(tweet):

    result = re.sub('pic.twitter[^\s|,]+', '', tweet)

    return result


def remove_vowel_repetitions(tweet):
    result = re.sub(r'(.)\1\1+', r'\1\1', tweet)

    return result


def main(tweetList):
    tweetListPreprocessed = []

    tweetPreprocessed = ""

    for tweet in tweetList:
        tweetPreprocessed = lower_case(tweet.text)
        tweetPreprocessed = remove_pic_twitter(tweetPreprocessed)
        tweetPreprocessed = remove_url(tweetPreprocessed)
        tweetPreprocessed = format_puntuation(tweetPreprocessed)
        tweetPreprocessed = remove_usernames(tweetPreprocessed)
        tweetPreprocessed = remove_puntuation(tweetPreprocessed)
        tweetPreprocessed = remove_multiple_spaces(tweetPreprocessed)
        tweetPreprocessed = remove_vowel_repetitions(tweetPreprocessed)

        # Save in new object
        tweetPre = read.make_tweet(tweet.id, tweet.name, tweet.language, tweetPreprocessed)
        tweetListPreprocessed.append(tweetPre)

    return tweetListPreprocessed
