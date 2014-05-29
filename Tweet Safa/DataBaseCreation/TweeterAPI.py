
BURGOS = ('42.333333', '-3.7','40mi')
VIC = ('41.930278', '2.254722','40mi')
LIVERPOOL = ('53.4', '-3','40mi')
TOULOUSE = ('43.605278','1.442778','40mi')
COIMBRA = ('40.25', '-8.45','40mi')

from parse_rest.datatypes import Object
from parse_rest.connection import register
import goslate

import twitter


register(APPLICATION_ID,REST_API_KEY)

class Tweet(Object):
    pass
gs = goslate.Goslate()

cities = list()
cities.append(BURGOS)
cities.append(VIC)
cities.append(LIVERPOOL)
cities.append(TOULOUSE)
cities.append(COIMBRA)


def inRange(geo):
    lat = geo['coordinates'][0]
    lng = geo['coordinates'][1]
    result = pow(pow(lat,2) + pow(lng,2),-2)
    if (result < 0.5):
        return True;
    else:
        return False;

api = twitter.Api(consumer_key='rW3r87OsW7V5WcL8uNc9m5kmU',
                  consumer_secret='zsjxaiYf23J5IsJjhZxodrVDVJkBUgWAVfEyBR2bfBwz5GZngV',
                  access_token_key='169260565-tlC8ZpYAD4eyyqPaPpzwYD3UPrxgBV9VQ0zxuu3D',
                  access_token_secret='mKOYFGuklZfo4X5m67pW3LZrB8rnXJlhsKCPasidzSwKt')

for city in cities:
# tweets = api.GetSearch(geocode=("41.263611", "1.773611", "40mi"), count=1000)
    tweets = api.GetSearch(geocode=city, count=100)

    for item in tweets:
        # if(item._geo):
        print 'id = ' + str(item._id) + '\ntext = ' + item._text + "\n\n"
        newTweet = Tweet(Text=item._text, Language=gs.detect(item._text),tweetId=str(item._id))
        newTweet.save()


