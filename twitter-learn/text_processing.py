"""
Modulo para el procesamiento de los tweets.
Procesamiento:
    * Stemming (lemmatization). ok
    * Tokenization. ok.
    * Tratamiento de emoticones. Se toman como un token.
    * Tratamiento signos de puntuación. ok. Se remueven.
    * Remover stop words. ok.
    * Lower case words. ok, se realiza en el proceso de Tokenization.
    * Eliminar urls y emails. ok.
    * Eliminar @user. ok, se realiza en el proceso de Tokenization
    * Replace #hashtag with hashtag (eliminate #) ok.
    * Los caracteres repetidos más de tres veces se contraen, por ejemplo hooooooola -> hooola. Se realiza en el proceso de Tokenization.
"""

import re
from string import punctuation

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

from nltk.tokenize import TweetTokenizer
from nltk.tokenize.casual import URLS as REG_EXP_URL
from nltk.tokenize.casual import EMOTICONS as REG_EXP_EMOTICONS

from sklearn.feature_extraction.text import CountVectorizer

HASHTAG = r"""\#+([\w_]+[\w\'_\-]*[\w_]+)"""
E_MAIL_ADDRESS = r"""[\w.+-]+@[\w-]+\.(?:[\w-]\.?)+[\w-]"""

def _signos_puntuacion():
    """Retorna una lista de signos de puntuación y de dígitos."""

    signos = list(punctuation)
    signos.extend(['¿', '¡', '“', '”'])
    signos.extend(map(str, range(10)))

    return signos

def _is_emoticon(token):
    """Determina si el token es un emoticon."""

    emoticon_re = re.compile(REG_EXP_EMOTICONS, re.VERBOSE | re.I | re.UNICODE)
    match = emoticon_re.match(token)

    return match is not None

def _remover_signos_puntuacion(token):
    """Remueve del token los signos de puntuación definidos en _signos_puntuacion si no forman emoticones."""

    token_txt = token

    if not _is_emoticon(token):
        signos = _signos_puntuacion()
        token_txt = [ch for ch in token if ch not in signos]
        token_txt = ''.join(token_txt)

    return token_txt

def _is_url(cadena):
    """Determina si la cadena es una url."""

    re_obj = re.compile(REG_EXP_URL, re.VERBOSE | re.I | re.UNICODE)
    match = re_obj.match(cadena)

    return match is not None or cadena.startswith('http')

def _is_email_address(cadena):
    """Determina si la cadena es una dirección de correo electrónico."""

    re_obj = re.compile(E_MAIL_ADDRESS, re.VERBOSE | re.I | re.UNICODE)
    match = re_obj.match(cadena)
    return match is not None

def _remove_email_address(text):
    re_obj = re.compile(E_MAIL_ADDRESS, re.VERBOSE | re.I | re.UNICODE)    
    return re_obj.sub('', text)

def _strip_hashtag(cadena):
    """Si la cadena es un hashtag, elimina el #."""

    return cadena.lstrip('#')
    # re_obj = re.compile(HASHTAG, re.VERBOSE | re.I | re.UNICODE)
    # return re_obj.sub(cadena)

def _is_stop_word(word):
    """Determina si word es stopword"""

    return word in stopwords.words('spanish')

def _stem_tokens(tokens):
    stemmer = SnowballStemmer('spanish')
    stemmed = []

    for item in tokens:
        stemmed.append(stemmer.stem(item))

    return stemmed

def tokenize(text):
    """Convierte un texto en una lista de tokens."""

    # tokenize
    # strip_handles: Remove Twitter username handles (@user) from text.
    # reduce_len: Replace repeated character sequences of length 3 or greater with sequences of length 3.
    # preserve_case: If it is set to False, then the tokenizer will downcase everything except for emoticons.
    tweet_tokenize = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False)
    tokens = tweet_tokenize.tokenize(text)

    # remueve de todos los tokens los signos de puntiación
    tokens = [_remover_signos_puntuacion(token) for token in tokens]
    tokens = [token for token in tokens if token]

    # remueve los tokens que son urls o direcciones de email
    tokens = [token for token in tokens if not (_is_url(token) or _is_email_address(token))]

    # remueve # de los hashtags
    tokens = [_strip_hashtag(token) for token in tokens]

    # remueve stopwords
    tokens = [token for token in tokens if not _is_stop_word(token)]

    # stem
    stems = _stem_tokens(tokens)    

    return stems

def simple_classifier_tokenizer(input_text):
    '''Genera la lista de palabras que maneja el clasificador SimpleClassifier.        
    Al mensaje, tweet, se lo procesa de la siguiente manera:            
        * Lower case words.
        * Eliminar @user.
        * Tratamiento signos de puntuación. Se remueven.
        * Eliminar urls y emails.
        * Replace #hashtag with hashtag (eliminate #).
        * Remover stop words.     
    '''

    # remueve direcciones de emails
    text = _remove_email_address(input_text)

    # tokenize
    # strip_handles: Remove Twitter username handles (@user) from text.        
    # preserve_case: If it is set to False, then the tokenizer will downcase everything except for emoticons.
    tweet_tokenize = TweetTokenizer(strip_handles=True, reduce_len=False, preserve_case=False)
    tokens = tweet_tokenize.tokenize(text)

    # remueve de todos los tokens los signos de puntiación
    tokens = [_remover_signos_puntuacion(token) for token in tokens]
    tokens = [token for token in tokens if token]

    # remueve los tokens que son urls
    tokens = [token for token in tokens if not (_is_url(token))]

    # remueve # de los hashtags
    tokens = [_strip_hashtag(token) for token in tokens]

    # remueve stopwords
    tokens = [token for token in tokens if not _is_stop_word(token)] 

    return tokens

if __name__ == "__main__":
    text = '#casas @leo. FirmaDO http://hola.com nieto.l@gmail.com de la nieto.l@gmail.ar comiendo comer comidas comoda comodas compila compilación'
    #tokens = tokenize(text)
    tokens = simple_classifier_tokenizer(text)    
    print(tokens)
    for t in tokens:
        print(t)
