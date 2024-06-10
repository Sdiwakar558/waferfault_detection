import os.path
import shutil
from Upload_CSVTOS3.mearge_csv_for_s3 import upload_csv_to_s3
from Client_Raw_Data_Validation.Raw_Data_Validation import Raw_data_validations
from App_Log_Writer.App_Logger import Logger
import pandas as pd
from sklearn.model_selection import train_test_split
from Training_model_data import Training_model_class
from Best_model_Tuner.Model_Tuner import Model_Tuner
from Data_Preprocessing.Clustering import Create_Kmeans_Clustering
from File_operation.File_methods import File_operation


class maincalling_function:
    def __init__(self):

        self.Create_kmeans_Clustering = Create_Kmeans_Clustering()
        self.raw_data_validation = Raw_data_validations()
        self.upload_csv_to_s3 = upload_csv_to_s3()
        self.Training_model_class = Training_model_class()
        self.Model_Tuner = Model_Tuner()
        self.training_data = Training_model_class().pure_data_provider_for_training()
        self.Logwriter = Logger()

    def calling_function_arrangement(self):
        if os.path.exists("./Training_Log/main_process.txt"):
            os.remove("./Training_Log/main_process.txt")
        log_file = open("./Training_Log/main_process.txt", 'a+')
        self.Logwriter.log_writer(log_file, "Raw_Data_Validation.py   methods started")
        self.raw_data_validation.creating_copy_of_complete_data()
        schema_data = self.raw_data_validation.fetchdatafrom_schema_training()
        manual_regex = self.raw_data_validation.manualregex()
        self.raw_data_validation.read_training_batchfolder(manual_regex)
        NumberofColumns = schema_data[3]
        self.raw_data_validation.validate_file_columndetails(NumberofColumns)
        self.raw_data_validation.validateMissingValueInWholeColumn()
        self.Logwriter.log_writer(log_file, "Raw_Data_Validation.py   methods Completed")

        # #               Above are the line which are responsible to call
        # #               Raw_Data_Validation (file)
        # #               of class
        # #               Raw_data_validations

        self.Logwriter.log_writer(log_file, ",merge_csv_for_s3.py      methods calling started")
        self.upload_csv_to_s3.mearge_all_csv()
        self.upload_csv_to_s3.upload_csv_s3()
        self.Logwriter.log_writer(log_file, ",merge_csv_for_s3.py      methods calling Completed")

        # fetch data from AWS S3 bucket
        self.Logwriter.log_writer(log_file, 'fetching data from AWS S3 buckets')
        # data_fetch_from_s3 = self.upload_csv_to_s3.fetch_csv_from_s3()


        # spliting data in independent,dependent


        self.independent_data_X, self.dependent_data_Y = self.training_data[0], self.training_data[1]

        # Applying the clustering approach

        kmeans_cluster_return = self.Create_kmeans_Clustering
        number_of_cluster = kmeans_cluster_return.elbow_plot(self.independent_data_X)
        independent_data_X_with_cluster = kmeans_cluster_return.create_cluster(self.independent_data_X,number_of_cluster)
        independent_data_X_with_cluster['Results'] = self.dependent_data_Y
        File_operation().check_folderexistance()
        for cluster_number in range(number_of_cluster):
            individual_cluster_data = independent_data_X_with_cluster[independent_data_X_with_cluster['Cluster']==cluster_number]
            dependent_data_Y_for_distinct_cluster = individual_cluster_data['Results']
            individual_cluster_data_without_cluster_label = individual_cluster_data.drop(['Results','Cluster'],axis = 1)
            X_train,X_test,Y_train,Y_test = train_test_split(individual_cluster_data_without_cluster_label,dependent_data_Y_for_distinct_cluster)
            Final_model,model_name=self.Model_Tuner.get_best_model(X_train,Y_train,X_test,Y_test)
            File_operation().save_model(Final_model,model_name)

        log_file.close()
    def predict_model(self):
        independent_data_X= self.training_data[0]
        File_operation().load_model(independent_data_X)



if __name__ == "__main__":
    # data_from_s3 = upload_csv_to_s3().fetch_csv_from_s3()
    # maincalling_function().calling_function_arrangement()
    maincalling_function().predict_model()




