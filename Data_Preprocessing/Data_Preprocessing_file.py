import os
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from App_Log_Writer.App_Logger import Logger
class Data_Preprocessing:
    def __init__(self):
        self.logwriter = Logger()

    def impute_missing_value(self, X):
        log_file = open("./Training_Log/Data_Preprocessing.txt", "a+")
        self.logwriter.log_writer(log_file, "Imputing missing value started")
        arr = []
        try:
            imputer = KNNImputer(missing_values=np.nan, n_neighbors=3, weights='uniform')
            arr = imputer.fit_transform(X)
            new_data = pd.DataFrame(arr, columns=X.columns)
            self.logwriter.log_writer(log_file, "Imputing missing value Completed")
            log_file.close()
            return new_data
        except Exception as e:
            log_file = open("./Training_Log/Data_Preprocessing.txt", 'a+')
            self.logwriter.log_writer(log_file, f"{e} Occured")
            log_file.close()
            raise e