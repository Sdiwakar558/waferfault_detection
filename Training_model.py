import os
from App_Log_Writer.App_Logger import Logger
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
class Training_model:
    def __init__(self):
        self.filepath = "./Merge_csv/"

    def pure_data_provider_for_training(self):
        log_file = open("./Training_Log/Training_model.txt",'a+')

        files = os.listdir(self.filepath)
        files_name = self.filepath+files[0]
        dataframe = pd.read_csv(files_name)
        dataframe.rename(columns={'Good/Bad':'Output'},inplace=True)
        X = dataframe.iloc[:,2:-1]
        Y = dataframe['Output']
        arr = []
        try:
            knnimputer = KNNImputer(n_neighbors=3,weights='uniform',missing_values=np.nan,)
            arr = knnimputer.fit_transform(X)
            Final_precessed_data = pd.DataFrame(arr,columns=X.columns)
            print(Final_precessed_data)
            print(Y)
            return Final_precessed_data,Y
        except Exception as e:
            raise e


Method_call = Training_model().pure_data_provider_for_training()



