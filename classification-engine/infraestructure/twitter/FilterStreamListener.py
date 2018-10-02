import tweepy
from authentication import get_api

__ARGENTINA__ = [-1.157420, 37.951741, -1.081202, 38.029126]

class FilterStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status)

if __name__ == "__main__":
    api = get_api()
    myStreamListener = FilterStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=['dolar'], languages=['es'], locations=__ARGENTINA__)