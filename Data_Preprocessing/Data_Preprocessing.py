import os.path

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from App_Log_Writer.App_Logger import Logger
class Data_Preprocessing:
    def __init__(self):
        self.logwriter = Logger()

    def impute_missing_value(self):
        files= os.listdir("./Merge_csv/")
        files_name = "./Merge_csv/"+files[0]
        dataframe = pd.read_csv(files_name)
        dataframe.rename(columns={'Good/Bad':'Output'},inplace=True)
        X = dataframe.iloc[:,2:-1]
        Y = dataframe['Output']
        log_file = open("../Training_Log/Data_Preprocessing.txt",'a+')
        self.logwriter.log_writer(log_file,"imputing_missing_values started")
        arr=[]
        try:
            imputer = KNNImputer(missing_values=np.nan,n_neighbors=3,weights='uniform')
            arr = imputer.fit_transform(X)
            New_data = pd.DataFrame(arr,columns=X.columns).isnull().sum()
            return New_data,Y
        except Exception as e:
            raise e
