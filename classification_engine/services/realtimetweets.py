"""
Realtime Tweets Resources. 
"""

import falcon
from bson import json_util

import classification_engine.infraestructure.odm.tweets_dal as tweets_dal

class RealtimeTweetsResource:

    def on_get(self, req, resp, timestamp):
        """Retorna los tweets cuyo timespan sea mayor o igual al parametrizado.
            Parámetros:
                timestamp: int, number of seconds since the epoch.
        """

        tweets = []

        cursor = tweets_dal.find({'timestamp_ms': {'$gte': timestamp}})

        for tweet in cursor:
            tweets.append(tweet)
        
        resp.status = falcon.HTTP_200        
        resp.body = json_util.dumps(tweets, json_options=json_util.RELAXED_JSON_OPTIONS)

