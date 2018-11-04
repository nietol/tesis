from enum import Enum, IntEnum
from ..infraestructure.clasification.text_processing import tokenize

import copy

class GeoPoint:

    def __init__(self, latitud, longitud):
        self.latitud = latitud
        self.longitud = longitud
    
    def to_dict(self):
        return copy.deepcopy(vars(self))

class PolarityLevel(IntEnum):
    """Niveles de polaridad."""

    ninguno = 0
    positivo = 1
    negativo = 2
    neutral = 3

class Tweet:
    u"""Abtracción de un tweet."""

    def __init__(self, tweet_id, user, content, date, polarity_level, geo):
        """Constructor. Setea todos los valores propios de un tweet.
        params
            polarity_level: PolarityLevel
            geo: GeoPoint
        """
        self.tweet_id = tweet_id
        self.user = user
        self.content = content
        self.date = date        
        self.polarity_level = polarity_level
        self.geo = geo

    @property
    def tokenized_content(self):
        """Retorna el texto del tweet tokenizado."""

        tokenized_txt = tokenize(self.content)
        return tokenized_txt
    
    @property
    def polarity(self):
        """Retorna la polaridad asociada al tweet."""
        
        return self.polarity_level.name

    def to_dict(self):
        """Returns dictionary with attribute:value"""

        data = copy.deepcopy(vars(self))

        data['geo'] = self.geo.to_dict()
        data['polarity_str'] = self.polarity
        data['tokenized_content'] = self.tokenized_content

        return data
        
    def __str__(self):        
        return 'tweet id: {} \n content: {} \n polarity: {} \n geo: {}'.format(self.tweet_id,
            self.content, self.polarity_level, self.geo.to_dict())

# end class Tweet