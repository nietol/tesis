from pymongo import MongoClient

def _get_database():
    """Returns classification_data_store database."""

    client = MongoClient('localhost', 27017)
    db = client.classification_data_store
    return db

def _get_tweets_collection():
    """Returns tweets collection"""

    db = _get_database()
    return db.raw_tweets

def insert_one(raw_tweet):
    """Insert one tweet into raw tweets collection
    Returns an instance of InsertOneResult.
    """
    
    tc = _get_tweets_collection()
    inserted_id = tc.insert_one(raw_tweet).inserted_id
    return inserted_id
