from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score
from xgboost import XGBClassifier
from App_Log_Writer.App_Logger import Logger
from Training_model_data import Training_model_class
from sklearn.model_selection import train_test_split

class Model_Tuner:
    def __init__(self):
        self.logwriter = Logger()
        self.RFC = RandomForestClassifier()
        self.XGBC = XGBClassifier(objective='binary:logistic')

    log_file = open("./Training_Log/Model_tuner.txt", 'r+')
    log_file.close()
    def get_best_parameter_for_random_forest(self, train_X, train_Y):
        try:
            log_file = open("./Training_Log/Model_Tuner.txt", "a+")
            self.logwriter.log_writer(log_file, "Model_tuner calling started")
            cv_param = {"n_estimators": [10, 50, 100, 130], "criterion": ['gini', 'entropy'],
                        "max_depth": range(2, 4, 1), "max_features": ['sqrt', 'log2']}
            grid_cv = GridSearchCV(estimator=self.RFC, param_grid=cv_param, cv=5, verbose=3)
            grid_cv.fit(train_X, train_Y)
            best_parameter = grid_cv.best_params_  #best_parameter
            criterion = best_parameter['criterion']
            max_depth = best_parameter['max_depth']
            max_features = best_parameter['max_features']
            n_estimators = best_parameter['n_estimators']
            RFC = RandomForestClassifier(criterion=criterion, max_depth=max_depth, max_features=max_features,
                                              n_estimators=n_estimators)
            RFC.fit(train_X, train_Y)  #training model
            return RFC
        except Exception as e:
            raise e
    def get_best_parameter_for_XGBoost(self, train_X, train_Y):
        try:
            log_file = open("./Training_Log/Model_Tuner.txt", "a+")
            self.logwriter.log_writer(log_file, "Prameter finding for Xgboost model started")
            param_for_XGBoost = {
                'learning_rate': [0.5, 0.1, 0.01, 0.001],
                'max_depth': [3, 5, 10, 20],
                'n_estimators': [10, 50, 100, 200]}
            grid_cvXGboost = GridSearchCV(XGBClassifier(objective='binary:logistic'), param_grid=param_for_XGBoost,
                                          verbose=3, cv=5)
            grid_cvXGboost.fit(train_X, train_Y)
            best_param_XGBC = grid_cvXGboost.best_params_
            learning_rate = best_param_XGBC['learning_rate']
            max_depth = best_param_XGBC['max_depth']
            n_estimators = best_param_XGBC['n_estimators']
            XGBC = XGBClassifier(max_depth=max_depth, learning_rate=learning_rate, n_estimators=n_estimators)
            XGBC.fit(train_X, train_Y)
            return XGBC
        except Exception as e:
            log_file = open("./Training_Log/Model_Tuner.txt",'a+')
            self.logwriter.log_writer(log_file,f'{e} error occured')
            log_file.close()

    def get_best_model(self,train_X,train_Y,test_X,test_Y):
        try:
            log_file = open("./Training_Log/Model_Tuner.txt",'a+')
            self.logwriter.log_writer(log_file,"Finding best parameter started")
            self.Xgboost = self.get_best_parameter_for_XGBoost(train_X,train_Y)
            predict_xgboost = self.Xgboost.predict(test_X)
            self.Random_forest = self.get_best_parameter_for_random_forest(train_X, train_Y)
            Randomforest_predict = self.Random_forest.predict(test_X)

            if len(test_Y.unique())==1:
                self.Xgboost_score = accuracy_score(test_Y,predict_xgboost)
                self.logwriter.log_writer(log_file,f'got score {self.Xgboost_score} accuracy score')
            else:
                self.Xgboost_score = roc_auc_score(test_Y,predict_xgboost)
                self.logwriter.log_writer(log_file,f'got score {self.Xgboost_score} from roc_auc_score')


            if len(test_Y.unique())==1:
                self.Random_forest_score = accuracy_score(test_Y,Randomforest_predict)
                self.logwriter.log_writer(log_file,f"Got this {self.Random_forest_score} Random_forest_score score from accuracy_score")
            else:
                self.Random_forest_score = roc_auc_score(test_Y,Randomforest_predict)
                self.logwriter.log_writer(log_file,f"Got this {self.Random_forest_score} Random_forest_score score from roc_auc_score")


            if self.Random_forest_score>self.Xgboost_score:
                 return self.Random_forest,'Random_forest'
            else:
                return self.Xgboost,'XG_boost'
        except Exception as e:
            log_file = open('./Training_Log/Model_Tuner.txt','a+')
            self.logwriter.log_writer(log_file,f'{e} occured')
            log_file.close()