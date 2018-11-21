import tweepy

from ..odm.raw_tweets_dal import insert_one
from .authentication import get_api

__ARGENTINA__ = [-73.616669,-55.185078,-53.637451,-21.781168]
__stream = None


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

    global __stream

    api = get_api()
    myStreamListener = FilterStreamListener()
    __stream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    __stream.filter(track=terms, languages=['es'], locations=__ARGENTINA__, async=True)

def stop():
    """Detiene el thread que ejecuta lee el stream de twitter."""

    global __stream

    if __stream is not None:
        print("__stream.disconnect()")
        __stream.disconnect()

if __name__ == "__main__":
    import time    
    filter([])
    time.sleep(60)
    stop()