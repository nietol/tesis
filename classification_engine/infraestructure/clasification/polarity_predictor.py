import os.path

from sklearn.externals import joblib
from ...domain.Tweet import PolarityLevel

__ESTIMATOR__ = None

def predict(tweet_text):
    """Predice la polaridad del tweet."""

    global __ESTIMATOR__

    if __ESTIMATOR__ is None:
        __ESTIMATOR__ = __load_model()

    content = [tweet_text]
    target_pred = __ESTIMATOR__.predict(content)

    polarity = PolarityLevel(target_pred[0])

    return polarity

def __load_model():
    base_path = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(base_path, "estimators/svm_model_rbf")
    return joblib.load(file_name)


    
    



    
