import numpy
import pandas as pd
from pandas import DataFrame
from Tweet import create_tweets_from_xml
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC, SVC

from text_processing import tokenize

def build_data_frame(tweets):
    """Genera data frame. Cada fila està compuesta por el contenido de un tweet y su polaridad"""

    rows = []
    index = []
    for tweet in tweets:
        rows.append({'tweet': tweet.content, 'polarity': tweet.polarity})
        index.append(tweet.tweet_id)

    data_frame = DataFrame(rows, index=index)
    return data_frame

def build_model():
    """Genera modelo de predicciòn"""

    pipeline = Pipeline([
        ('vectorizer',  CountVectorizer(lowercase=False, tokenizer=tokenize)),
        ('classifier',  SVC()) ])
        #('classifier',  LinearSVC()) ])
    
    return pipeline

def fit_model(tweets):
    """Construye modelo y lo ajusta en base a los datos de entrenamiento para poder realizar
    predicciones en la polaridad de tweets"""

    data_frame = build_data_frame(tweets)
    model = build_model()

    model.fit(data_frame['tweet'].values, data_frame['polarity'].values)
    return model

if __name__ == "__main__":
    import sys
    xml_path = sys.argv[1]
    samples_path = sys.argv[2]
    training_tweets = create_tweets_from_xml(xml_path)
    samples_tweets = create_tweets_from_xml(samples_path)
    
    pd.set_option('display.max_colwidth', -1)
    
    model = fit_model(training_tweets)
    samples = [t.content for t in samples_tweets]    
    
    # print(training_df.to_html())    
    
    predictions = model.predict(samples)

    for i in range(len(predictions)):
        print(str(samples_tweets[i].tweet_id) + ":" + str(predictions[i]))

    # print(predictions)