"""
Tweets Resources. 
"""

import falcon
from bson import json_util
import datetime

import classification_engine.infraestructure.odm.tweets_dal as tweets_dal

class TweetsResource:    

    def on_get(self, req, resp, fechaDesde, fechaHasta):
        """Retorna los tweets comprendidos entre fechaDesde y FechaHasta.
            Parémetros:
                fechaDesde: UTC Date.
                fechaHasta: UTC Date.
        """

        tweets = []

        cursor = tweets_dal.find({ '$and': [
            {'date': {'$gte': fechaDesde}},
            {'date': {'$lte': fechaHasta}}
        ]})

        for tweet in cursor:
            tweets.append(tweet)
        
        resp.status = falcon.HTTP_200        
        resp.body = json_util.dumps(tweets, json_options=json_util.RELAXED_JSON_OPTIONS)