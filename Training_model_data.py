import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from App_Log_Writer.App_Logger import Logger


class Training_model_class:
    def __init__(self):
        self.filepath = "./Merge_csv/"
        self.logwriter = Logger()

    def pure_data_provider_for_training(self):
        log_file = open("./Training_Log/Training_model_data.txt", 'w+')
        self.logwriter.log_writer(log_file, "Pure_data_provider_for_training (Methods calling started)")
        files = os.listdir(self.filepath)
        files_name = self.filepath + files[0]
        dataframe = pd.read_csv(files_name)

        dataframe.rename(columns={'Good/Bad': 'Output'}, inplace=True)
        X = dataframe.iloc[:, 2:-1]
        Y = dataframe['Output'].replace(-1, 0)
        self.logwriter.log_writer(log_file, "Data split successfully")
        arr = []
        try:
            self.logwriter.log_writer(log_file, "Knn imputer started")
            knnimputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            arr = knnimputer.fit_transform(X)
            Final_precessed_data = pd.DataFrame(arr, columns=X.columns)
            self.logwriter.log_writer(log_file, "Knn imputer completed")
            log_file.close()

            return Final_precessed_data, Y
        except Exception as e:
            log_file = open('./Training_Log/Training_model_data.txt', 'a+')
            self.logwriter.log_writer(log_file, f'{e} got this error')
            log_file.close()
