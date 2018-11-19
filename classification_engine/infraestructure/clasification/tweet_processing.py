"""
Módulo para el procesamiento de tweets.
Clasificación y procesamiento de localización.
"""

import classification_engine.infraestructure.odm.raw_tweets_dal as raw_tweets_dal
import classification_engine.infraestructure.odm.tweets_dal as tweets_dal
#from ..odm.raw_tweets_dal import find, update_one
#from bson import json_util
from dateutil import parser

from ...domain.Tweet import Tweet, GeoPoint
from .polarity_predictor import predict

def procesar():
    """Procesa tweets marcados como no procesados"""

    # filter = { "procesado": { "$exists": False } , "geo": {"$ne": None} }
    filter = { "geo": {"$ne": None} }
    no_procesados = raw_tweets_dal.find(filter)

    print(no_procesados.count())
    
    for data in no_procesados:

        polarity = predict(data['text'])
        geo = GeoPoint(data['coordinates']['coordinates'][1],
            data['coordinates']['coordinates'][0])
        
        tweet_date = parser.parse(data['created_at'])

        tweet = Tweet(data['id'], data['user']['screen_name'],
            data['text'], tweet_date, polarity, geo)

        tweets_dal.insert_one(tweet)
        data['procesado'] = True
        raw_tweets_dal.update_one(data)

if __name__ == "__main__":
    procesar()


