"""
Clasificación de tweets en tiempo real.
"""

from falcon import HTTP_ACCEPTED

import classification_engine.infraestructure.twitter.streaming as stream
import classification_engine.infraestructure.clasification.tweet_processing as proceso

__stream__ = stream.Stream(True)
__proceso__ = proceso.Proceso(True)

class ClassificationsResource:

    def __init__(self):
        pass

    def on_post(self, req, resp, terms):
        """Inicia clasificaciòn de tweets en tiempo real. Filtra los mensajes según terms.
            Parametros
                terms: lista de términos.
        """

        __stream__.start(terms)
        __proceso__.start()

        #resp.status = HTTP_ACCEPTED

    def on_put(self, req, resp):
        """Si está ejecutando, detiene la clasificación en tiempo real de tweets.
        """
        __stream__.stop()
        __proceso__.stop()
        
        #resp.status = HTTP_ACCEPTED

if __name__ == "__main__":
    import time
    clasificacion = ClassificationsResource()
    clasificacion.on_post(None, None, [])
    time.sleep(300)
    clasificacion.on_put(None, None) 