from sklearn.base import BaseEstimator, ClassifierMixin

from Tweet import PolarityLevel

class SimpleClassifier(BaseEstimator, ClassifierMixin):  
    """
        Clasifica un mensaje como positivo, negativo, neutral o ninguno en término
        de la ocurrencia de términos positivos y negativos en él.

        Un mensaje con mayor cantidad de palabras positivas será positivo, en sentido inverso,
        de tener mayor cantidad de términos negativos será considerado negativo,
        de tener similar número de términos negativos y positivos, será considerado neutro
        y de no contar con términos positivos o negativos será considerado como un mensaje
        que no expresa opinión.        
    """

    def __init__(self):
        pass

    def fit(self, X=None, y=None):
        """
            Lee los archivos que contienen las palabras positivas y negativas que permiten predecir la clase
            a la que pertenece el mensaje.
        """

        self.palabras_positivas_ = set(line.strip() for line in open('./DATA/palabras_positivas.txt', encoding='ISO-8859-1'))
        self.palabras_negativas_ = set(line.strip() for line in open('./DATA/palabras_negativas.txt', encoding = 'ISO-8859-1'))       

        return self

    def _predict_class(self, x):
        '''
            Retorna una de las clases definidas en PolarityLevel. Polaridad/Clase a la que
            pertenece el mensaje x.

            Ejemplo de mensaje: ['hola', 'mundo']
        '''

        clase = PolarityLevel.ninguno
        
        count_pos = sum([1 for word in x if word in self.palabras_positivas_])
        count_neg = sum([1 for word in x if word in self.palabras_negativas_])

        if count_pos > count_neg:
            clase = PolarityLevel.positivo
        elif count_pos < count_neg:
            clase = PolarityLevel.negativo
        elif count_pos + count_neg > 0:
            clase = PolarityLevel.neutral

        return clase

    def predict(self, X, y=None):
        """
            Recibe una lista de mensajes, representados como una lista de tokens (palabras),
            y determina en términos de la ocurrencia de positivos y negaticos
            a que clase pertenece. Donde las clases y criterios para determinarlas son:

                * ninguno: si el mensaje no cuenta con términos positivos ni negativos.
                * positivo: si el mensaje cuenta con mayor ocurrencia de términos positivos.
                * negativo: si el mensaje cuenta con mayor ocurrencia de términos negativos.
                * neutral: si el mensaje cuenta con igual ocurrencia de términos positivos y negativos.

            Ejemplo lista de mensajes: [['hola', 'mundo'], ['que', 'tal'], ... ]

            Returns:
                Lista de clases, el mensaje i-ésimo del input pertenece a la i-ésima clase predicha.

                Ejemplo: ['0', '2', ... ]
        """
        try:
            getattr(self, 'palabras_positivas_')
            getattr(self, 'palabras_negativas_')
        except AttributeError:
            raise RuntimeError('You must train classifer before predicting data!')

        return [self._predict_class(x) for x in X]

