"""
Módulo para el procesamiento de tweets.
Clasificación y procesamiento de localización.
"""

import classification_engine.infraestructure.odm.raw_tweets_dal as raw_tweets_dal
import classification_engine.infraestructure.odm.tweets_dal as tweets_dal

from time import sleep
from dateutil import parser
from threading import Thread

from ...domain.Tweet import Tweet, GeoPoint
from .polarity_predictor import predict

class Proceso:
    """Abstrae el proceso de los tweets en base de datos."""

    def __init__(self, async = False):
        """Constructor.
            Params:
                async, default false.
        """
        self.async = async
        self.running = False
        self._thread = None

    def start(self):
        """Inicia el procesamiento de los tweets."""
        if not self.running:
            self.running = True
            if self.async:
                self._thread = Thread(target=self._procesar)
                self._thread.start()
            else:
                self._procesar()

    def stop(self):
        """Detiene procesamiento de los tweets."""
        self.running = False

    def _procesar(self):
        """Procesa tweets marcados como no procesados"""

        while self.running:
            filter = { "procesado": { "$exists": False } , "geo": {"$ne": None} }            
            no_procesados = raw_tweets_dal.find(filter)
            
            print('cuenta...')
            print(no_procesados.collection.count_documents(filter))
            if no_procesados.count() > 0:         
                print("Cantidad de tweets a procesar: " + str(no_procesados.count()))
            else:
                print("Sin tweets a procesar... ")
                sleep(45)

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
    import time
    proc = Proceso(True)
    proc.start()
    time.sleep(60)
    proc.stop()    



