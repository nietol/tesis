# Universidad Nacional del Sur
## Tesis de Licenciatura en Ciencias de la Computación
## Minería de Opinión en Twitter
## Clasificación de Tweets y Visualización de Tendencias de Opinión

### Setup de Ambiente

Esta tesis se encuentra dividida en tres proyectos:

*	twitter-learn: implementación de algoritmos orientados a generar el modelo de clasificación que utiliza el motor para clasificar los tweets en tiempo real. Se encuentra escrito en Python.
* classification_engine: implementación del backend que realiza la clasificación en tiempo real y expone API REST para ser consumida por el cliente. Se encuentra escrito en Python.
* classification_interface: implementación del frontend. HTML + CSS + Javascript.

Para los dos proyectos escritos en Python, para su ejecución, es necesario generar un ambiente con la versión 3.5 del intérprete. Por otro lado, cada uno tiene definido el archivo freeze.pip con sus dependencias. Una vez generado el ambiente y restauradas las dependencias, el siguiente paso es activar el ambiente y estamos listos para ejecutarlo.

En cuanto a **classification_interface**, se trata de un sitio web que se comunica mediante AJAX con el API que expone el backend, para su ejecución solo basta abrirlo con un browser. Es necesario estar conectado a internet (por las dependencias en librerías como jquery y google maps). La versión del browser tiene que soportar el control **input datetime-local**

#### Pasos para la generación del ambiente en los proyectos escritos en Python

1. Generar el ambiente: python3.5 -m venv env
2. Restaurar dependencias: pip install -r freeze.pip
3. Activar el ambiente: . env/bin/activate

### Ejecución de classification_engine

### Configuraciones

#### Backend - **classification_engine**

El backend se conecta a Twitter Streaming API. Es necesario establecer los keys que el servicio necesita. En el archivo **./classification_engine/infraestructure/twitter/authentication.py** se define el setup de estas keys...

```python
CONSUMER_KEY = "SETUP_KEY"
CONSUMER_SECRET = "SETUP_KEY"

ACCESS_TOKEN = "SETUP_KEY"
ACCESS_TOKEN_SECRET = "SETUP_KEY"
```

Por otro lado, la conexión a la base de datos se define dentro de los *DALs*

**./classification_engine/infraestructure/odm/raw_tweets_dal.py**
**./classification_engine/infraestructure/odm/tweets_dal.py**

```python
def _get_database():
    """Returns classification_data_store database."""

    client = MongoClient('localhost', 27017)
    db = client.classification_data_store
    return db
```

Modificarlo acorde al setup de base de datos que se esté utilizando.

##### Ejecución del backend

El proyecto se desarrolló usando gunicorn como servidor web para hostear el backend. Para su ejecución ejecutar el siguiente comando, sobre el directorio padre a *classification_engine*:

**gunicorn --reload --timeout 300 classification_engine.services.startup:app**

#### Frontend - **classification_interface**

1. En el archivo **.\classification_interface\assets\scripts.js** se encuentran definidos los endpoints que expone el backend y consuma la interfaz...

```javascript
var endpoints = {
    tweets: 'http://127.0.0.1:8000/tweets',
    classifications: 'http://127.0.0.1:8000/classifications',
    realtimetweets: 'http://127.0.0.1:8000/realtimetweets'
}
```
De realizarse algún cambio en el endpoind donde se hostean estos servicios es necesario replicarlo en esta configuración.

2. En el archivo **.\classification_interface\index.html**, sobre el final, se encuentra la inyección de las dependencias de Google Maps JavaScript API. Modificar (**SETUP_KEY**) con la propia obtenida de Google Maps Platform.

```html
<script src="https://maps.googleapis.com/maps/api/js?key=SETUP_KEY&callback=mapsSetup"></script>
```

nltk stopwords download

python -m nltk.downloader stopwords
