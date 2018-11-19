import falcon
from bson import json_util
import datetime

import classification_engine.infraestructure.odm.tweets_dal as tweets_dal

# get_all: retorna històrico de clasificaciones, guids + fecha_Desde, fecha_hasta + resultado clasificacion
# tiene que permitir filtrar entre fecha_desde y fecha_hasta

# get: permite buscar los resultados de una clasificaciòn.
# params: id: guid identificando la instancia
# returns: datos asociados a la instancia de clasificaciòn.

# post: permite generar una nueva instancia de clasificaciòn.
# params: frase: string (frase a filtrar), duracion: int (minutos escuchando tweets)
# returns: guid identificando la instancia de clasificaciòn.

class TweetsResources:

    def on_get(self, req, resp, fechaDesde, fechaHasta):    

        tweets = []

        cursor = tweets_dal.find({ '$and': [
            {'date': {'$gte': fechaDesde}},
            {'date': {'$lte': fechaHasta}}
        ]})

        for tweet in cursor:
            tweets.append(tweet)
        
        resp.status = falcon.HTTP_200        
        resp.body = json_util.dumps(tweets, json_options=json_util.RELAXED_JSON_OPTIONS)

class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise falcon.http_status(falcon.HTTP_200, body='\n')

app = falcon.API(middleware=[HandleCORS()])
tweets = TweetsResources()
app.add_route('/tweets/{fechaDesde:dt("%Y-%m-%d-%Z")}/{fechaHasta:dt("%Y-%m-%d-%Z")}', tweets)