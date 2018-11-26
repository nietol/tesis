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
            Parámetros:                
                async: bool, default False.
        """        
        self.async = async
        self.geolocalizar = False
        self.running = False
        self._thread = None

    def start(self, geolocalizar = True):
        """Inicia el procesamiento de los tweets.
            Parámetros:
                geolocalizar: bool, default True. Se deben geolicalizar los tweets?
        """
        self.geolocalizar = geolocalizar

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

        filter = { "procesado": { "$exists": False } , "geo": {"$ne": None} }
        if not self.geolocalizar:
            filter = { "procesado": { "$exists": False } }

        while self.running:            
            
            no_procesados = raw_tweets_dal.find(filter)   
            
            a_procesar = no_procesados.collection.count_documents(filter)
            if a_procesar > 0:         
                print("Cantidad de tweets a procesar: " + str(a_procesar))
            else:
                print("Sin tweets a procesar... ")
                sleep(45)
                continue

            for data in no_procesados:
                polarity = predict(data['text'])                

                if self.geolocalizar:
                    geo = GeoPoint(data['coordinates']['coordinates'][1],
                        data['coordinates']['coordinates'][0])
                else:
                    geo = None
                
                tweet_date = parser.parse(data['created_at'])
                tweet_timestamp = int(data['timestamp_ms'])

                #pylint: disable-msg=too-many-arguments
                tweet = Tweet(data['id'], data['user']['screen_name'],
                    data['text'], tweet_date, polarity, geo, tweet_timestamp)
                #pylint: enable-msg=too-many-arguments  

                tweets_dal.insert_one(tweet)
                data['procesado'] = True
                raw_tweets_dal.update_one(data)

if __name__ == "__main__":
    import time
    proc = Proceso(True)
    proc.start()
    time.sleep(60)
    proc.stop()    



