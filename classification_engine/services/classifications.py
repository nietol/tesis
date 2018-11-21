"""
Clasificación de tweets en tiempo real.
"""

class ClassificationsResource:

    def on_post(self, req, resp, terms):
        """Inicia clasificaciòn de tweets en tiempo real. Filtra los mensajes según terms.
            Parametros
                terms: lista de términos.
        """

        pass
        #abrir el stream filtrando por los terminos
        #iniciar la clasificación
        #Ambos quedan corriendo en background.
        #terminar con un 201 created o similar

    def on_put(self, req, resp):
        """Si está ejecutando, detiene la clasificación en tiempo real de tweets.
        """

        pass
