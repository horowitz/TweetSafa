__author__ = 'danielhorowitz'
import TwitterAPI as TwitterAPI
import CreateTweetFiles as localTweets

def createLanguagesList():
    languages = list()
    languages.append(FRENCH)
    languages.append(ENGLISH)
    languages.append(PORTUGUESE)
    languages.append(SPANISH)
    return languages


# Language parameters for the twitter search query
FRENCH = 'lang%3Afr'
ENGLISH = 'lang%3Aen'
PORTUGUESE = 'lang%3Apt'
SPANISH = 'lang%3Aes'
CATALAN = 'lang%3Acat'

consumer_key='rW3r87OsW7V5WcL8uNc9m5kmU',
consumer_secret='zsjxaiYf23J5IsJjhZxodrVDVJkBUgWAVfEyBR2bfBwz5GZngV',
access_token_key='169260565-tlC8ZpYAD4eyyqPaPpzwYD3UPrxgBV9VQ0zxuu3D',
access_token_secret='mKOYFGuklZfo4X5m67pW3LZrB8rnXJlhsKCPasidzSwKt'

languages = createLanguagesList()

# This method creates a database in Parse.com and performs a search in twitter for 4 languages EN,ES,PT,FR
TwitterAPI.performTwitterSearch(consumer_key,consumer_secret,access_token_key,access_token_secret,languages)

# After creating the online database, we can retrieve the db items and create local datasets

# These methods create the local datasets files
localTweets.writeFile("datasets/eng_tweets_x.txt",'en')
localTweets.writeFile("datasets/es_tweets_x.txt",'es')
localTweets.writeFile("datasets/pt_tweets_x.txt",'pt')
localTweets.writeFile("datasets/fr_tweets_x.txt",'fr')

