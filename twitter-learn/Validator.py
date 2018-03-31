"""
    Modulo para la validación de modelos de clasificación.
"""

from sklearn.model_selection import KFold, cross_val_score, cross_val_predict, GridSearchCV, train_test_split
from sklearn.metrics import precision_recall_fscore_support, make_scorer, classification_report, confusion_matrix

class KFoldValidator:
    """KFold Cross Validation"""

    def __init__(self, model, data_frame):
        self.model = model
        self.data_frame = data_frame
    
    def validate(self):
        """KFold validation"""

        data = self.data_frame['tweet'].values
        target = self.data_frame['polarity'].values

        predicted = cross_val_predict(estimator=self.model, X=data, y=target)
        
        target_names = ['ninguno', 'positivo', 'negativo', 'neutral']
        report = classification_report(target, predicted, target_names=target_names)

        return report

    def gird_serach_cv(self):
        """GridSearchCV for linear svm"""

        data = self.data_frame['tweet'].values
        target = self.data_frame['polarity'].values

        # Split the dataset in two equal parts
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.33, random_state=42)

        #[0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5]
        parameters = {'classifier__kernel':['linear'], 'classifier__C':[0.1, 0.25, 0.5, 0.75, 1]}
        # parameters = {'classifier__C':[1, 10]}
        grid = GridSearchCV(self.model, cv=3, n_jobs=4, param_grid=parameters, scoring='f1_weighted')

        #fit model
        grid.fit(X_train, y_train)
        #predict test set
        y_pred = grid.predict(X_test)

        target_names = ['ninguno', 'positivo', 'negativo', 'neutral']
        report = classification_report(y_test, y_pred, target_names=target_names)
        confusion = confusion_matrix(y_test, y_pred)


        return report, confusion, grid.best_params_
        
if __name__ == "__main__":
    import sys
    from clasification import build_data_frame
    from clasification import build_model
    from Tweet import create_tweets_from_xml

    xml_path = sys.argv[1]    
    training_tweets = create_tweets_from_xml(xml_path)

    df = build_data_frame(training_tweets)
    model = build_model()

    kfold = KFoldValidator(model, df)    
    report, confusion, params = kfold.gird_serach_cv()

    print(report)
    print(confusion)
    print('params: ', params)
