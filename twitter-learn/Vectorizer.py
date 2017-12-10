import pickle
from sklearn.feature_extraction.text import CountVectorizer

class Vectorizer:
    u"""Vectorización de texto."""
    
    def __init__(self, tweet, corpus):
        """Constructor."""
        self.tweet = tweet
        self.corpus = corpus
        
    def fit_save(self, file_name):
        """Construye vocabulario y lo serializa en archivo."""
        count_vectorizer = CountVectorizer()
        model = count_vectorizer.fit(self.corpus)
        
        
    def load(self, file_name):
        """Deserealiza vocabulario."""
        
    def transform(self):
        """Retorna matriz de documentos."""
        