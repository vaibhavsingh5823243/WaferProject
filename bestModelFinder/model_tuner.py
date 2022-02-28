from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from appLogger import app_logger


class ModelTuner:
    """
    This class is created for finding best objectSaver
    along with there best parameters
    """
    def __init__(self):
        self.xgc = XGBClassifier(objective='binary:logistic')
        self.rfc = RandomForestClassifier()
        self.log = app_logger.AppLogger()

    def getXGBCBestParams(self,x_train,y_train):
        """
        This function will return XGBClassifier with best
        accuracy score and hypertune parameters.
        :param x_train: features of training data
        :param y_train: target values of training data
        :return: XGBClassifier objectSaver
        """
        try:
            xgb_params = {
                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]
            }
            xgb_grid = GridSearchCV(XGBClassifier(objective='binary:logistic'),param_grid=xgb_params,cv=5,verbose=3)
            xgb_grid.fit(x_train,y_train)
            xgb_model = XGBClassifier(**xgb_grid.best_params_)
            xgb_model.fit(x_train,y_train)
            message = f"XGBClassifier's best parameters are:{xgb_grid.best_params_}."
            self.log.logger(message)
            return xgb_model
        except Exception as e:
            self.log.logger(str(e))

    def getRandomForestClassifierBestParams(self,x_train,y_train):
        """
        This function will return the RandomForestClassifier with best accuracy score
        and hypertune parameter.
        :param x_train: features of training data
        :param y_train: target values
        :return: RandomForestClassifier
        """
        try:
            random_forest_param = {
                "n_estimators": [10, 50, 100, 130], "criterion": ['gini', 'entropy'],
                "max_depth": range(2, 4, 1), "max_features": ['auto', 'log2']
            }
            clf_grid = GridSearchCV(RandomForestClassifier(),param_grid=random_forest_param,cv=5,verbose=3)
            clf_grid.fit(x_train,y_train)
            clf_model = RandomForestClassifier(**clf_grid.best_params_)
            clf_model.fit(x_train,y_train)
            message = f"RandomForestClassifier's best parameters are:{clf_grid.best_params_}"
            self.log.logger(message)
            return clf_model
        except Exception as e:
            self.log.logger(str(e))

    def getBestModel(self,x_train,y_train,x_test,y_test):
        """
        This function will find the best objectSaver between
        XGBClassifier and RandomForestClassifier
        :param x_train:training dataset
        :param y_train:training target value
        :param x_test:validation dataset
        :param y_test:validation target value
        :return:best objectSaver between XGBClassifier and RandomForestClassifier
        """
        try:
            xgb_model = self.getXGBCBestParams(x_train,y_train)
            clf_model = self.getRandomForestClassifierBestParams(x_train,y_train)
            xgb_acc = xgb_model.score(x_test,y_test)
            clf_acc = clf_model.score(x_test,y_test)
            if xgb_acc<=clf_acc:
                message = f"XGBClassifier accuracy score:{xgb_acc}\n" \
                          f"RandomForestClassifier accuracy score:{clf_acc}."
                best_model = xgb_model
                best_model_name = 'XGBClassifier'
                accuracy = xgb_acc
            else:
                message = f"XGBClassifier roc_auc_score:{xgb_acc}\n" \
                          f"RandomForestClassifier roc_auc_score:{clf_acc}."
                best_model = clf_model
                best_model_name = 'RandomForestClassifier'
                accuracy = clf_acc
            self.log.logger(message)

            message = f"Best objectSaver:{best_model_name}" \
                      f"Best Model Accuracy Score:{accuracy}"
            self.log.logger(message)
            return best_model,best_model_name
        except Exception as e:
            self.log.logger(str(e))
