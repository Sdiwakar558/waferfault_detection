import os
from App_Log_Writer.App_Logger import Logger
import numpy as np
from Data_Preprocessing.Data_Preprocessing_file import Data_Preprocessing
import pandas as pd
from sklearn.impute import KNNImputer
from Data_Preprocessing.Clustering import Create_Kmeans_Clustering
from App_Log_Writer.App_Logger import Logger
class Training_model_class:
    def __init__(self):
        self.filepath = "./Merge_csv/"
        self.logwriter = Logger()

    def pure_data_provider_for_training(self):
        log_file = open("./Training_Log/Training_model.txt", "a+")
        self.logwriter.log_writer(log_file, "Pure_data_provider_for_training (Methods calling started)")
        files = os.listdir(self.filepath)
        files_name = self.filepath + files[0]
        dataframe = pd.read_csv(files_name)
        dataframe.rename(columns={'Good/Bad': 'Output'}, inplace=True)
        X = dataframe.iloc[:, 2:-1]
        Y = dataframe['Output']
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
            raise e

Training_model_class = Training_model_class()
Data = Training_model_class.pure_data_provider_for_training()[0]
processed_data = Data_Preprocessing().impute_missing_value(Data)
clustering_class = Create_Kmeans_Clustering()
results = clustering_class.elbow_plot(processed_data)
cluster_created = clustering_class.create_cluster(Data,results)


