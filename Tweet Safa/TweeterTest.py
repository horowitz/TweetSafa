from PyRSS2Gen import Enclosure

__author__ = 'danielhorowitz'

FRENCH = 'lang%3Afr'
ENGLISH = 'lang%3Aen'
PORTUGUESE = 'lang%3Apt'
SPANISH = 'lang%3Aes'
CATALAN = 'lang%3Acat'
from parse_rest.datatypes import Object
from settings_local import APPLICATION_ID, REST_API_KEY, MASTER_KEY
from parse_rest.connection import register
from twython import Twython
import goslate
consumer_key=""
consumer_secret=""

APP_KEY = 'rW3r87OsW7V5WcL8uNc9m5kmU'
APP_SECRET = 'zsjxaiYf23J5IsJjhZxodrVDVJkBUgWAVfEyBR2bfBwz5GZngV'
consumer_key='rW3r87OsW7V5WcL8uNc9m5kmU',
consumer_secret='zsjxaiYf23J5IsJjhZxodrVDVJkBUgWAVfEyBR2bfBwz5GZngV',
access_token_key='169260565-tlC8ZpYAD4eyyqPaPpzwYD3UPrxgBV9VQ0zxuu3D',
access_token_secret='mKOYFGuklZfo4X5m67pW3LZrB8rnXJlhsKCPasidzSwKt'

twitter = Twython(APP_KEY, APP_SECRET, '169260565-tlC8ZpYAD4eyyqPaPpzwYD3UPrxgBV9VQ0zxuu3D', 'mKOYFGuklZfo4X5m67pW3LZrB8rnXJlhsKCPasidzSwKt')

register(APPLICATION_ID, REST_API_KEY)


class Tweet(Object):
    pass


gs = goslate.Goslate()

languages = list()
languages.append(FRENCH)
languages.append(ENGLISH)
languages.append(PORTUGUESE)
languages.append(SPANISH)
# languages.append(CATALAN)


def inRange(geo):
    lat = geo['coordinates'][0]
    lng = geo['coordinates'][1]
    result = pow(pow(lat, 2) + pow(lng, 2), -2)
    if (result < 0.5):
        return True;
    else:
        return False;


# for city in cities:
# # tweets = api.GetSearch(geocode=("41.263611", "1.773611", "40mi"), count=1000)
#     tweets = api.GetSearch(geocode=city, count=10000)
#
#     for item in tweets:
#         if(item._geo):
#             print 'id = ' + str(item._id) + '\ntext = ' + item._text + "\n\n"
#             newTweet = Tweet(Text=item._text, Language=gs.detect(item._text),tweetId=str(item._id))
#             newTweet.save()

for language in languages:
    maxId = 999999999999999999999999

    for page in range(1,11):
        print('page = ' + str(page))
        print('maxId = ' + str(maxId))
        if page == 1:
            query = twitter.search(q=language,src='typd',count=100)
        else:
            query = twitter.search(q=language,src='typd',count=100,max_id=maxId)

        for result in query['statuses']:
            text = result['text']
            id = result['id']
            if id != maxId:
                newTweet = Tweet(Text=text, Language=gs.detect(text), tweetId=str(id))
                newTweet.save()

            if id < maxId:
                maxId = id
                print('changed maxId to ' + str(maxId))