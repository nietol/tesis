from enum import Enum, IntEnum
from ..infraestructure.clasification.text_processing import tokenize

class PolarityLevel(IntEnum):
    """Niveles de polaridad."""

    ninguno = 0
    positivo = 1
    negativo = 2
    neutral = 3

class Tweet:
    u"""Abtracción de un tweet."""

    def __init__(self, tweet_id, user, content, date, polarity_level):
        """Constructor. Setea todos los valores propios de un tweet."""
        self.tweet_id = tweet_id
        self.user = user
        self.content = content
        self.date = date        
        # PolarityLevel
        self.polarity_level = polarity_level

    @property
    def tokenized_content(self):
        """Retorna el texto del tweet tokenizado."""

        tokenized_txt = tokenize(self.content)
        return tokenized_txt
    
    @property
    def vector(self):
        """Retorna la representación vectorizada del tweet."""
        
        return -1
    
    @property
    def polarity(self):
        """Retorna la polaridad asociada al tweet."""
        
        return self.polarity_level

    def to_dict(self):
        """Returns dictionary with attribute:value"""

        return vars(self)
        # return { 'tweet_id': self.tweet_id, 'user': self.user, \
        # 'content': self.content, 'date': self.date, \
        # 'polarity_level': self.polarity_level }
        
    def __str__(self):        
        return 'tweet id: {} \n content: {} \n polarity: {}'.format(self.tweet_id, self.content, self.polarity_level)

# end class Tweet