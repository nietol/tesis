"""
Clasificación de tweets en tiempo real.
"""

import time
from falcon import HTTP_ACCEPTED
from bson import json_util

import classification_engine.infraestructure.twitter.streaming as stream
import classification_engine.infraestructure.clasification.tweet_processing as proceso

__stream__ = stream.Stream(True)
__proceso__ = proceso.Proceso(True)

class ClassificationsResource:

    def __init__(self):
        self.started = False
        self.started_at = 0        

    def on_post(self, req, resp):
        """Inicia clasificaciòn de tweets en tiempo real. Filtra los mensajes según terms.
            POST Data:
                Array(String) => Lista de términos.
        """
        
        raw_data = req.bounded_stream.read()
        terms = []

        if raw_data:
            terms = json_util.loads(raw_data.decode("utf-8"), json_options=json_util.RELAXED_JSON_OPTIONS)

        geolocalizar = not terms #si no hay términos de búsqueda, se geolocaliza.

        if not self.started:            
            self.started_at = int(time.time() * 1000)
            __stream__.start(terms, geolocalizar)
            __proceso__.start(geolocalizar)
            self.started = True
        
        response_body = { 'started_at': self.started_at }
        resp.status = HTTP_ACCEPTED
        resp.body = json_util.dumps(response_body, json_options=json_util.RELAXED_JSON_OPTIONS)

    def on_put(self, req, resp):
        """Si está ejecutando, detiene la clasificación en tiempo real de tweets.
        """        
        __stream__.stop()
        __proceso__.stop()
        self.started = False        
        resp.status = HTTP_ACCEPTED
        print('Classification stoped')

if __name__ == "__main__":
    import time
    clasificacion = ClassificationsResource()
    clasificacion.on_post(None, None)
    time.sleep(300)
    clasificacion.on_put(None, None) 