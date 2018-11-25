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

class Stream:
    """Stream hacia twitter streaming api."""

    def __init__(self, async = False):
        self._async = async
        self.running = False

    def start(self, terms):
        """Abre un stream y filtra los mensajes segùn la lista de términos."""

        if not self.running:            
            api = get_api()
            myStreamListener = FilterStreamListener()
            self._stream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
            self._stream.filter(track=terms, languages=['es'], locations=__ARGENTINA__, async=self._async)
            self.running = True

    def stop(self):
        """Cierra la conexión al stream de twitter."""
        if self._stream is not None:            
            self._stream.disconnect()
            self._stream = None
            self.running = False

if __name__ == "__main__":
    import time
    stream = Stream(True)
    stream.start([])
    time.sleep(60)
    stream.stop()