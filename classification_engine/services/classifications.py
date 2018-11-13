import falcon

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
        tweets_dal.find({date: {''}})