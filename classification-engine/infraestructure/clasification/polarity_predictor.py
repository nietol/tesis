import os.path

from sklearn.externals import joblib
from text_processing import tokenize

__ESTIMATOR__ = None

def predict(tweet_text):
    """Predice la polaridad del tweet."""

    global __ESTIMATOR__

    if __ESTIMATOR__ is None:
        __ESTIMATOR__ = load_model()

    content = [tweet_text]
    target_pred = __ESTIMATOR__.predict(content)

    return target_pred

def load_model():
    base_path = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(base_path, "estimators/svm_model_linear_0.25")
    return joblib.load(file_name)

if __name__ == "__main__":
    print(predict('bueno'))
    print(predict('malo'))
    print(predict('si no tal vez'))

    
    



    
