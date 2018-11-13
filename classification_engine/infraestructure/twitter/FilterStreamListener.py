import tweepy

from ..odm.raw_tweets_dal import insert_one
from .authentication import get_api

__ARGENTINA__ = [-73.616669,-55.185078,-53.637451,-21.781168]

class FilterStreamListener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.cuenta = 0

    def on_status(self, status):
        insert_one(status._json)
        self.cuenta += 1
        print("inserted..." + str(self.cuenta))

def filter(terms):
    """Abre un stream y filtra los mensajes segùn la lista de términos."""

    api = get_api()
    myStreamListener = FilterStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=terms, languages=['es'], locations=__ARGENTINA__)

if __name__ == "__main__":
    filter([])