__author__ = 'danielhorowitz'

from parse_rest.datatypes import Object
from settings_local import APPLICATION_ID, REST_API_KEY, MASTER_KEY
from parse_rest.connection import register
register(APPLICATION_ID,REST_API_KEY)

class Tweet(Object):
    pass

# newTweet = Tweet(Text="mira", Language="es")
# newTweet.save()

high_scores = Tweet.Query.filter(Language='en')

print(high_scores)