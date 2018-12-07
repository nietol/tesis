"""
Modulo destinado a la generación de las métricas del modelo basado en SimpleClassifier
"""

from SimpleClassifier import SimpleClassifier
from text_processing import simple_classifier_tokenizer

from sklearn.metrics import precision_recall_fscore_support, make_scorer, classification_report, confusion_matrix

def build_metrics(data_frame):
    """GridSearchCV for linear svm"""

    texts = data_frame['tweet'].values
    target = data_frame['polarity'].values

    data = [] #lista de lista de términos: [['hola','bien', 'día'], ['que', 'tal'], ...]

    for text in texts:
        tokens = simple_classifier_tokenizer(text)
        data.append(tokens)
    
    sc = SimpleClassifier()
    
    sc.fit()
    target_pred = sc.predict(data)

    target_names = ['ninguno', 'positivo', 'negativo', 'neutral']
    report = classification_report(target, target_pred, target_names=target_names)
    confusion = confusion_matrix(target, target_pred)

    return report, confusion

if __name__ == "__main__":
    import sys
    from clasification import build_data_frame    
    from Tweet import create_tweets_from_xml

    xml_path = sys.argv[1]    
    training_tweets = create_tweets_from_xml(xml_path)

    df = build_data_frame(training_tweets)
    report, confusion = build_metrics(df)

    print(report)
    print(confusion)    