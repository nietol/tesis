from pymongo import MongoClient

def _get_database():
    """Returns classification_data_store database."""

    client = MongoClient('localhost', 27017)
    db = client.classification_data_store
    return db

def _get_raw_tweets_collection():
    """Returns tweets collection"""

    db = _get_database()
    return db.raw_tweets

def insert_one(raw_tweet):
    """Insert one tweet into raw tweets collection
    Returns an instance of InsertOneResult.
    """    

    tc = _get_raw_tweets_collection()
    inserted_id = tc.insert_one(raw_tweet).inserted_id
    return inserted_id

def find(filter):
    """Busca documentos dentro de la colección raw_tweets filtrados según filter."""

    tc = _get_raw_tweets_collection()
    cursor = tc.find(filter)
    return cursor

def update_one(raw_tweet):
    """Actualiza el tweet en la colección raw_tweets.
        params
            raw_tweet: dict
    """
    
    tc = _get_raw_tweets_collection()
    result = tc.update_one({'_id': raw_tweet['_id']}, {"$set": raw_tweet}, upsert=False)
    return result