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
                fechaDesde: Date, with UTC Offset.
                fechaHasta: Date, with UTC Offset.
        """
        tweets = []

        filter = { 'date': {'$gte': fechaDesde, '$lte': fechaHasta} }
        cursor = tweets_dal.find(filter) 

        for tweet in cursor:
            tweets.append(tweet)
        
        resp.status = falcon.HTTP_200        
        resp.body = json_util.dumps(tweets, json_options=json_util.RELAXED_JSON_OPTIONS)

        count = cursor.collection.count_documents(filter)
        print('Tweets count: ' + str(count))