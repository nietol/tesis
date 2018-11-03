import tweepy

CONSUMER_KEY = "PLkddisggl5SHeucRbGYOXMA2"
CONSUMER_SECRET = "NUzdpOvan3vY1Gg0jhMjmmbkyN3T11PtwObuUdXmb7XOUe4RuE"

ACCESS_TOKEN = "861247683880771584-4xWt0UaiS3nWRYvgXW7Jtcin6r9OMr8"
ACCESS_TOKEN_SECRET = "QxjiVdGa803vQBQ2vhkdz089Lgr707YEUjJYJ93qklihD"

def get_auth_handler():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return auth

def get_api():
    """Get api object."""

    auth = get_auth_handler()
    api = tweepy.API(auth)

    return api

if __name__ == "__main__":

    api = get_api()
    #me = api.me()
    #print(me)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet)