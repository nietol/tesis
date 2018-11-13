from pymongo import MongoClient

def _get_database():
    """Returns classification_data_store database."""

    client = MongoClient('localhost', 27017)
    db = client.classification_data_store
    return db

def _get_tweets_collection():
    """Returns tweets collection"""

    db = _get_database()
    return db.tweets

def insert_one(tweet):
    """Insert one tweet into tweets collection
    Returns an instance of InsertOneResult.
    """
    
    tc = _get_tweets_collection()
    inserted_id = tc.insert_one(tweet.to_dict()).inserted_id
    return inserted_id

def find(filter):
    """Busca documentos dentro de la colección tweets filtrados según filter."""

    tc = _get_tweets_collection()
    cursor = tc.find(filter)
    return cursor

if __name__ == "__main__":
    from ...domain.Tweet import Tweet, PolarityLevel
    from datetime import datetime

    tweet = Tweet(1, 'usuario', 'contenido', datetime.now(), PolarityLevel.ninguno, None)
    #print(tweet.to_dict())
    insert_one(tweet)