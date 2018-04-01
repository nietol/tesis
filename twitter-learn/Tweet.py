"""Modulo para manejo de tweets."""

from enum import IntEnum
from xml.etree import ElementTree
from enum import Enum
from text_processing import tokenize

GLOBAL_ENTITY = "GLOBAL_ENTITY"

class PolarityLevel(IntEnum):
    """Niveles de polaridad."""

    ninguno = 0
    positivo = 1
    negativo = 2
    neutral = 3

class AgreementLevel(IntEnum):
    """Niveles de acuerdo."""

    agreement = 0
    disagreement = 1


class Tweet:
    u"""Abtracción de un tweet."""

    def __init__(self, tweet_id, user, content, date, lang, sentiments, topics):
        """Constructor. Setea todos los valores propios de un tweet."""
        self.tweet_id = tweet_id
        self.user = user
        self.content = content
        self.date = date
        self.lang = lang
        # List of Polarity
        self.sentiments = sentiments
        # lista de strings, cada elemento es un topic
        self.topics = topics

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
        
        pol = [p for p in self.sentiments if p.entity == GLOBAL_ENTITY]        
        return pol[0].polarity
        
    def __str__(self):
        polarities = [[str(sentiment)] for sentiment in self.sentiments]
        return 'tweet id: {} \n content: {} \n polarities: {}'.format(self.tweet_id, self.content, polarities)

# end class Tweet


class Polarity:
    """Polaridad asociada a un tweet."""

    def __init__(self, entity, polarityValue, agreementLevel):
        """Constructor.
        Setea los datos propios de la polaridad.
        entity: entidad a la que hace referencia la polaridad.
        polarityValue: valor de polaridad.
        agreementLevel: valor de acuerdo.
        """

        self.entity = entity
        self.polarity = polarityValue
        self.type = agreementLevel

    @property
    def entity(self):
        return self.__entity

    @entity.setter
    def entity(self, value):
        self.__entity = value

    @property
    def polarity(self):
        p_level = PolarityLevel.ninguno

        if self.__polarity == 'N+':
            p_level = PolarityLevel.negativo
        elif self.__polarity == 'N':
            p_level = PolarityLevel.negativo
        elif self.__polarity == 'NEU':
            p_level = PolarityLevel.neutral
        elif self.__polarity == 'P':
            p_level = PolarityLevel.positivo
        elif self.__polarity == 'P+':
            p_level = PolarityLevel.positivo

        return p_level

    @polarity.setter
    def polarity(self, value):
        self.__polarity = value

    @property
    def type(self):
        t_value = None

        if self.__type == 'AGREEMENT':
            t_value = AgreementLevel.agreement
        elif self.__type == 'DISAGREEMENT':
            t_value = AgreementLevel.disagreement

        return t_value

    @type.setter
    def type(self, value):
        self.__type = value

    def __str__(self):
        return 'entity: {}, polaridad: {}, tipo: {}'.format(self.entity, self.polarity, self.type)

# end class Polarity

# module level functions

def create_tweets_from_xml(xml_file_path):
    """
    Factory method.
    Lee los tweets desde un xml y genera una lista de Tweet.
    """

    tree = ElementTree.parse(xml_file_path)
    root = tree.getroot()

    tweets = []

    for tweet in root.iter('tweet'):

        tweet_id = int(tweet.find('tweetid').text)
        user = tweet.find('user').text
        content = tweet.find('content').text
        date = tweet.find('date').text
        lang = tweet.find('lang').text

        sentiments = []

        if tweet.find('sentiments') != None:
            for p in tweet.find('sentiments'):
                entity = p.find('entity').text if p.find('entity') is not None else GLOBAL_ENTITY
                polarity_value = p.find('value').text
                agreement_level = p.find('type').text if p.find('type') is not None else 'None'
                polarity = Polarity(entity, polarity_value, agreement_level)
                sentiments.append(polarity)

        topics = []

        if tweet.find('topics') != None:
            for t in tweet.find('topics'):
                topics.append(t.text)

        if content is not None:
            tweet = Tweet(tweet_id, user, content, date, lang, sentiments, topics)
            tweets.append(tweet)

    return tweets

if __name__ == "__main__":
    import sys
    xml_path = sys.argv[1]
    print(xml_path)
    tweets = create_tweets_from_xml(xml_path)

    count = 1
    for t in tweets:
        # print(str(t) + "\n")
        # print(count)
        print(t.content)
        print(t.tokenized_content)
        count += 1
