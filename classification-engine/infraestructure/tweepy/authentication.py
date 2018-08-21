import tweepy

CONSUMER_KEY = "0oUad8zhU7m8iSxAMHZxyoCAu"
CONSUMER_SECRET = "rYIQGPxOVBdPvw613zBMPE92aMkngY0eozTm79dOyFy7onUUKC"

ACCESS_TOKEN = "861247683880771584-aTEi142PvVdou2l1CDzxx3dpCToSUVr"
ACCESS_TOKEN_SECRET = "yOWkM8E1PaTHVG5o92kw2sSZ6TZeBOuwqihntUU8UZhrr"

def get_auth_handler():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return auth

if __name__ == "__main__":
    auth = get_auth_handler()
    api = tweepy.API(auth)
    #me = api.me()
    #print(me)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet)

    