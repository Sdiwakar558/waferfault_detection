import boto3
import pandas as pd
import os
from datetime import datetime
import shutil
from App_Log_Writer.App_Logger import Logger
from aws_s3_conn.Aws_conn import Aws_conn_est


class upload_csv_to_s3:
    def __init__(self):
        self.Logwriter = Logger()
        self.good_file_path = "./Prediction_data/Good_Raw/"
        self.S3_fileOBJ = "/waferfaultdatacsv/ML_DATASET/wafer_prediction.csv"
        self.curr_date_time = datetime.now()
        self.curr_date = self.curr_date_time.date()
        self.curr_time = self.curr_date_time.strftime("%H:%M:%S")
        self.final_mearge_csv = "./Merge_csv/"
        self.aws_client_conn = Aws_conn_est().aws_connest()

    def mearge_all_csv(self):
        try:
            log_file = open("./Training_Log/merge_csv_for_s3.txt", "a+")
            self.Logwriter.log_writer(log_file, "CSV mearging started 20")
            if not os.path.exists(self.final_mearge_csv):
                os.makedirs(self.final_mearge_csv)
            else:
                shutil.rmtree(self.final_mearge_csv)
                os.makedirs(self.final_mearge_csv)
            self.Logwriter.log_writer(log_file, f"{self.final_mearge_csv} at line 26")
            final_dataframe = pd.DataFrame()
            for file in os.listdir(self.good_file_path):
                df_file = pd.read_csv(self.good_file_path + file)
                final_dataframe = pd.concat([final_dataframe, df_file])
            final = final_dataframe.drop('Unnamed: 0', axis=1)
            final.to_csv(f"./Merge_csv/Final_{self.curr_date}_Training.csv")
            self.Logwriter.log_writer(log_file,
                                      "Merge_csv and saved at path location " + self.final_mearge_csv + f"final_wafer_{self.curr_date}_{self.curr_time}.csv")
            log_file.close()
        except OSError:
            log_file = open("./Training_Log/merge_csv_for_s3.txt", "a+")
            self.Logwriter.log_writer(log_file, f"{OSError} occured")
            log_file.close()
            raise OSError
        except Exception as e:
            log_file = open("./Training_Log/merge_csv_for_s3.txt", "a+")
            self.Logwriter.log_writer(log_file, f"{e} occured")
            log_file.close()
            raise e

    def upload_csv_s3(self):
        try:
            log_file = open("./Training_Log/merge_csv_for_s3.txt", 'a+')
            self.Logwriter.log_writer(log_file, "Connection Started")
            client = self.aws_client_conn
            self.Logwriter.log_writer(log_file, "Connection established successfully")
            file_path = self.final_mearge_csv + [file for file in os.listdir(self.final_mearge_csv)][0]
            bucket = "waferfaultdatacsv"
            file = f"wafer_{self.curr_date}.csv"
            client.upload_file(file_path, bucket, file)
            self.Logwriter.log_writer(log_file, "File successfully uploaded to AWS S3")
            log_file.close()
        except OSError:
            log_file = open("./Training_Log/merge_csv_for_s3.txt", 'a+')
            self.Logwriter.log_writer(log_file, f"{OSError} occured")
            log_file.close()
        except Exception as e:
            log_file = open("./Training_Log/merge_csv_for_s3.txt", 'a+')
            self.Logwriter.log_writer(log_file, f"{e} Exception occured")
            log_file.close()
            raise e




    def fetch_csv_from_s3(self):
        try:
            log_file = open('./Training_Log/merge_csv_for_s3.txt','a+')
            self.Logwriter.log_writer(log_file,"file fetching from AWS S3 bucket started")
            client = self.aws_client_conn
            buckets = 'waferfaultdatacsv'
            Local_folder_path = r'C:\Users\diwashar\Waferfault_detection\pythonProject\Final_csv_file_fromAWS_S3'
            response_from_s3 = client.list_objects_v2(Bucket = buckets)
            file_name_to_download = response_from_s3['Contents'][0]['Key']
            client.download_file(buckets,file_name_to_download, Local_folder_path)
            print('download completed')
            self.Logwriter.log_writer(log_file,f"{response_from_s3} recieve this file from AWS S3 bucket")
            log_file.close()
            return response_from_s3
        except OSError:
            log_file = open('./Training_Log/merge_csv_for_s3.txt','a+')
            self.Logwriter.log_writer(log_file,f"{OSError} occurred")
            log_file.close()
        except Exception as e:
            log_file = open('./Training_Log/merge_csv_for_s3.txt', 'a+')
            self.Logwriter.log_writer(log_file,f"{e} error occurred")
            log_file.close()


