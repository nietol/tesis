import numpy
import pandas as pd
from pandas import DataFrame
from Tweet import create_tweets_from_xml
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC, SVC
from sklearn.externals import joblib

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
        ('vectorizer',  CountVectorizer(lowercase=False, tokenizer=tokenize, binary=True)),
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

def save_model(model, file_name):
    joblib.dump(model, file_name)

def load_model(file_name):
    return joblib.load(file_name)

if __name__ == "__main__":
    '''
    import sys
    from sklearn.metrics import classification_report, confusion_matrix    
    xml_path = sys.argv[1]

    tweets = create_tweets_from_xml(xml_path)
    df = build_data_frame(tweets)
    data = df['tweet'].values
    target = df['polarity'].values
    '''
    svm_model_estimator = load_model('MODELS/svm_model_linear_0.25')
    print(svm_model_estimator.named_steps['vectorizer'].tokenizer)

    '''
    target_pred = svm_model_estimator.predict(data)

    target_names = ['ninguno', 'positivo', 'negativo', 'neutral']
    report = classification_report(target, target_pred, target_names=target_names)
    confusion = confusion_matrix(target, target_pred)
    
    print(report)
    print(confusion)
    '''


    
