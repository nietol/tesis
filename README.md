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

Por otro lado, **classification_interface** es un sitio web que se comunica mediante AJAX con el API que expone el backend, para su ejecución solo basta con abrirlo con un browser. Es necesario estar conectado a internet (por las dependencias en librerías como jquery y google maps). La versión del browser tiene que soportar el control **input datetime-local**

#### Pasos para la generación del ambiente en los proyectos escritos en Python

1. Generar el ambiente: python3.5 -m venv env
2. Restaurar dependencias: pip install -r freeze.pip
3. Activar el ambiente: . env/bin/activate

### Ejecución de classification_engine

### Configuraciones

nltk stopwords download

python -m nltk.downloader stopwords
