


from parse_rest.datatypes import Object
from parse_rest.connection import register
from settings_local import APPLICATION_ID,MASTER_KEY,REST_API_KEY
import goslate

from twython import Twython

class Tweet(Object):
    pass
def inRange(geo):
    lat = geo['coordinates'][0]
    lng = geo['coordinates'][1]
    result = pow(pow(lat, 2) + pow(lng, 2), -2)
    if (result < 0.5):
        return True;
    else:
        return False;

def performTwitterSearch(consumer_key,consumer_secret,access_token_key,access_token_secret,languages):

    twitter = Twython(consumer_key, consumer_secret, access_token_key, access_token_secret)

    register(APPLICATION_ID, REST_API_KEY)

    gs = goslate.Goslate()

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





